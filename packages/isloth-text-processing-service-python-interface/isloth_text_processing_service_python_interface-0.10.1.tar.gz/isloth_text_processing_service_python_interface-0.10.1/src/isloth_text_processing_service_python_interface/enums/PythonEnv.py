"""
PythonEnv.py
------------
Defines the runtime environment types for Python-based backend services.
"""

from enum import Enum


class PythonEnv(str, Enum):
    """
    Enum representing the different Python backend environments.

    Attributes
    ----------
    DEVELOPMENT : str
        Active development environment.
    PRODUCTION : str
        Live production environment.
    TEST : str
        Testing or CI/CD environment.
    """

    DEVELOPMENT = 'development'
    PRODUCTION = 'production'
    TEST = 'test'
