"""
string_builder.py
-----------------
Efficient string builder for dynamic string assembly.
"""


class StringBuilder:
    """
    Utility for building strings efficiently by appending lines or values.

    Methods
    -------
    append(value: str) -> 'StringBuilder'
        Appends a string value to the current content.

    append_line(value: str) -> 'StringBuilder'
        Appends a string followed by a newline character.

    to_string() -> str
        Returns the current string content.
    """

    def __init__(self):
        self._content = []

    def append(self, value: str) -> 'StringBuilder':
        """
        Appends a string to the current content.

        Parameters
        ----------
        value : str
            The string to append.

        Returns
        -------
        StringBuilder
            The current instance for chaining.
        """
        self._content.append(value)
        return self

    def append_line(self, value: str) -> 'StringBuilder':
        """
        Appends a string followed by a newline character to the current content.

        Parameters
        ----------
        value : str
            The string to append with a newline.

        Returns
        -------
        StringBuilder
            The current instance for chaining.
        """
        self._content.append(value + '\n')
        return self

    def to_string(self) -> str:
        """
        Returns the full built string.

        Returns
        -------
        str
            The concatenated string.
        """
        return ''.join(self._content)
