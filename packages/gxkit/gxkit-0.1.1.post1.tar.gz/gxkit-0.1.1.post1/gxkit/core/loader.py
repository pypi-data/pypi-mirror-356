import importlib


def try_import_module(module_name: str, hint: str = ""):
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        raise ImportError(
            f"Module [{module_name}] is not installed.\n"
            f"{hint or f'Please install it using: pip install {module_name}'}"
        ) from e


def try_import_dbtools():
    return try_import_module("gxkit_dbtools", "Please install it using: pip install gxkit-dbtools")


def try_import_dataprep():
    return try_import_module("gxkit_dataprep", "Please install it using: pip install gxkit-dataprep")
