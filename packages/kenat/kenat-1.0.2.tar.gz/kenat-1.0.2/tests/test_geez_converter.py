# tests/test_geez_converter.py

import pytest
from kenat.geez_converter import to_geez, to_arabic
from kenat.exceptions import GeezConverterError

class TestToGeez:
    """Tests the to_geez (Arabic to Ethiopic numeral) function."""

    def test_converts_single_digits(self):
        assert to_geez(1) == '፩'
        assert to_geez(2) == '፪'
        assert to_geez(9) == '፱'

    def test_converts_tens(self):
        assert to_geez(10) == '፲'
        assert to_geez(20) == '፳'
        assert to_geez(99) == '፺፱'

    def test_converts_hundreds(self):
        assert to_geez(100) == '፻'
        assert to_geez(101) == '፻፩'
        assert to_geez(123) == '፻፳፫'
        assert to_geez(999) == '፱፻፺፱'

    def test_converts_thousands_and_ten_thousands(self):
        assert to_geez(1000) == '፲፻' # Ten-hundred
        assert to_geez(10000) == '፼'

    def test_returns_zero_string_for_input_zero(self):
        assert to_geez(0) == '0'

    def test_accepts_string_input(self):
        assert to_geez('123') == '፻፳፫'
        assert to_geez('10000') == '፼'

    @pytest.mark.parametrize("invalid_input", [-1, 1.5, 'abc', None, []])
    def test_throws_error_for_invalid_input(self, invalid_input):
        with pytest.raises(GeezConverterError):
            to_geez(invalid_input)


class TestToArabic:
    """Tests the to_arabic (Ethiopic numeral to Arabic) function."""

    def test_converts_single_geez_numerals(self):
        assert to_arabic('፩') == 1
        assert to_arabic('፪') == 2
        assert to_arabic('፱') == 9

    def test_converts_geez_tens(self):
        assert to_arabic('፲') == 10
        assert to_arabic('፳') == 20
        assert to_arabic('፺፱') == 99

    def test_converts_geez_hundreds(self):
        assert to_arabic('፻') == 100
        assert to_arabic('፻፩') == 101
        assert to_arabic('፻፳፫') == 123
        assert to_arabic('፱፻፺፱') == 999

    def test_converts_geez_thousands_and_ten_thousands(self):
        assert to_arabic('፲፻') == 1000
        assert to_arabic('፼') == 10000
        assert to_arabic('፲፼') == 100000

    def test_handles_complex_numbers(self):
        assert to_arabic('፲፻፺፱') == 1099
        assert to_arabic('፬፻') == 400

    def test_throws_error_for_unknown_geez_numerals(self):
        with pytest.raises(GeezConverterError, match="Unknown Ge'ez numeral: A"):
            to_arabic('A')
        with pytest.raises(GeezConverterError, match="Unknown Ge'ez numeral: X"):
            to_arabic('፩X')

    @pytest.mark.parametrize("invalid_input", [None, 123, 1.5, []])
    def test_throws_error_for_non_string_input(self, invalid_input):
        with pytest.raises(GeezConverterError):
            to_arabic(invalid_input)

    @pytest.mark.parametrize("number", [1, 10, 99, 100, 123, 999, 1000, 10000, 12345, 999999])
    def test_round_trip_conversion(self, number):
        """Tests that to_arabic(to_geez(n)) == n."""
        geez_representation = to_geez(number)
        assert to_arabic(geez_representation) == number
