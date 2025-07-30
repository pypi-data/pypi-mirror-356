"""
DateHelper.py
-------------
Provides utility functions for formatting and validating date and time values.
"""

from datetime import datetime, timezone


class DateHelper:
    """
    Utility class for date-related operations across services.

    Methods
    -------
    to_date_format(date: datetime) -> str | None
        Converts a datetime object to a standardized date string (YYYY-MM-DD).

    to_datetime_format(date: datetime) -> str | None
        Converts a datetime object to a standardized datetime string (YYYY-MM-DDTHH:MM:SSZ).

    is_future_date(date: datetime) -> bool
        Checks if the given date is in the future.

    is_past_date(date: datetime) -> bool
        Checks if the given date is in the past.
    """

    @staticmethod
    def to_date_format(date: datetime) -> str | None:
        """
        Convert a datetime to a UTC date string in ISO format (YYYY-MM-DD).

        Parameters
        ----------
        date : datetime
            The datetime object to convert.

        Returns
        -------
        str or None
            Formatted date string, or None if input is invalid.
        """
        if not date:
            return None
        return date.astimezone(timezone.utc).strftime('%Y-%m-%d')

    @staticmethod
    def to_datetime_format(date: datetime) -> str | None:
        """
        Convert a datetime to a UTC datetime string (YYYY-MM-DDTHH:MM:SSZ).

        Parameters
        ----------
        date : datetime
            The datetime object to convert.

        Returns
        -------
        str or None
            Formatted datetime string, or None if input is invalid.
        """
        if not date:
            return None
        return date.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    @staticmethod
    def is_future_date(date: datetime) -> bool:
        """
        Check if a datetime is in the future relative to now.

        Parameters
        ----------
        date : datetime
            The datetime object to check.

        Returns
        -------
        bool
            True if the date is in the future, False otherwise.
        """
        return date > datetime.now(timezone.utc)

    @staticmethod
    def is_past_date(date: datetime) -> bool:
        """
        Check if a datetime is in the past relative to now.

        Parameters
        ----------
        date : datetime
            The datetime object to check.

        Returns
        -------
        bool
            True if the date is in the past, False otherwise.
        """
        return date < datetime.now(timezone.utc)
