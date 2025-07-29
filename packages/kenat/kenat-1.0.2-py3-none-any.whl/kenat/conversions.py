import datetime
import math
from .utils import (
    is_gregorian_leap_year,
    is_ethiopian_leap_year,
    get_ethiopian_days_in_month,
    validate_numeric_inputs
)
from .exceptions import InvalidEthiopianDateError, InvalidGregorianDateError, KenatError


def to_gc(eth_year, eth_month, eth_day):
    """
    Converts an Ethiopian date to its corresponding Gregorian date.

    Args:
        eth_year (int): The Ethiopian year.
        eth_month (int): The Ethiopian month (1-13).
        eth_day (int): The Ethiopian day.

    Returns:
        datetime.date: The equivalent Gregorian date object.
    """
    # 1. Validate input types and date range 
    validate_numeric_inputs('to_gc', eth_year=eth_year, eth_month=eth_month, eth_day=eth_day)
    if not 1 <= eth_month <= 13 or not 1 <= eth_day <= get_ethiopian_days_in_month(eth_year, eth_month):
        raise InvalidEthiopianDateError(eth_year, eth_month, eth_day)

    # 2. Determine the Gregorian date of the Ethiopian New Year 
    gregorian_year = eth_year + 7
    new_year_day = 12 if is_gregorian_leap_year(gregorian_year + 1) else 11
    new_year_date = datetime.date(gregorian_year, 9, new_year_day)

    # 3. Calculate days elapsed since the Ethiopian new year and add to the new year date 
    days_to_add = (eth_month - 1) * 30 + (eth_day - 1)
    
    return new_year_date + datetime.timedelta(days=days_to_add)

def to_ec(greg_year, greg_month, greg_day):
    """
    Converts a Gregorian date to the Ethiopian calendar (EC) date.
    """
    # 1. Validate input types
    validate_numeric_inputs('to_ec', g_year=greg_year, g_month=greg_month, g_day=greg_day)
    
    # 2. Validate date validity and range (1900-2100) to match original library
    try:
        greg_date = datetime.date(greg_year, greg_month, greg_day)
        if not (datetime.date(1900, 1, 1) <= greg_date <= datetime.date(2100, 12, 31)):
             raise InvalidGregorianDateError(greg_year, greg_month, greg_day)
    except (ValueError, InvalidGregorianDateError): # Catch both invalid dates and out-of-range
        raise InvalidGregorianDateError(greg_year, greg_month, greg_day)

    # 3. Determine the corresponding Ethiopian year
    eth_year = greg_year - 8
    greg_of_eth_new_year = to_gc(eth_year + 1, 1, 1)
    if greg_date >= greg_of_eth_new_year:
        eth_year += 1

    # 4. Calculate the difference in days from that Ethiopian New Year
    new_year_greg_date = to_gc(eth_year, 1, 1)
    days_diff = (greg_date - new_year_greg_date).days
    
    # 5. Convert the day difference into Ethiopian month and day
    eth_month = (days_diff // 30) + 1
    eth_day = (days_diff % 30) + 1
    
    return {'year': eth_year, 'month': eth_month, 'day': eth_day}

def _gregorian_to_jd(year, month, day):
    """Converts a Gregorian date to Julian Day Number."""
    if month < 3:
        year -= 1
        month += 12
    a = year // 100
    b = a // 4
    c = 2 - a + b
    e = int(365.25 * (year + 4716))
    f = int(30.6001 * (month + 1))
    return c + day + e + f - 1524

def _jd_to_gregorian(jd):
    """Converts a Julian Day Number to a Gregorian date."""
    q = jd + 0.5
    z = int(q)
    w = (z - 1867216.25) / 36524.25
    x = w // 4
    a = z + 1 + w - x
    b = a + 1524
    c = (b - 122.1) / 365.25
    d = int(c)
    e = int(365.25 * d)
    f = int((b - e) / 30.6001)
    day = b - e - int(30.6001 * f)
    month = f - 1 if f < 14 else f - 13
    year = d - 4716 if month > 2 else d - 4715
    return datetime.date(year, month, day)

def _hijri_to_jd(year, month, day):
    """Converts a Hijri date to Julian Day Number."""
    # This is the corrected formula for the Tabular Islamic Calendar.
    return int((11 * year + 3) / 30) + 354 * year + 30 * month - int((month - 1) / 2) + day + 1948440 - 385

def _jd_to_hijri(jd):
    """Converts a Julian Day Number to a Hijri date using the tabular Islamic calendar."""
    jd = math.floor(jd) + 0.5  # Ensure it's at start of day
    jd = jd - 1948439.5
    year = int((30 * jd + 10646) // 10631)
    start_of_year = 354 * (year - 1) + math.floor((3 + 11 * year) / 30)
    day_of_year = int(jd - start_of_year)
    month = int((day_of_year) // 29.5) + 1
    if month > 12:
        month = 12
    start_of_month = 29.5 * (month - 1)
    day = int(jd - (start_of_year + start_of_month)) + 1
    return {'year': year, 'month': month, 'day': day}

def hijri_to_gregorian(h_year, h_month, h_day, gregorian_year):
    """
    Converts a Hijri date to a Gregorian date by searching within a given Gregorian year.
    This mimics the brute-force search methodology of the original JavaScript code.
    """
    # Start searching from the beginning of the previous Gregorian year to be safe.
    base_date = datetime.date(gregorian_year - 1, 1, 1)

    # Search for up to 730 days (2 years) to guarantee finding the date.
    for offset in range(731):
        test_date = base_date + datetime.timedelta(days=offset)

        # For each day, find its corresponding Hijri date using our JDN functions.
        jd = _gregorian_to_jd(test_date.year, test_date.month, test_date.day)
        hijri_parts = _jd_to_hijri(jd)

        # Check if we have a match for the target date within the target year.
        if (
            hijri_parts['year'] == h_year and
            hijri_parts['month'] == h_month and
            hijri_parts['day'] == h_day and
            test_date.year == gregorian_year
        ):
            return test_date  # Found it!

    return None

def get_hijri_year(greg_date):
    """Gets the Hijri year from a Gregorian date object."""
    jd = _gregorian_to_jd(greg_date.year, greg_date.month, greg_date.day)
    return _jd_to_hijri(jd)['year']
