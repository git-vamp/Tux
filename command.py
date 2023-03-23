from enum import Enum
from typing import (TypedDict, Callable, List, Union, Awaitable)
import time
from os import listdir
from importlib import import_module
from logger import logger


class Command:
    def __init__(self):
        self._commands: List[CommandType] = []

    def get_commands(self):
        return self._commands


    def register_command(self):
        def wrapper(func: Callable[[List[str]], Awaitable]):
            self._commands.append({
                "keyword": func.__name__, "func": func
            })

        return wrapper

    @staticmethod
    def load_commands():
        load_time = 0
        loaded_commands: List[CommandClassType] = []
        for file in listdir(f"./commands"):
            logger.debug(file)
            if file.endswith("_command.py"):
                try:
                    load_start = time.time() * 1000
                    import_command = import_module(
                        f'commands.{file.replace(".py", "")}')

                    load_time += round(abs(load_start -
                                           time.time() * 1000))
                    command: CommandClassType = {
                        'command_class': import_command.command,
                        'name': file.replace('.py', ''),
                        'loaded': True,
                        'load_time': load_time
                    }
                    loaded_commands.append(command)
                    logger.debug(f"Command \"{command.get('name')}\" Loaded!")
                except ImportError:
                    logger.exception(f"Command Loading Failed!")
                finally:
                    pass

        logger.debug(f"Loaded All Plugins In {load_time}ms")
        return loaded_commands


class CommandType(TypedDict):
    keyword: str
    func: Callable[[List[str]], Awaitable]


class CommandClassType(TypedDict):
    command_class: Command
    name: str
    loaded: bool
    load_time: float


class CommandEventType(Enum):
    COMMAND = 1


class CommandEvent(TypedDict):
    type: CommandEventType
    name: str
    args: List[str]
    # state: str
    output: Union[str, None]
