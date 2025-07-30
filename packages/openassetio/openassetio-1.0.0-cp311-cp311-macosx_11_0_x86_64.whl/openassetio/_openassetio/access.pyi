from __future__ import annotations
import typing
__all__ = ['DefaultEntityAccess', 'EntityTraitsAccess', 'PolicyAccess', 'PublishingAccess', 'RelationsAccess', 'ResolveAccess', 'kAccessNames']
class DefaultEntityAccess:
    """
    Members:
    
      kRead
    
      kWrite
    
      kCreateRelated
    """
    __members__: typing.ClassVar[dict[str, DefaultEntityAccess]]  # value = {'kRead': <DefaultEntityAccess.kRead: 0>, 'kWrite': <DefaultEntityAccess.kWrite: 1>, 'kCreateRelated': <DefaultEntityAccess.kCreateRelated: 2>}
    kCreateRelated: typing.ClassVar[DefaultEntityAccess]  # value = <DefaultEntityAccess.kCreateRelated: 2>
    kRead: typing.ClassVar[DefaultEntityAccess]  # value = <DefaultEntityAccess.kRead: 0>
    kWrite: typing.ClassVar[DefaultEntityAccess]  # value = <DefaultEntityAccess.kWrite: 1>
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
class EntityTraitsAccess:
    """
    Members:
    
      kRead
    
      kWrite
    """
    __members__: typing.ClassVar[dict[str, EntityTraitsAccess]]  # value = {'kRead': <EntityTraitsAccess.kRead: 0>, 'kWrite': <EntityTraitsAccess.kWrite: 1>}
    kRead: typing.ClassVar[EntityTraitsAccess]  # value = <EntityTraitsAccess.kRead: 0>
    kWrite: typing.ClassVar[EntityTraitsAccess]  # value = <EntityTraitsAccess.kWrite: 1>
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
class PolicyAccess:
    """
    Members:
    
      kRead
    
      kWrite
    
      kCreateRelated
    
      kRequired
    
      kManagerDriven
    """
    __members__: typing.ClassVar[dict[str, PolicyAccess]]  # value = {'kRead': <PolicyAccess.kRead: 0>, 'kWrite': <PolicyAccess.kWrite: 1>, 'kCreateRelated': <PolicyAccess.kCreateRelated: 2>, 'kRequired': <PolicyAccess.kRequired: 3>, 'kManagerDriven': <PolicyAccess.kManagerDriven: 4>}
    kCreateRelated: typing.ClassVar[PolicyAccess]  # value = <PolicyAccess.kCreateRelated: 2>
    kManagerDriven: typing.ClassVar[PolicyAccess]  # value = <PolicyAccess.kManagerDriven: 4>
    kRead: typing.ClassVar[PolicyAccess]  # value = <PolicyAccess.kRead: 0>
    kRequired: typing.ClassVar[PolicyAccess]  # value = <PolicyAccess.kRequired: 3>
    kWrite: typing.ClassVar[PolicyAccess]  # value = <PolicyAccess.kWrite: 1>
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
class PublishingAccess:
    """
    Members:
    
      kWrite
    
      kCreateRelated
    """
    __members__: typing.ClassVar[dict[str, PublishingAccess]]  # value = {'kWrite': <PublishingAccess.kWrite: 1>, 'kCreateRelated': <PublishingAccess.kCreateRelated: 2>}
    kCreateRelated: typing.ClassVar[PublishingAccess]  # value = <PublishingAccess.kCreateRelated: 2>
    kWrite: typing.ClassVar[PublishingAccess]  # value = <PublishingAccess.kWrite: 1>
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
class RelationsAccess:
    """
    Members:
    
      kRead
    
      kWrite
    
      kCreateRelated
    """
    __members__: typing.ClassVar[dict[str, RelationsAccess]]  # value = {'kRead': <RelationsAccess.kRead: 0>, 'kWrite': <RelationsAccess.kWrite: 1>, 'kCreateRelated': <RelationsAccess.kCreateRelated: 2>}
    kCreateRelated: typing.ClassVar[RelationsAccess]  # value = <RelationsAccess.kCreateRelated: 2>
    kRead: typing.ClassVar[RelationsAccess]  # value = <RelationsAccess.kRead: 0>
    kWrite: typing.ClassVar[RelationsAccess]  # value = <RelationsAccess.kWrite: 1>
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
class ResolveAccess:
    """
    Members:
    
      kRead
    
      kManagerDriven
    """
    __members__: typing.ClassVar[dict[str, ResolveAccess]]  # value = {'kRead': <ResolveAccess.kRead: 0>, 'kManagerDriven': <ResolveAccess.kManagerDriven: 4>}
    kManagerDriven: typing.ClassVar[ResolveAccess]  # value = <ResolveAccess.kManagerDriven: 4>
    kRead: typing.ClassVar[ResolveAccess]  # value = <ResolveAccess.kRead: 0>
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
kAccessNames: list = ['read', 'write', 'createRelated', 'required', 'managerDriven']
