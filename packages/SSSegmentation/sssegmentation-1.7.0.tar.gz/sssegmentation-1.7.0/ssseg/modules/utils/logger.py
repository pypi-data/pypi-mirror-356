'''
Function:
    Implementation of LoggerHandles
Author:
    Zhenchao Jin
'''
import time
from .misc import ismainprocess
from .modulebuilder import BaseModuleBuilder


'''LocalLoggerHandle'''
class LocalLoggerHandle():
    def __init__(self, logfilepath):
        self.logfilepath = logfilepath
    '''log'''
    def log(self, message, level='INFO', endwithnewline=True, main_process_only=False):
        if main_process_only and (not ismainprocess()):
            return
        message = f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {level}  {message}'
        print(message)
        if not message.endswith('\n') and endwithnewline:
            message = message + '\n'
        with open(self.logfilepath, 'a') as fp:
            fp.write(message)
    '''debug'''
    def debug(self, message, endwithnewline=True, main_process_only=False):
        self.log(message, 'DEBUG', endwithnewline, main_process_only)
    '''info'''
    def info(self, message, endwithnewline=True, main_process_only=False):
        self.log(message, 'INFO', endwithnewline, main_process_only)
    '''warning'''
    def warning(self, message, endwithnewline=True, main_process_only=False):
        self.log(message, 'WARNING', endwithnewline, main_process_only)
    '''error'''
    def error(self, message, endwithnewline=True, main_process_only=False):
        self.log(message, 'ERROR', endwithnewline, main_process_only)


'''LoggerHandleBuilder'''
class LoggerHandleBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'LocalLoggerHandle': LocalLoggerHandle,
    }
    '''build'''
    def build(self, logger_handle_cfg):
        return super().build(logger_handle_cfg)


'''BuildLoggerHandle'''
BuildLoggerHandle = LoggerHandleBuilder().build


'''TrainingLoggingManager'''
class TrainingLoggingManager():
    def __init__(self, log_interval_iters=None, log_interval_epochs=None, logger_handle_cfg={}, logger_handle=None):
        assert (log_interval_iters is None and log_interval_epochs is not None) or (log_interval_iters is not None and log_interval_epochs is None), 'please only specify either of `log_interval_iters` and `log_interval_epochs`'
        self.basic_log_dict = {}
        self.history_losses_log_dict = {}
        self.log_interval_iters = log_interval_iters
        self.log_interval_epochs = log_interval_epochs
        self.logger_handle = BuildLoggerHandle(logger_handle_cfg=logger_handle_cfg) if logger_handle is None else logger_handle
    '''log'''
    def autolog(self, main_process_only=False):
        cur_epoch, cur_iter = self.basic_log_dict['cur_epoch'], self.basic_log_dict['cur_iter']
        if self.log_interval_iters is not None:
            if cur_iter % self.log_interval_iters == 0:
                log_dict = self.getlogdict()
                self.logger_handle.info(log_dict, main_process_only=main_process_only)
                self.clear()
        else:
            if cur_epoch % self.log_interval_epochs == 0:
                log_dict = self.getlogdict()
                self.logger_handle.info(log_dict, main_process_only=main_process_only)
                self.clear()
    '''update'''
    def update(self, basic_log_dict, losses_log_dict):
        self.basic_log_dict = basic_log_dict
        for key, value in losses_log_dict.items():
            if key in self.history_losses_log_dict:
                self.history_losses_log_dict[key].append(value)
            else:
                self.history_losses_log_dict[key] = [value]
    '''getlogdict'''
    def getlogdict(self):
        log_dict = self.basic_log_dict.copy()
        for key in list(self.history_losses_log_dict.keys()):
            log_dict[key] = sum(self.history_losses_log_dict[key]) / len(self.history_losses_log_dict[key])
        return log_dict
    '''clear'''
    def clear(self):
        self.history_losses_log_dict.clear()