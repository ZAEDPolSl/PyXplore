from datetime import datetime
from abc import ABC, abstractmethod

class Bcolors:
    '''Colors used in Ilogger'''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ILogger(ABC):
    '''Abstract class for all logers'''

    @abstractmethod
    def info(self, message, context: str = None, tags: list = [], duration: int = 0, additional_info: str = None):
        print(f'{Bcolors.OKGREEN}{datetime.now().isoformat()}\tINFO:\t\t{message}')

    @abstractmethod
    def warning(self, message, context: str = None, tags: list = [], duration: int = 0, additional_info: str = None):
        print(f'{Bcolors.WARNING}{datetime.now().isoformat()}\tWARNING:\t{message}')

    @abstractmethod
    def error(self, message, context: str = None, tags: list = [], duration: int = 0, additional_info: str = None):
        print(f'{Bcolors.FAIL}{datetime.now().isoformat()}\tERROR:\t\t{message}')

    @abstractmethod
    def exception(self, message, context: str = None, tags: list = [], duration: int = 0, additional_info: str = None):
        print(f'{Bcolors.FAIL}{datetime.now().isoformat()}\tEXCEPTION:\t{message}')
    
    @abstractmethod
    def count(self, group: str, name: str, value: float, tags: list = []):
        pass

    @abstractmethod
    def signal(self, group: str, name: str, tags: list = []):
        print(f'{Bcolors.OKBLUE}{datetime.now().isoformat()}\tSIGNAL:\t\t{group}/{name} [{",".join(tags)}]')

class ConsoleLogger(ILogger):

    def __init__(self) -> None:
        super().__init__()
        self.info('Activated ConsoleLogger. Logs will be only visible in console!')

    def info(self, message, context: str = None, tags: list = [], duration: int = 0, additional_info: str = None):
        return super().info(message, context, tags, duration, additional_info)

    def warning(self, message, context: str = None, tags: list = [], duration: int = 0, additional_info: str = None):
        return super().warning(message, context, tags, duration, additional_info)
    
    def error(self, message, context: str = None, tags: list = [], duration: int = 0, additional_info: str = None):
        return super().error(message, context, tags, duration, additional_info)
    
    def exception(self, message, context: str = None, tags: list = [], duration: int = 0, additional_info: str = None):
        return super().exception(message, context, tags, duration, additional_info)

    def count(self, group: str, name: str, value: float, tags: list = []):
        return super().count(group, name, value, tags)

    def signal(self, group: str, name: str, tags: list = []):
        return super().signal(group, name, tags)
        