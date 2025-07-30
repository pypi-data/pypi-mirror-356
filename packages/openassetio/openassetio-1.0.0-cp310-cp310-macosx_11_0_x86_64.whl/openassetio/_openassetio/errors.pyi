from __future__ import annotations
import typing
__all__ = ['BatchElementError', 'BatchElementException', 'ConfigurationException', 'InputValidationException', 'NotImplementedException', 'OpenAssetIOException', 'UnhandledException']
class BatchElementError:
    class ErrorCode:
        """
        Members:
        
          kUnknown
        
          kInvalidEntityReference
        
          kMalformedEntityReference
        
          kEntityAccessError
        
          kEntityResolutionError
        
          kInvalidPreflightHint
        
          kInvalidTraitSet
        
          kAuthError
        """
        __members__: typing.ClassVar[dict[str, BatchElementError.ErrorCode]]  # value = {'kUnknown': <ErrorCode.kUnknown: 128>, 'kInvalidEntityReference': <ErrorCode.kInvalidEntityReference: 129>, 'kMalformedEntityReference': <ErrorCode.kMalformedEntityReference: 130>, 'kEntityAccessError': <ErrorCode.kEntityAccessError: 131>, 'kEntityResolutionError': <ErrorCode.kEntityResolutionError: 132>, 'kInvalidPreflightHint': <ErrorCode.kInvalidPreflightHint: 133>, 'kInvalidTraitSet': <ErrorCode.kInvalidTraitSet: 134>, 'kAuthError': <ErrorCode.kAuthError: 135>}
        kAuthError: typing.ClassVar[BatchElementError.ErrorCode]  # value = <ErrorCode.kAuthError: 135>
        kEntityAccessError: typing.ClassVar[BatchElementError.ErrorCode]  # value = <ErrorCode.kEntityAccessError: 131>
        kEntityResolutionError: typing.ClassVar[BatchElementError.ErrorCode]  # value = <ErrorCode.kEntityResolutionError: 132>
        kInvalidEntityReference: typing.ClassVar[BatchElementError.ErrorCode]  # value = <ErrorCode.kInvalidEntityReference: 129>
        kInvalidPreflightHint: typing.ClassVar[BatchElementError.ErrorCode]  # value = <ErrorCode.kInvalidPreflightHint: 133>
        kInvalidTraitSet: typing.ClassVar[BatchElementError.ErrorCode]  # value = <ErrorCode.kInvalidTraitSet: 134>
        kMalformedEntityReference: typing.ClassVar[BatchElementError.ErrorCode]  # value = <ErrorCode.kMalformedEntityReference: 130>
        kUnknown: typing.ClassVar[BatchElementError.ErrorCode]  # value = <ErrorCode.kUnknown: 128>
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    __hash__: typing.ClassVar[None] = None
    def __eq__(self, arg0: BatchElementError) -> bool:
        ...
    def __init__(self, code: BatchElementError.ErrorCode, message: str) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def code(self) -> BatchElementError.ErrorCode:
        ...
    @property
    def message(self) -> str:
        ...
class BatchElementException(OpenAssetIOException):
    def __init__(self, index: int, error, message: str):
        ...
class ConfigurationException(InputValidationException):
    pass
class InputValidationException(OpenAssetIOException):
    pass
class NotImplementedException(OpenAssetIOException):
    pass
class OpenAssetIOException(RuntimeError):
    pass
class UnhandledException(OpenAssetIOException):
    pass
