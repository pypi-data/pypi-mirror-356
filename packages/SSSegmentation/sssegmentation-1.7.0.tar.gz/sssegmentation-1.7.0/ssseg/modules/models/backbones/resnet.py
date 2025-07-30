'''
Function:
    Implementation of ResNet
Author:
    Zhenchao Jin
'''
import torch
import torch.nn as nn
import torch.utils.checkpoint as checkpoint
from ...utils import loadpretrainedweights
from .bricks import BuildNormalization, BuildActivation


'''DEFAULT_MODEL_URLS'''
DEFAULT_MODEL_URLS = {
    'resnet18': 'https://download.pytorch.org/models/resnet18-5c106cde.pth',
    'resnet34': 'https://download.pytorch.org/models/resnet34-333f7ec4.pth',
    'resnet50': 'https://download.pytorch.org/models/resnet50-19c8e357.pth',
    'resnet101': 'https://download.pytorch.org/models/resnet101-5d3b4d8f.pth',
    'resnet152': 'https://download.pytorch.org/models/resnet152-b121ed2d.pth',
    'resnet18conv3x3stem': 'https://download.openmmlab.com/pretrain/third_party/resnet18_v1c-b5776b93.pth',
    'resnet50conv3x3stem': 'https://download.openmmlab.com/pretrain/third_party/resnet50_v1c-2cccc1ad.pth',
    'resnet101conv3x3stem': 'https://download.openmmlab.com/pretrain/third_party/resnet101_v1c-e67eebb6.pth',
}
'''AUTO_ASSERT_STRUCTURE_TYPES'''
AUTO_ASSERT_STRUCTURE_TYPES = {}


'''BasicBlock'''
class BasicBlock(nn.Module):
    expansion = 1
    def __init__(self, inplanes, planes, stride=1, dilation=1, downsample=None, style='pytorch', use_checkpoint=False, norm_cfg=None, act_cfg=None):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=3, stride=stride, padding=dilation, dilation=dilation, bias=False)
        self.bn1 = BuildNormalization(placeholder=planes, norm_cfg=norm_cfg)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = BuildNormalization(placeholder=planes, norm_cfg=norm_cfg)
        self.relu = BuildActivation(act_cfg)
        self.downsample = downsample
        self.stride = stride
        self.dilation = dilation
        self.use_checkpoint = use_checkpoint
    '''forward'''
    def forward(self, x: torch.Tensor):
        def _forward(x):
            identity = x
            out = self.conv1(x)
            out = self.bn1(out)
            out = self.relu(out)
            out = self.conv2(out)
            out = self.bn2(out)
            if self.downsample is not None: identity = self.downsample(x)
            out += identity
            return out
        if self.use_checkpoint and x.requires_grad:
            out = checkpoint.checkpoint(_forward, x)
        else:
            out = _forward(x)
        out = self.relu(out)
        return out


'''Bottleneck'''
class Bottleneck(nn.Module):
    expansion = 4
    def __init__(self, inplanes, planes, stride=1, dilation=1, downsample=None, style='pytorch', use_checkpoint=False, norm_cfg=None, act_cfg=None):
        super(Bottleneck, self).__init__()
        assert style in ['pytorch', 'caffe']
        # set attributes
        self.inplanes = inplanes
        self.planes = planes
        self.stride = stride
        self.dilation = dilation
        self.downsample = downsample
        self.style = style
        self.use_checkpoint = use_checkpoint
        self.norm_cfg = norm_cfg
        self.act_cfg = act_cfg
        # build layers
        if self.style == 'pytorch':
            self.conv1_stride = 1
            self.conv2_stride = stride
        else:
            self.conv1_stride = stride
            self.conv2_stride = 1
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=1, stride=self.conv1_stride, padding=0, bias=False)
        self.bn1 = BuildNormalization(placeholder=planes, norm_cfg=norm_cfg)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=self.conv2_stride, padding=dilation, dilation=dilation, bias=False)
        self.bn2 = BuildNormalization(placeholder=planes, norm_cfg=norm_cfg)
        self.conv3 = nn.Conv2d(planes, planes * self.expansion, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn3 = BuildNormalization(placeholder=planes * self.expansion, norm_cfg=norm_cfg)
        self.relu = BuildActivation(act_cfg)
    '''forward'''
    def forward(self, x: torch.Tensor):
        def _forward(x):
            identity = x
            out = self.conv1(x)
            out = self.bn1(out)
            out = self.relu(out)
            out = self.conv2(out)
            out = self.bn2(out)
            out = self.relu(out)
            out = self.conv3(out)
            out = self.bn3(out)
            if self.downsample is not None: identity = self.downsample(x)
            out += identity
            return out
        if self.use_checkpoint and x.requires_grad:
            out = checkpoint.checkpoint(_forward, x)
        else:
            out = _forward(x)
        out = self.relu(out)
        return out


'''ResNet'''
class ResNet(nn.Module):
    arch_settings = {
        18: (BasicBlock, (2, 2, 2, 2)),
        34: (BasicBlock, (3, 4, 6, 3)),
        50: (Bottleneck, (3, 4, 6, 3)),
        101: (Bottleneck, (3, 4, 23, 3)),
        152: (Bottleneck, (3, 8, 36, 3))
    }
    def __init__(self, structure_type, in_channels=3, base_channels=64, stem_channels=64, depth=101, outstride=8, contract_dilation=True, use_conv3x3_stem=True, 
                 out_indices=(0, 1, 2, 3), use_avg_for_downsample=False, norm_cfg={'type': 'SyncBatchNorm'}, act_cfg={'type': 'ReLU', 'inplace': True}, style='pytorch',
                 pretrained=True, pretrained_model_path='', use_checkpoint=False):
        super(ResNet, self).__init__()
        # set attributes
        self.structure_type = structure_type
        self.in_channels = in_channels
        self.base_channels = base_channels
        self.stem_channels = stem_channels
        self.depth = depth
        self.outstride = outstride
        self.contract_dilation = contract_dilation
        self.use_conv3x3_stem = use_conv3x3_stem
        self.out_indices = out_indices
        self.use_avg_for_downsample = use_avg_for_downsample
        self.norm_cfg = norm_cfg
        self.act_cfg = act_cfg
        self.pretrained = pretrained
        self.pretrained_model_path = pretrained_model_path
        self.style = style
        self.use_checkpoint = use_checkpoint
        # assert
        if structure_type in AUTO_ASSERT_STRUCTURE_TYPES:
            for key, value in AUTO_ASSERT_STRUCTURE_TYPES[structure_type].items():
                assert hasattr(self, key) and (getattr(self, key) == value)
        self.inplanes = stem_channels
        # parse depth settings
        assert depth in self.arch_settings, f'invalid depth {depth} for resnet'
        block, num_blocks_list = self.arch_settings[depth]
        # parse outstride
        outstride_to_strides_and_dilations = {
            8: ((1, 2, 1, 1), (1, 1, 2, 4)), 16: ((1, 2, 2, 1), (1, 1, 1, 2)), 32: ((1, 2, 2, 2), (1, 1, 1, 1)),
        }
        assert outstride in outstride_to_strides_and_dilations, f'invalid outstride {outstride} for resnet'
        stride_list, dilation_list = outstride_to_strides_and_dilations[outstride]
        # whether replace the 7x7 conv in the input stem with three 3x3 convs
        if use_conv3x3_stem:
            self.stem = nn.Sequential(
                nn.Conv2d(in_channels, stem_channels // 2, kernel_size=3, stride=2, padding=1, bias=False),
                BuildNormalization(placeholder=stem_channels // 2, norm_cfg=norm_cfg),
                BuildActivation(act_cfg),
                nn.Conv2d(stem_channels // 2, stem_channels // 2, kernel_size=3, stride=1, padding=1, bias=False),
                BuildNormalization(placeholder=stem_channels // 2, norm_cfg=norm_cfg),
                BuildActivation(act_cfg),
                nn.Conv2d(stem_channels // 2, stem_channels, kernel_size=3, stride=1, padding=1, bias=False),
                BuildNormalization(placeholder=stem_channels, norm_cfg=norm_cfg),
                BuildActivation(act_cfg),
            )
        else:
            self.conv1 = nn.Conv2d(in_channels, stem_channels, kernel_size=7, stride=2, padding=3, bias=False)
            self.bn1 = BuildNormalization(placeholder=stem_channels, norm_cfg=norm_cfg)
            self.relu = BuildActivation(act_cfg)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        # make layers
        for i in range(4):
            planes = base_channels * 2**i
            res_layer = self.makelayer(
                block=block, inplanes=self.inplanes, planes=planes, num_blocks=num_blocks_list[i], stride=stride_list[i], dilation=dilation_list[i], 
                contract_dilation=contract_dilation, use_avg_for_downsample=use_avg_for_downsample, norm_cfg=norm_cfg, act_cfg=act_cfg, style=style,
                use_checkpoint=use_checkpoint,
            )
            setattr(self, f'layer{i+1}', res_layer)
            self.inplanes = planes * block.expansion
        # load pretrained weights
        if pretrained:
            state_dict = loadpretrainedweights(
                structure_type=structure_type, pretrained_model_path=pretrained_model_path, default_model_urls=DEFAULT_MODEL_URLS
            )
            self.load_state_dict(state_dict, strict=False)
    '''makelayer'''
    def makelayer(self, block, inplanes, planes, num_blocks, stride=1, dilation=1, contract_dilation=True, use_avg_for_downsample=False, norm_cfg=None, act_cfg=None, style='pytorch', use_checkpoint=False, block_extra_args=None):
        downsample = None
        dilations = [dilation] * num_blocks
        if contract_dilation and dilation > 1: dilations[0] = dilation // 2
        if stride != 1 or inplanes != planes * block.expansion:
            if use_avg_for_downsample:
                downsample = nn.Sequential(
                    nn.AvgPool2d(kernel_size=stride, stride=stride, ceil_mode=True, count_include_pad=False),
                    nn.Conv2d(inplanes, planes * block.expansion, kernel_size=1, stride=1, padding=0, bias=False),
                    BuildNormalization(placeholder=planes * block.expansion, norm_cfg=norm_cfg)
                )
            else:
                downsample = nn.Sequential(
                    nn.Conv2d(inplanes, planes * block.expansion, kernel_size=1, stride=stride, padding=0, bias=False),
                    BuildNormalization(placeholder=planes * block.expansion, norm_cfg=norm_cfg)
                )
        layers = []
        if block_extra_args is None: block_extra_args = dict()
        layers.append(block(inplanes, planes, stride=stride, dilation=dilations[0], downsample=downsample, norm_cfg=norm_cfg, act_cfg=act_cfg, style=style, use_checkpoint=use_checkpoint, **block_extra_args))
        for i in range(1, num_blocks): 
            layers.append(block(planes * block.expansion, planes, stride=1, dilation=dilations[i], norm_cfg=norm_cfg, act_cfg=act_cfg, style=style, use_checkpoint=use_checkpoint, **block_extra_args))
        return nn.Sequential(*layers)
    '''forward'''
    def forward(self, x):
        if self.use_conv3x3_stem:
            x = self.stem(x)
        else:
            x = self.conv1(x)
            x = self.bn1(x)
            x = self.relu(x)
        x = self.maxpool(x)
        x1 = self.layer1(x)
        x2 = self.layer2(x1)
        x3 = self.layer3(x2)
        x4 = self.layer4(x3)
        outs = []
        for i, feats in enumerate([x1, x2, x3, x4]):
            if i in self.out_indices: outs.append(feats)
        return tuple(outs)