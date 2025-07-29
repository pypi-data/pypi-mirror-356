from kenat.day_arithmetic import (
    add_days,
    add_months,
    add_years,
    diff_in_days,
    diff_in_months,
    diff_in_years,
)

class TestAddDays:
    def test_add_days_within_same_month(self):
        start_date = {'year': 2016, 'month': 1, 'day': 10}
        result = add_days(start_date, 5)
        assert result == {'year': 2016, 'month': 1, 'day': 15}

    def test_add_days_crossing_month_boundary(self):
        start_date = {'year': 2016, 'month': 1, 'day': 28}
        result = add_days(start_date, 5)  # Month 1 has 30 days
        assert result == {'year': 2016, 'month': 2, 'day': 3}

    def test_add_days_crossing_year_boundary(self):
        # 2016 is not a leap year, so Pagume has 5 days
        start_date = {'year': 2016, 'month': 13, 'day': 4}
        result = add_days(start_date, 3)
        assert result == {'year': 2017, 'month': 1, 'day': 2}


class TestAddMonths:
    def test_add_months_within_same_year(self):
        start_date = {'year': 2016, 'month': 3, 'day': 10}
        result = add_months(start_date, 5)
        assert result == {'year': 2016, 'month': 8, 'day': 10}

    def test_add_months_with_year_rollover(self):
        start_date = {'year': 2016, 'month': 11, 'day': 10}
        result = add_months(start_date, 3) # 11 + 3 = 14 -> month 1 of next year
        assert result == {'year': 2017, 'month': 1, 'day': 10}

    def test_add_months_to_pagume_with_day_clamping(self):
        # 2015 is a leap year (Pagume has 6 days)
        start_date = {'year': 2015, 'month': 12, 'day': 30}
        # Adding 1 month moves it to Pagume. The day (30) is clamped to the max day of Pagume (6).
        result = add_months(start_date, 1)
        # NOTE: The original JS test expected day: 6, but for a non-leap year this would be 5.
        # My implementation correctly clamps to the last day of the month. 2015 is a leap year, so Pagume has 6 days.
        assert result == {'year': 2015, 'month': 13, 'day': 6}

    def test_add_negative_months(self):
        start_date = {'year': 2016, 'month': 3, 'day': 10}
        result = add_months(start_date, -4)
        assert result == {'year': 2015, 'month': 12, 'day': 10}


class TestAddYears:
    def test_add_years_simple(self):
        start_date = {'year': 2010, 'month': 5, 'day': 15}
        result = add_years(start_date, 3)
        assert result == {'year': 2013, 'month': 5, 'day': 15}

    def test_add_years_from_leap_pagume_to_non_leap_year(self):
        # 2011 is a leap year
        start_date = {'year': 2011, 'month': 13, 'day': 6}
        # 2012 is not a leap year, day should be clamped from 6 to 5
        result = add_years(start_date, 1)
        assert result == {'year': 2012, 'month': 13, 'day': 5}
    
    def test_add_years_from_leap_to_leap_year(self):
        # 2011 is a leap year
        start_date = {'year': 2011, 'month': 13, 'day': 6}
        # 2015 is also a leap year, day 6 is preserved
        result = add_years(start_date, 4)
        assert result == {'year': 2015, 'month': 13, 'day': 6}


class TestDiffInDays:
    def test_same_date_returns_zero(self):
        a = {'year': 2016, 'month': 5, 'day': 15}
        b = {'year': 2016, 'month': 5, 'day': 15}
        assert diff_in_days(a, b) == 0

    def test_diff_is_positive(self):
        a = {'year': 2016, 'month': 6, 'day': 10}
        b = {'year': 2016, 'month': 6, 'day': 5}
        assert diff_in_days(a, b) == 5

    def test_diff_is_negative(self):
        a = {'year': 2016, 'month': 6, 'day': 1}
        b = {'year': 2016, 'month': 6, 'day': 6}
        assert diff_in_days(a, b) == -5

    def test_diff_crossing_year_boundary(self):
        a = {'year': 2017, 'month': 1, 'day': 3}
        # 2016 has 5 days in Pagume. 2 days left in Pagume + 3 days in Meskerem = 5
        b = {'year': 2016, 'month': 13, 'day': 4}
        assert diff_in_days(a, b) == 4
    
    def test_diff_crossing_multiple_years(self):
        a = {'year': 2018, 'month': 1, 'day': 1}
        b = {'year': 2016, 'month': 1, 'day': 1}
        # Year 2016 (365 days) + Year 2017 (365 days) = 730
        assert diff_in_days(a, b) == 730


class TestDiffInMonths:
    def test_same_date_returns_zero(self):
        a = {'year': 2016, 'month': 5, 'day': 15}
        b = {'year': 2016, 'month': 5, 'day': 15}
        assert diff_in_months(a, b) == 0
    
    def test_diff_is_positive(self):
        a = {'year': 2016, 'month': 6, 'day': 10}
        b = {'year': 2016, 'month': 5, 'day': 5}
        assert diff_in_months(a, b) == 1

    def test_earlier_date_minus_later_date_is_negative(self):
        a = {'year': 2016, 'month': 5, 'day': 1}
        b = {'year': 2016, 'month': 6, 'day': 6}
        assert diff_in_months(a, b) == -2
        
    def test_diff_crossing_multiple_years(self):
        a = {'year': 2018, 'month': 1, 'day': 1}
        b = {'year': 2016, 'month': 1, 'day': 1}
        assert diff_in_months(a, b) == 26 # 2 years * 13 months/year


class TestDiffInYears:
    def test_same_date_returns_zero(self):
        a = {'year': 2016, 'month': 5, 'day': 15}
        b = {'year': 2016, 'month': 5, 'day': 15}
        assert diff_in_years(a, b) == 0

    def test_less_than_a_year_diff_is_zero(self):
        a = {'year': 2017, 'month': 1, 'day': 3}
        b = {'year': 2016, 'month': 1, 'day': 5}
        assert diff_in_years(a, b) == 0

    def test_exactly_one_year_diff(self):
        a = {'year': 2017, 'month': 1, 'day': 5}
        b = {'year': 2016, 'month': 1, 'day': 5}
        assert diff_in_years(a, b) == 1

    def test_diff_crossing_multiple_years(self):
        a = {'year': 2018, 'month': 1, 'day': 1}
        b = {'year': 2016, 'month': 1, 'day': 1}
        assert diff_in_years(a, b) == 2
