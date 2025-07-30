import importlib
from typing import Any, TYPE_CHECKING
from gxkit.core import __version__

_EXPORTS = {
    "dbclient": "dbtools.dbclient",
}

_SUBMODULES = ["dbtools"]

__all__ = list(_EXPORTS.keys()) + _SUBMODULES

__version__ = __version__


def __getattr__(name: str) -> Any:
    """懒加载所有模块"""
    if name in _EXPORTS:
        module_path = f"gxkit.{_EXPORTS[name]}"
        module = importlib.import_module(module_path, __name__)
        return getattr(module, name)
    if name in _SUBMODULES:
        return importlib.import_module(f".{name}", __name__)
    raise AttributeError(f"module {__name__} has no attribute {name}")


def __dir__():
    """返回IDE可识别的顶层列表"""
    return __all__


if TYPE_CHECKING:
    from gxkit.dbtools.dbclient import dbclient
