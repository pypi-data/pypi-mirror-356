from __future__ import annotations
import openassetio._openassetio.log
import openassetio._openassetio.ui.hostApi
import openassetio._openassetio.ui.managerApi
import typing
__all__ = ['CppPluginSystemUIDelegateImplementationFactory', 'HybridPluginSystemUIDelegateImplementationFactory']
class CppPluginSystemUIDelegateImplementationFactory(openassetio._openassetio.ui.hostApi.UIDelegateImplementationFactoryInterface):
    kModuleHookName: typing.ClassVar[str] = 'openassetioUIPlugin'
    kPluginEnvVar: typing.ClassVar[str] = 'OPENASSETIO_UI_PLUGIN_PATH'
    @typing.overload
    def __init__(self, paths: str, logger: openassetio._openassetio.log.LoggerInterface) -> None:
        ...
    @typing.overload
    def __init__(self, logger: openassetio._openassetio.log.LoggerInterface) -> None:
        ...
    def identifiers(self) -> list[str]:
        ...
    def instantiate(self, identifier: str) -> openassetio._openassetio.ui.managerApi.UIDelegateInterface:
        ...
class HybridPluginSystemUIDelegateImplementationFactory(openassetio._openassetio.ui.hostApi.UIDelegateImplementationFactoryInterface):
    def __init__(self, factories: list[openassetio._openassetio.ui.hostApi.UIDelegateImplementationFactoryInterface], logger: openassetio._openassetio.log.LoggerInterface) -> None:
        ...
    def identifiers(self) -> list[str]:
        ...
    def instantiate(self, identifier: str) -> openassetio._openassetio.ui.managerApi.UIDelegateInterface:
        ...
