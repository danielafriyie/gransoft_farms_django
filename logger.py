import logging
import os
from django.conf import settings

BASE_DIR = settings.BASE_DIR


class BaseLogger:
    """
    Base Logger class
    """

    def __init__(self, name=None, fmt=None, file_name=None, dir_name=None):
        self._name = name if name else __name__
        self._fmt = fmt if fmt else '%(asctime)s:%(levelname)s:%(message)s'
        self._dir_name = dir_name if dir_name else 'event_log'
        self._file_name = file_name if file_name else 'event.log'

        self._path = os.path.join(BASE_DIR, self._dir_name)
        if not os.path.exists(self._path):
            os.mkdir(self._path)

        self._logger = logging.getLogger(self._name)
        self._logger.setLevel(level=logging.DEBUG)

        self._log_file_manager()

        formatter = logging.Formatter(self._fmt)
        file_handler = logging.FileHandler(f'{self._path}/{self._file_name}')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        # stream_handler = logging.StreamHandler()
        # stream_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)
        # self._logger.addHandler(stream_handler)

    def _log_file_manager(self):
        """
        check if the log file is more than 10mb then it deletes it
        :return:
        """
        _path = f'{self._path}/{self._file_name}'
        if os.path.exists(_path):
            if os.path.getsize(_path) > 10485760:
                try:
                    os.remove(_path)
                except PermissionError as e:
                    self._logger.exception(e)

    def __call__(self):
        return self._logger


def logger(*args, **kwargs):
    _logger = BaseLogger(*args, **kwargs)
    return _logger()


def model_logger():
    _logger = BaseLogger(file_name='model.log')
    return _logger()


def error_check_logger():
    _logger = BaseLogger(file_name='error_check.log')
    return _logger()


def auth_log():
    _logger = BaseLogger(file_name='user_auth.log')
    return _logger()
