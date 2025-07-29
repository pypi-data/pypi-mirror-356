import pytest
from kenat.utils import (
    day_of_year,
    month_day_from_day_of_year,
    is_gregorian_leap_year,
    is_ethiopian_leap_year,
    get_ethiopian_days_in_month
)

@pytest.mark.parametrize("year, month, day, expected_doy", [
    (2023, 1, 1, 1),
    (2023, 2, 1, 32),
    (2023, 2, 28, 59),
    (2023, 3, 1, 60),
    (2024, 2, 29, 60),  # Leap year
    (2024, 3, 1, 61),   # Leap year
    (2023, 12, 31, 365),
    (2024, 12, 31, 366), # Leap year
])
def test_day_of_year(year, month, day, expected_doy):
    assert day_of_year(year, month, day) == expected_doy


@pytest.mark.parametrize("year, doy, expected_date", [
    (2023, 1, {'month': 1, 'day': 1}),
    (2023, 32, {'month': 2, 'day': 1}),
    (2023, 60, {'month': 3, 'day': 1}),
    (2024, 60, {'month': 2, 'day': 29}), # Leap year
    (2024, 61, {'month': 3, 'day': 1}),  # Leap year
    (2023, 365, {'month': 12, 'day': 31}),
    (2024, 366, {'month': 12, 'day': 31}),# Leap year
])
def test_month_day_from_day_of_year(year, doy, expected_date):
    assert month_day_from_day_of_year(year, doy) == expected_date


class TestLeapYearFunctions:
    @pytest.mark.parametrize("year, expected", [
        (2024, True), (1996, True), # Divisible by 4, not 100
        (2023, False), (2019, False),# Not divisible by 4
        (1900, False), (2100, False),# Divisible by 100, not 400
        (2000, True), (1600, True),  # Divisible by 400
    ])
    def test_is_gregorian_leap_year(self, year, expected):
        assert is_gregorian_leap_year(year) is expected

    @pytest.mark.parametrize("year, expected", [
        (2011, True), (2015, True), # year % 4 == 3
        (2010, False), (2012, False),# year % 4 != 3
    ])
    def test_is_ethiopian_leap_year(self, year, expected):
        assert is_ethiopian_leap_year(year) is expected


class TestGetEthiopianDaysInMonth:
    @pytest.mark.parametrize("month", range(1, 13))
    def test_returns_30_for_standard_months(self, month):
        assert get_ethiopian_days_in_month(2010, month) == 30
        assert get_ethiopian_days_in_month(2011, month) == 30 # Also for leap years

    @pytest.mark.parametrize("leap_year", [2011, 2015, 2019])
    def test_returns_6_for_pagume_in_leap_year(self, leap_year):
        assert get_ethiopian_days_in_month(leap_year, 13) == 6

    @pytest.mark.parametrize("non_leap_year", [2010, 2012, 2013, 2014])
    def test_returns_5_for_pagume_in_non_leap_year(self, non_leap_year):
        assert get_ethiopian_days_in_month(non_leap_year, 13) == 5