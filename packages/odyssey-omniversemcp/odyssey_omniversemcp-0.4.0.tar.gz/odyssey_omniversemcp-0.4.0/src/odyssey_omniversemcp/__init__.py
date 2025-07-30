__version__ = "0.1.0"

# Initialize __all__ list
__all__ = ["__version__"]

# The mcp_server module can be imported directly without Isaac Sim dependencies
# For the direct connection mode
try:
    from . import server
    __all__.append("server")
except (ImportError, ModuleNotFoundError):
    pass