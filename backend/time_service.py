"""
Time-of-Day Service Module
Handles time period detection and management
"""
from datetime import datetime, time
from typing import Dict, Literal

TimeperiodType = Literal['day', 'night']

class TimeService:
    """Manages time period detection."""

    def __init__(self, day_start: str = "06:00", night_start: str = "22:00"):
        """
        Initialize the time service.

        Args:
            day_start: Time when day period starts (HH:MM format)
            night_start: Time when night period starts (HH:MM format)
        """
        self.day_start = self._parse_time(day_start)
        self.night_start = self._parse_time(night_start)

    def _parse_time(self, time_str: str) -> time:
        """
        Parse time string in HH:MM format.

        Args:
            time_str: Time string (e.g., "06:00")

        Returns:
            datetime.time object

        Raises:
            ValueError: If time string is invalid
        """
        try:
            hour, minute = map(int, time_str.split(':'))
            return time(hour, minute)
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Invalid time format: {time_str}. Expected HH:MM") from e

    def get_current_period(self, current_time: datetime = None) -> TimeperiodType:
        """
        Determine the current time period (day or night).

        Args:
            current_time: Current datetime (defaults to now)

        Returns:
            'day' or 'night'
        """
        if current_time is None:
            current_time = datetime.now()

        current = current_time.time()

        # Handle different scenarios based on day_start and night_start
        if self.day_start < self.night_start:
            # Normal case: day starts before night (e.g., 06:00 - 22:00)
            if self.day_start <= current < self.night_start:
                return 'day'
            else:
                return 'night'
        else:
            # Edge case: night starts before day (e.g., 22:00 - 06:00)
            # This means night period spans midnight
            if self.night_start <= current < self.day_start:
                return 'night'
            else:
                return 'day'

    def get_period_info(self, current_time: datetime = None) -> Dict[str, any]:
        """
        Get detailed information about the current time period.

        Args:
            current_time: Current datetime (defaults to now)

        Returns:
            Dictionary containing:
            {
                'period': 'day' or 'night',
                'current_time': ISO format timestamp,
                'day_start': Day start time string,
                'night_start': Night start time string
            }
        """
        if current_time is None:
            current_time = datetime.now()

        period = self.get_current_period(current_time)

        return {
            'period': period,
            'current_time': current_time.isoformat(),
            'day_start': self.day_start.strftime('%H:%M'),
            'night_start': self.night_start.strftime('%H:%M')
        }

    def is_day(self, current_time: datetime = None) -> bool:
        """
        Check if current time is during day period.

        Args:
            current_time: Current datetime (defaults to now)

        Returns:
            True if day, False if night
        """
        return self.get_current_period(current_time) == 'day'

    def is_night(self, current_time: datetime = None) -> bool:
        """
        Check if current time is during night period.

        Args:
            current_time: Current datetime (defaults to now)

        Returns:
            True if night, False if day
        """
        return self.get_current_period(current_time) == 'night'
