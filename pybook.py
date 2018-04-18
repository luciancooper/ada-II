
from importlib import reload as _reload

def reload(*mods):
    for m in mods:
        _reload(m)
