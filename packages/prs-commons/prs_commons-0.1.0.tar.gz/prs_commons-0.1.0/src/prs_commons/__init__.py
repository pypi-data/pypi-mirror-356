"""
PRS Facade Common - A Python library for common facade functionality.

This package provides common utilities and clients for PRS microservices,
including Odoo RPC client and other shared functionality.
"""

__version__ = "0.1.0"

# Import key classes/functions to make them available at the package level
from .core import MyClass
from .odoo.rpc_client import OdooRPCClient

__all__ = ["__version__", "MyClass", "OdooRPCClient"]
