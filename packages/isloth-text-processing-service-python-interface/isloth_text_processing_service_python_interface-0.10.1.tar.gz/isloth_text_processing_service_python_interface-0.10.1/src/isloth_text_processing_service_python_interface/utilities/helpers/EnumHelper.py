"""
EnumHelper.py
-------------
Provides helper methods for working with enums.
"""

from typing import Type, TypeVar
from isloth_python_common_lib.errors.BadRequestError import BadRequestError
from enum import Enum

T = TypeVar('T', bound=Enum)


class EnumHelper:
    """
    A utility class for safe enum lookups.
    """

    @staticmethod
    def get(enum_cls: Type[T], key: str) -> T:
        """
        Returns the enum value associated with the given key.

        Parameters
        ----------
        enum_cls : Type[T]
            The Enum class to look up.
        key : str
            The key to find in the enum.

        Returns
        -------
        T
            The corresponding enum value.

        Raises
        ------
        BadRequestError
            If the key does not exist in the enum.
        """
        try:
            return enum_cls[key]
        except KeyError:
            raise BadRequestError('Invalid enum key').add_invalid_input_error(str(enum_cls), key)
