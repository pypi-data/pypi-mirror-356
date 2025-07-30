
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import typing



class SerializationManager:
    def __init__(self): ...
    @staticmethod
    def open(string: typing.Union[java.lang.String, str]) -> typing.Any: ...
    @staticmethod
    def save(object: typing.Any, string: typing.Union[java.lang.String, str]) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.util.serialization")``.

    SerializationManager: typing.Type[SerializationManager]
