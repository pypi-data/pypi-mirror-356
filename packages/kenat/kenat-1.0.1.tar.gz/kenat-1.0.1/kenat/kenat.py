import datetime
from .geez_converter import to_geez
from . import (
    conversions,
    holidays,
    day_arithmetic,
    formatting,
    bahire_hasab,
    utils
)
from .time import Time
from .exceptions import UnrecognizedInputError, InvalidDateFormatError, InvalidEthiopianDateError

class Kenat:
    """
    A class to represent and manipulate Ethiopian calendar dates. It serves as
    a wrapper for an Ethiopian date, providing conversion, formatting, and
    arithmetic functionalities.
    """
    def __init__(self, year=None, month=None, day=None, time_obj=None):
        """
        Constructs a Kenat instance. Can be initialized with:
         - An Ethiopian date string (e.g., '2016/1/1', '2016-1-1'). 
         - A dictionary with {'year', 'month', 'day'}. 
         - A native Python datetime.date or datetime.datetime object. 
         - No arguments, for the current date. 
         - Year, month, day as separate integer arguments.
        """
        # Default to current date and time if no input is provided 
        if year is None:
            today_greg = datetime.datetime.now()
            self._ethiopian = conversions.to_ec(today_greg.year, today_greg.month, today_greg.day)
            self._time = Time.from_gregorian(today_greg.hour, today_greg.minute)
        
        # From a datetime object 
        elif isinstance(year, (datetime.datetime, datetime.date)):
            self._ethiopian = conversions.to_ec(year.year, year.month, year.day)
            self._time = Time.from_gregorian(year.hour, year.minute) if isinstance(year, datetime.datetime) else Time(12, 0, 'day')

        # From a dictionary {'year', 'month', 'day'} 
        elif isinstance(year, dict):
            self._ethiopian = year
            self._time = time_obj if isinstance(time_obj, Time) else Time(12, 0, 'day')

        # From a string 'YYYY/MM/DD' or 'YYYY-MM-DD' 
        elif isinstance(year, str):
            try:
                parts = list(map(int, year.replace('/', '-').split('-')))
                self._ethiopian = {'year': parts[0], 'month': parts[1], 'day': parts[2]}
                self._time = time_obj if isinstance(time_obj, Time) else Time(12, 0, 'day')
            except (ValueError, IndexError):
                raise InvalidDateFormatError(year)
        
        # From year, month, day integers
        elif isinstance(year, int) and month is not None and day is not None:
            self._ethiopian = {'year': year, 'month': month, 'day': day}
            self._time = time_obj if isinstance(time_obj, Time) else Time(12, 0, 'day')
            
        else:
            raise UnrecognizedInputError(year)

        # Final validation
        if not utils.is_valid_ethiopian_date(self.year, self.month, self.day):
            raise InvalidEthiopianDateError(self.year, self.month, self.day)

    @classmethod
    def now(cls):
        """Creates and returns a new Kenat instance for the current date and time."""
        return cls()

    # --- Properties ---
    @property
    def year(self):
        return self._ethiopian['year']

    @property
    def month(self):
        return self._ethiopian['month']
        
    @property
    def day(self):
        return self._ethiopian['day']

    @property
    def time(self):
        return self._time
        
    def to_gregorian_date(self):
        """Returns the Gregorian date as a Python datetime.date object."""
        return conversions.to_gc(self.year, self.month, self.day)

    # --- Information Methods ---
    def get_bahire_hasab(self, lang='amharic'):
        """Calculates and returns the Bahire Hasab values for the current instance's year."""
        return bahire_hasab.get_bahire_hasab(self.year, lang)

    def is_holiday(self, lang='amharic'):
        """Checks if the current date is a holiday and returns a list of holiday objects if it is."""
        holidays_in_month = holidays.get_holidays_in_month(self.year, self.month, lang) 
        return [h for h in holidays_in_month if h['ethiopian']['day'] == self.day]

    def is_leap_year(self):
        """Checks if the current Ethiopian year is a leap year."""
        return utils.is_ethiopian_leap_year(self.year)

    def weekday(self):
        """Returns the weekday number (0 for Sunday, 6 for Saturday)."""
        return utils.get_weekday(self._ethiopian)

    # --- Formatting Methods ---
    def format(self, options=None):
        """
        Formats the Ethiopian date according to the specified options.
        Options is a dict: {'lang', 'show_weekday', 'use_geez', 'include_time'}
        """
        if options is None:
            options = {}
        lang = options.get('lang', 'amharic')
        show_weekday = options.get('show_weekday', False)
        use_geez = options.get('use_geez', False)
        include_time = options.get('include_time', False)

        if use_geez:
             return formatting.format_in_geez_amharic(self._ethiopian)
        if show_weekday:
            return formatting.format_with_weekday(self._ethiopian, lang)
        if include_time:
            return formatting.format_with_time(self._ethiopian, self._time, lang)
        
        return formatting.format_standard(self._ethiopian, lang)
    
    def get_ethiopian(self):
        """Returns the Ethiopian date as a dictionary."""
        return self._ethiopian

    def get_gregorian(self):
        """Returns the Gregorian date as a dictionary, for test compatibility."""
        greg_date = self.to_gregorian_date()
        return {'year': greg_date.year, 'month': greg_date.month, 'day': greg_date.day}

    def to_string(self):
        """Returns a specific string format matching the original JS toString()."""
        # This format includes the default time.
        return formatting.format_with_time(self._ethiopian, self._time)
        
    def format_in_geez_amharic(self):
        """Formats the date with Amharic month and Geez numerals."""
        return formatting.format_in_geez_amharic(self._ethiopian)

    def is_before(self, other):
        """Checks if this date is before another Kenat instance."""
        if not isinstance(other, Kenat):
            raise TypeError("Can only compare with another Kenat instance.")
        return self.diff_in_days(other) < 0

    def is_after(self, other):
        """Checks if this date is after another Kenat instance."""
        if not isinstance(other, Kenat):
            raise TypeError("Can only compare with another Kenat instance.")
        return self.diff_in_days(other) > 0

    def is_same_day(self, other):
        """Checks if this date is the same as another Kenat instance."""
        if not isinstance(other, Kenat):
            return False
        return self.diff_in_days(other) == 0

    def start_of_month(self):
        """Returns a new Kenat instance set to the first day of the current month."""
        return Kenat(year=self.year, month=self.month, day=1)

    def end_of_month(self):
        """Returns a new Kenat instance set to the last day of the current month."""
        last_day = utils.get_ethiopian_days_in_month(self.year, self.month)
        return Kenat(year=self.year, month=self.month, day=last_day)

    # --- Arithmetic Methods ---
    def add(self, years=0, months=0, days=0):
        """Returns a new Kenat instance with the added duration."""
        new_date = self._ethiopian
        if years:
            new_date = day_arithmetic.add_years(new_date, years)
        if months:
            new_date = day_arithmetic.add_months(new_date, months)
        if days:
            new_date = day_arithmetic.add_days(new_date, days)
        return Kenat(year=new_date)

    def diff_in_days(self, other):
        """Calculates the difference in days between this and another Kenat instance."""
        return day_arithmetic.diff_in_days(self._ethiopian, other._ethiopian) 

    # --- Calendar Grid Generation ---
    @staticmethod
    def get_year_calendar(year, options=None):
        from .month_grid import MonthGrid
        """Generates a full-year calendar as a list of month objects.""" 
        if options is None: options = {}
        full_year = []
        for month in range(1, 14):
            # Create a MonthGrid for each month and append its data
            month_grid = MonthGrid.create(year=year, month=month, **options)
            full_year.append(month_grid)
        return full_year
    
    def get_current_time(self):
        """Returns a Time object representing the current Ethiopian time."""
        now = datetime.datetime.now()
        return Time.from_gregorian(now.hour, now.minute)

    def get_month_calendar(self, year=None, month=None, use_geez=False):
        """
        Generates a simple calendar for a given month, mapping each Ethiopian day
        to its Gregorian equivalent, including display strings.
        """
        # These local imports are fine.
        from .constants import MONTH_NAMES
        from .geez_converter import to_geez
        from . import utils, conversions

        year = year or self.year
        month = month or self.month
        days_in_month = utils.get_ethiopian_days_in_month(year, month)
        calendar = []

        for day in range(1, days_in_month + 1):
            eth_date = {'year': year, 'month': month, 'day': day}
            greg_date = conversions.to_gc(year, month, day) # This returns a datetime.date object

            ethiopian_display = ""
            if use_geez:
                ethiopian_display = f"{MONTH_NAMES['amharic'][month - 1]} {to_geez(day)} {to_geez(year)}"
            else:
                ethiopian_display = f"{MONTH_NAMES['amharic'][month - 1]} {day} {year}"

            # --- THIS IS THE FIX ---
            # Use dot notation (.year, .month, .day) for the datetime.date object
            gregorian_display = f"{greg_date.year}-{str(greg_date.month).zfill(2)}-{str(greg_date.day).zfill(2)}"

            eth_date['display'] = ethiopian_display
            
            # We need to create the greg_date dict for the return value
            greg_date_dict = {
                'year': greg_date.year,
                'month': greg_date.month,
                'day': greg_date.day,
                'display': gregorian_display
            }
            
            calendar.append({
                'ethiopian': eth_date,
                'gregorian': greg_date_dict,
            })
        return calendar

    # --- Python Special Methods ---
    def __str__(self):
        """Returns a user-friendly string representation."""
        return self.format({'lang': 'english'})

    def __repr__(self):
        """Returns an unambiguous string representation of the object."""
        return f"Kenat(year={self.year}, month={self.month}, day={self.day})"

    def __eq__(self, other):
        """Checks for date equality."""
        if not isinstance(other, Kenat):
            return NotImplemented
        return self._ethiopian == other._ethiopian

    def __lt__(self, other):
        """Checks if this date is before another."""
        if not isinstance(other, Kenat):
            return NotImplemented
        return self.diff_in_days(other) < 0

    def __gt__(self, other):
        """Checks if this date is after another."""
        if not isinstance(other, Kenat):
            return NotImplemented
        return self.diff_in_days(other) > 0
