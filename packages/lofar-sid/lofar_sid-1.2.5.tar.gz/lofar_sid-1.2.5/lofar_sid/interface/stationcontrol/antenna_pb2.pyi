from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Antenna_Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OK: _ClassVar[Antenna_Status]
    SUSPICIOUS: _ClassVar[Antenna_Status]
    BROKEN: _ClassVar[Antenna_Status]
    BEYOND_REPAIR: _ClassVar[Antenna_Status]
    NOT_AVAILABLE: _ClassVar[Antenna_Status]

class Antenna_Use(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AUTO: _ClassVar[Antenna_Use]
    ON: _ClassVar[Antenna_Use]
    OFF: _ClassVar[Antenna_Use]
OK: Antenna_Status
SUSPICIOUS: Antenna_Status
BROKEN: Antenna_Status
BEYOND_REPAIR: Antenna_Status
NOT_AVAILABLE: Antenna_Status
AUTO: Antenna_Use
ON: Antenna_Use
OFF: Antenna_Use

class Identifier(_message.Message):
    __slots__ = ("antennafield_name", "antenna_name")
    ANTENNAFIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    ANTENNA_NAME_FIELD_NUMBER: _ClassVar[int]
    antennafield_name: str
    antenna_name: str
    def __init__(self, antennafield_name: _Optional[str] = ..., antenna_name: _Optional[str] = ...) -> None: ...

class SetAntennaStatusRequest(_message.Message):
    __slots__ = ("identifier", "antenna_status")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ANTENNA_STATUS_FIELD_NUMBER: _ClassVar[int]
    identifier: Identifier
    antenna_status: Antenna_Status
    def __init__(self, identifier: _Optional[_Union[Identifier, _Mapping]] = ..., antenna_status: _Optional[_Union[Antenna_Status, str]] = ...) -> None: ...

class GetAntennaRequest(_message.Message):
    __slots__ = ("identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    identifier: Identifier
    def __init__(self, identifier: _Optional[_Union[Identifier, _Mapping]] = ...) -> None: ...

class SetAntennaUseRequest(_message.Message):
    __slots__ = ("identifier", "antenna_use")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ANTENNA_USE_FIELD_NUMBER: _ClassVar[int]
    identifier: Identifier
    antenna_use: Antenna_Use
    def __init__(self, identifier: _Optional[_Union[Identifier, _Mapping]] = ..., antenna_use: _Optional[_Union[Antenna_Use, str]] = ...) -> None: ...

class AntennaResult(_message.Message):
    __slots__ = ("identifier", "antenna_use", "antenna_status")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ANTENNA_USE_FIELD_NUMBER: _ClassVar[int]
    ANTENNA_STATUS_FIELD_NUMBER: _ClassVar[int]
    identifier: Identifier
    antenna_use: Antenna_Use
    antenna_status: Antenna_Status
    def __init__(self, identifier: _Optional[_Union[Identifier, _Mapping]] = ..., antenna_use: _Optional[_Union[Antenna_Use, str]] = ..., antenna_status: _Optional[_Union[Antenna_Status, str]] = ...) -> None: ...

class AntennaReply(_message.Message):
    __slots__ = ("success", "exception", "result")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    exception: str
    result: AntennaResult
    def __init__(self, success: bool = ..., exception: _Optional[str] = ..., result: _Optional[_Union[AntennaResult, _Mapping]] = ...) -> None: ...
