import importlib, inspect, pkgutil, pathlib

PLUGINS = {"filter": {}, "tracker": {}, "renderer": {}, "exporter": {}}

def _scan(pkg_name):
    pkg_path = pathlib.Path(__file__).parent / "plugins" / pkg_name
    for _, mod, _ in pkgutil.iter_modules([str(pkg_path)]):
        mod = importlib.import_module(f"plugins.{pkg_name}.{mod}")
        for _, cls in inspect.getmembers(mod, inspect.isclass):
            if cls.__module__ == mod.__name__ and hasattr(cls, "_tag"):
                PLUGINS[cls._tag][cls.__name__.lower()] = cls

for group in ("filters", "trackers", "renderers", "exporters"):
    _scan(group)