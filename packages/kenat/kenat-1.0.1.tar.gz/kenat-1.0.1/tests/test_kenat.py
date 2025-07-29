# tests/test_kenat.py

import pytest
import datetime
from kenat import Kenat

class TestKenatClass:
    """
    This class corresponds to the 'Kenat class' describe block in the JS test.
    It tests the constructor and formatting methods.
    """

    def test_should_create_an_instance_with_current_date(self):
        now = datetime.datetime.now()
        kenat = Kenat()
        gregorian = kenat.get_gregorian()

        # Check that the date parts match today's date
        assert gregorian['year'] == now.year
        assert gregorian['month'] == now.month
        assert gregorian['day'] == now.day

        # Check that the ethiopian property exists
        ethiopian = kenat.get_ethiopian()
        assert 'year' in ethiopian
        assert 'month' in ethiopian
        assert 'day' in ethiopian

    def test_should_convert_a_specific_ethiopian_date_correctly(self):
        kenat = Kenat("2016/9/15")
        assert kenat.get_gregorian() == {'year': 2024, 'month': 5, 'day': 23}
        assert kenat.get_ethiopian() == {'year': 2016, 'month': 9, 'day': 15}

    def test_to_string_should_return_ethiopian_date_string(self):
        kenat = Kenat("2016/9/15")
        # The 9th Ethiopian month is 'Ginbot'. The to_string() method uses Amharic.
        assert kenat.to_string() == "ግንቦት 15 2016 12:00 ጠዋት"

    def test_format_returns_ethiopian_date_string_in_english_and_amharic(self):
        kenat = Kenat("2017/1/15")  # Meskerem 15, 2017
        assert kenat.format({'lang': 'english'}) == "Meskerem 15 2017"
        assert kenat.format({'lang': 'amharic'}) == "መስከረም 15 2017"

    def test_format_in_geez_amharic_returns_correct_string(self):
        kenat = Kenat("2017/1/15")  # Meskerem 15, 2017
        assert kenat.format_in_geez_amharic() == "መስከረም ፲፭ ፳፻፲፯"


class TestKenatApiHelperMethods:
    """
    This class corresponds to the 'Kenat API Helper Methods' describe block.
    """

    @pytest.fixture(scope="class")
    def dates(self):
        """Provides a set of dates for testing comparisons."""
        return {
            "date1": Kenat("2016/8/15"),
            "date2": Kenat("2016/8/20"),
            "date3": Kenat("2016/8/15"),
            "leap": Kenat("2015/1/1"),      # 2015 is a leap year
            "non_leap": Kenat("2016/1/1"),  # 2016 is not
        }

    def test_is_before_should_correctly_compare_dates(self, dates):
        assert dates['date1'].is_before(dates['date2']) is True
        assert dates['date2'].is_before(dates['date1']) is False
        assert dates['date1'].is_before(dates['date3']) is False

    def test_is_after_should_correctly_compare_dates(self, dates):
        assert dates['date2'].is_after(dates['date1']) is True
        assert dates['date1'].is_after(dates['date2']) is False
        assert dates['date1'].is_after(dates['date3']) is False

    def test_is_same_day_should_correctly_compare_dates(self, dates):
        assert dates['date1'].is_same_day(dates['date3']) is True
        assert dates['date1'].is_same_day(dates['date2']) is False

    def test_start_of_month_should_return_first_day(self, dates):
        start = dates['date1'].start_of_month()
        assert start.get_ethiopian() == {'year': 2016, 'month': 8, 'day': 1}

    def test_end_of_month_should_return_last_day_of_standard_month(self, dates):
        end = dates['date1'].end_of_month()
        assert end.get_ethiopian() == {'year': 2016, 'month': 8, 'day': 30}

    def test_end_of_month_should_return_last_day_of_pagume_in_leap_year(self):
        pagume = Kenat("2015/13/1")  # 2015 is a leap year
        end = pagume.end_of_month()
        assert end.get_ethiopian() == {'year': 2015, 'month': 13, 'day': 6}

    def test_is_leap_year_should_correctly_identify_leap_years(self, dates):
        assert dates['leap'].is_leap_year() is True
        assert dates['non_leap'].is_leap_year() is False

    def test_weekday_should_return_correct_day_of_the_week(self):
        # 2016/9/15 ET is May 23, 2024 GC, which is a Thursday.
        # In JS getDay(), Thursday is 4.
        specific_date = Kenat("2016/9/15")
        assert specific_date.weekday() == 4