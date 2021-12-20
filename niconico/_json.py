# niconico.py - Json


try:
    from ujson import loads, dumps
except ImportError:
    from json import loads, dumps