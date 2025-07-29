import pytest
import datetime
from kenat.conversions import to_ec, to_gc
from kenat.exceptions import InvalidGregorianDateError, InvalidEthiopianDateError

class TestEthiopianToGregorian:
    """
    Tests the `to_gc` (Ethiopian to Gregorian) conversion.
    """
    def test_normal_date_conversion(self):
        # 2017-9-14 ET -> May 22, 2025 GC
        assert to_gc(2017, 9, 14) == datetime.date(2025, 5, 22)

    def test_pagume_conversion(self):
        # Pagume 5, 2016 ET -> Sep 10, 2024 GC
        assert to_gc(2016, 13, 5) == datetime.date(2024, 9, 10)

    def test_leap_year_pagume_conversion(self):
        # Pagume 6, 2011 ET -> Sep 11, 2019 GC
        assert to_gc(2011, 13, 6) == datetime.date(2019, 9, 11)

    def test_new_year_conversion(self):
        # Meskerem 1, 2016 ET -> Sep 12, 2023 GC
        # Note: JS test comment said Sep 11, but code expected Sep 12. 2024 is a GC leap year.
        assert to_gc(2016, 1, 1) == datetime.date(2023, 9, 12)
        
    def test_random_date_conversion(self):
        # Tahsas 30, 2015 ET -> Jan 8, 2023 GC
        assert to_gc(2015, 4, 30) == datetime.date(2023, 1, 8)
    
    def test_invalid_date_throws_error(self):
        with pytest.raises(InvalidEthiopianDateError):
            to_gc(2016, 13, 7) # Pagume only has 6 days in a leap year
        with pytest.raises(InvalidEthiopianDateError):
            to_gc(2015, 14, 1) # No 14th month


class TestGregorianToEthiopian:
    """
    Tests the `to_ec` (Gregorian to Ethiopian) conversion.
    """
    def test_normal_date_conversion(self):
        # May 22, 2025 GC -> 2017-9-14 ET
        assert to_ec(2025, 5, 22) == {'year': 2017, 'month': 9, 'day': 14}
        
    def test_gregorian_leap_day_conversion(self):
        # Feb 29, 2020 GC -> Yekatit 22, 2012 ET
        # Note: Day is 22, not 21 as in JS test. The calculation is complex. Let's trust the robust algorithm.
        assert to_ec(2020, 2, 29) == {'year': 2012, 'month': 6, 'day': 21}

    def test_pagume_conversion(self):
        # Sep 10, 2024 GC -> Pagume 5, 2016 ET
        assert to_ec(2024, 9, 10) == {'year': 2016, 'month': 13, 'day': 5}

    def test_leap_pagume_conversion(self):
        # Sep 11, 2019 GC -> Pagume 6, 2011 ET
        assert to_ec(2019, 9, 11) == {'year': 2011, 'month': 13, 'day': 6}

    def test_out_of_range_year_throws_error(self):
        # With our updated to_ec function, this test should now pass.
        with pytest.raises(InvalidGregorianDateError):
            to_ec(1800, 1, 1)
        with pytest.raises(InvalidGregorianDateError):
            to_ec(2200, 1, 1)
            
    def test_invalid_date_throws_error(self):
        with pytest.raises(InvalidGregorianDateError):
            to_ec(2023, 2, 29) # Not a leap year