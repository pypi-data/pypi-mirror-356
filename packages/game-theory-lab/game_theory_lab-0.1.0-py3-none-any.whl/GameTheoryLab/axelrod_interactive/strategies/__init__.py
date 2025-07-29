import os
import importlib
import inspect
import pkgutil
from GameTheoryLab.axelrod_interactive.strategy import Strategy

STRATEGIES = {}

strategy_dir = os.path.dirname(__file__)

for finder, module_name, is_pkg in pkgutil.iter_modules([strategy_dir]):
    try:
        module = importlib.import_module(f".{module_name}", package=__package__)
    except Exception as e:
        print(f"Warning: Failed to import {module_name}: {e}")
        continue

    for name, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, Strategy) and obj is not Strategy and name != "User":
            globals()[name] = obj
            STRATEGIES[name] = obj

__all__ = list(STRATEGIES.keys())

locals().update(STRATEGIES)

import sys

def __getattr__(name):
    if name in STRATEGIES:
        return STRATEGIES[name]
    raise AttributeError(f"module {__name__} has no attribute {name}")

sys.modules[__name__].__dict__.update(STRATEGIES)


