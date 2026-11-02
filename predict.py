import importlib as _importlib
import sys as _sys

_mod = _importlib.import_module('sentiment_app.predict')
_sys.modules[__name__] = _mod
