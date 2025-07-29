import importlib.metadata

try:
    __version__ = importlib.metadata.version("nqs_sdk")
except importlib.metadata.PackageNotFoundError:
    __version__ = "undefined -- not installed"
