import sys
import types
import importlib
import importlib.abc
import importlib.util

# ====== Configuration ======
_VIRTUAL_ROOT = 'finda_tool'  # Public virtual package name
_REAL_ROOT = 'yuanlanlab_tool.src.s074.v01_01'  # Actual backend package path

# ====== Module cache ======
_module_cache = {}


# ====== Convert virtual module name to real module name ======
def to_real_module_name(virtual_name: str) -> str:
    return virtual_name.replace(_VIRTUAL_ROOT, _REAL_ROOT, 1)


# ====== Register virtual module to sys.modules ======
def register_virtual_module(fullname: str):
    if fullname in sys.modules:
        return sys.modules[fullname]

    real_name = to_real_module_name(fullname)

    try:
        real_mod = importlib.import_module(real_name)
        sys.modules[fullname] = real_mod
        return real_mod
    except ModuleNotFoundError:
        # If real module is not found, create a dummy package-like module
        dummy = types.ModuleType(fullname)
        dummy.__path__ = []  # Pretend to be a package
        sys.modules[fullname] = dummy
        return dummy


# ====== Custom MetaPathFinder for virtual module routing ======
class VirtualModuleFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname == _VIRTUAL_ROOT or fullname.startswith(_VIRTUAL_ROOT + '.'):
            return importlib.util.spec_from_loader(fullname, VirtualModuleLoader())
        return None


# ====== Custom Loader for virtual modules ======
class VirtualModuleLoader(importlib.abc.Loader):
    def create_module(self, spec):
        return None  # Use the default module creation behavior

    def exec_module(self, module):
        fullname = module.__name__
        if fullname in _module_cache:
            return

        real_name = to_real_module_name(fullname)
        try:
            real_mod = importlib.import_module(real_name)
            sys.modules[fullname] = real_mod
        except ModuleNotFoundError:
            module.__path__ = []  # Create a dummy package module
            sys.modules[fullname] = module

        _module_cache[fullname] = True


# ====== Install the import hook (only once) ======
if not any(isinstance(f, VirtualModuleFinder) for f in sys.meta_path):
    sys.meta_path.insert(0, VirtualModuleFinder())
