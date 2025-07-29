import pytest
from kenat import Kenat
from kenat.time import Time
from kenat.exceptions import InvalidTimeError, InvalidInputTypeError

class TestTimeConstructor:
    def test_should_create_valid_time_object(self):
        time = Time(3, 30, 'day')
        assert time.hour == 3
        assert time.minute == 30
        assert time.period == 'day'

    def test_should_throw_for_out_of_range_values(self):
        with pytest.raises(InvalidTimeError): Time(0, 0, 'day')
        with pytest.raises(InvalidTimeError): Time(13, 0, 'day')
        with pytest.raises(InvalidTimeError): Time(5, -1, 'day')
        with pytest.raises(InvalidTimeError): Time(5, 60, 'day')
        with pytest.raises(InvalidTimeError): Time(5, 0, 'morning')
        
    def test_should_throw_for_non_numeric_inputs(self):
        with pytest.raises(InvalidInputTypeError): Time('three', 30)
        with pytest.raises(InvalidInputTypeError): Time(3, 'thirty')

class TestTimeFromString:
    def test_should_parse_valid_strings(self):
        assert Time.from_string('10:30 day') == Time(10, 30, 'day')
        assert Time.from_string('5:00 night') == Time(5, 0, 'night')
        assert Time.from_string('፫:፲፭ ማታ') == Time(3, 15, 'night')
        assert Time.from_string('፲፪:፴ day') == Time(12, 30, 'day')

    def test_should_default_to_day_period(self):
        assert Time.from_string('11:45') == Time(11, 45, 'day')

    def test_should_throw_for_malformed_strings(self):
        with pytest.raises(InvalidTimeError): Time.from_string('10')
        with pytest.raises(InvalidTimeError): Time.from_string('')
        with pytest.raises(InvalidTimeError): Time.from_string('10 30')

class TestTimeConversion:
    @pytest.mark.parametrize("g_hour, g_minute, expected", [
        (7, 30, Time(1, 30, 'day')),
        (18, 0, Time(12, 0, 'night')),
        (0, 0, Time(6, 0, 'night')),
        (6, 0, Time(12, 0, 'day')),
    ])
    def test_from_gregorian(self, g_hour, g_minute, expected):
        assert Time.from_gregorian(g_hour, g_minute) == expected

    @pytest.mark.parametrize("eth_time, expected", [
        (Time(1, 30, 'day'), {'hour': 7, 'minute': 30}),
        (Time(12, 0, 'night'), {'hour': 18, 'minute': 0}),
        (Time(6, 0, 'night'), {'hour': 0, 'minute': 0}),
        (Time(12, 0, 'day'), {'hour': 6, 'minute': 0}),
    ])
    def test_to_gregorian(self, eth_time, expected):
        assert eth_time.to_gregorian() == expected

class TestTimeArithmetic:
    start_time = Time(3, 15, 'day') # 9:15 AM

    def test_add_simple(self):
        new_time = self.start_time.add({'hours': 2, 'minutes': 10})
        assert new_time == Time(5, 25, 'day') # 11:25 AM

    def test_add_rolls_over_period(self):
        new_time = self.start_time.add({'hours': 9}) # 9:15 AM + 9hr = 6:15 PM
        assert new_time == Time(12, 15, 'night')

    def test_subtract_simple(self):
        new_time = self.start_time.subtract({'hours': 1, 'minutes': 15})
        assert new_time == Time(2, 0, 'day') # 8:00 AM
        
    def test_subtract_rolls_back_period(self):
        time = Time(1, 0, 'day') # 7:00 AM
        new_time = time.subtract({'hours': 2}) # 7:00 AM - 2hr = 5:00 AM
        assert new_time == Time(11, 0, 'night')
        
    def test_diff(self):
        end_time = Time(5, 45, 'day')
        assert self.start_time.diff(end_time) == {'hours': 2, 'minutes': 30}
        
    def test_diff_across_wrap(self):
        t1 = Time(2, 0, 'night') # 8 PM
        t2 = Time(10, 0, 'night') # 4 AM
        assert t1.diff(t2) == {'hours': 8, 'minutes': 0}

class TestTimeFormatting:
    def test_format_default_options(self):
        time = Time(5, 30, 'day')
        assert time.format() == '፭:፴ ጠዋት'

    def test_format_with_arabic_numerals(self):
        time = Time(5, 30, 'day')
        assert time.format(use_geez=False) == '05:30 day'

    def test_format_without_period_label(self):
        time = Time(8, 15, 'night')
        assert time.format(use_geez=False, show_period=False) == '08:15'
        
    def test_format_with_dash_for_zero(self):
        time = Time(12, 0, 'day')
        assert time.format(use_geez=False, zero_as_dash=True) == '12:_ day'