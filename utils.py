from config.config import Config
from config.config2 import Config2
import json

class Utils:

    @staticmethod
    def read_json(file_path):
        """ Read json to dict. """
        with open(file_path, 'rt') as f:
            return json.load(f, object_hook=lambda a: Config(**a))

class Utils2:

    @staticmethod
    def read_json(file_path):
        """ Read json to dict. """
        with open(file_path, 'rt') as f:
            return json.load(f, object_hook=lambda a: Config2(**a))




