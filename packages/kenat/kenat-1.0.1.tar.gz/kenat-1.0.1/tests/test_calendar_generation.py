import pytest
import re
from kenat import Kenat

class TestGetMonthCalendar:
    """
    Tests the get_month_calendar method of the Kenat class.
    This corresponds to the 'print.test.js' file.
    """

    def test_should_return_30_days_for_standard_month(self):
        k = Kenat('2015/1/1')
        calendar = k.get_month_calendar(2015, 1)
        assert len(calendar) == 30

    def test_should_return_6_days_for_pagume_in_leap_year(self):
        # 2011 is a leap year in the Ethiopian calendar
        k = Kenat('2011/1/1')
        calendar = k.get_month_calendar(2011, 13)
        assert len(calendar) == 6

    def test_should_return_5_days_for_pagume_in_non_leap_year(self):
        k = Kenat('2012/1/1')
        calendar = k.get_month_calendar(2012, 13)
        assert len(calendar) == 5

    def test_each_day_includes_formatted_display_fields(self):
        k = Kenat('2015/2/1')
        calendar = k.get_month_calendar(2015, 2)
        day = calendar[0]
        
        assert 'display' in day['ethiopian']
        assert 'display' in day['gregorian']
        assert isinstance(day['ethiopian']['display'], str)
        assert isinstance(day['gregorian']['display'], str)

    def test_should_correctly_format_geez_numerals_when_use_geez_is_true(self):
        k = Kenat('2015/1/1')
        calendar = k.get_month_calendar(2015, 1, use_geez=True)
        day = calendar[0]
        
        # Check if the display string contains any Geez numeral characters
        assert re.search(r'[፩-፼]', day['ethiopian']['display']) is not None