from __future__ import annotations
import typing
__all__ = ['UIAccess']
class UIAccess:
    """
    Members:
    
      kRead
    
      kWrite
    
      kCreateRelated
    """
    __members__: typing.ClassVar[dict[str, UIAccess]]  # value = {'kRead': <UIAccess.kRead: 0>, 'kWrite': <UIAccess.kWrite: 1>, 'kCreateRelated': <UIAccess.kCreateRelated: 2>}
    kCreateRelated: typing.ClassVar[UIAccess]  # value = <UIAccess.kCreateRelated: 2>
    kRead: typing.ClassVar[UIAccess]  # value = <UIAccess.kRead: 0>
    kWrite: typing.ClassVar[UIAccess]  # value = <UIAccess.kWrite: 1>
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
