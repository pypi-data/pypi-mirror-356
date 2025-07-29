from . import holidays
from .geez_converter import to_geez
from .constants import DAYS_OF_WEEK, MONTH_NAMES
from .utils import get_weekday, validate_numeric_inputs
from .exceptions import InvalidGridConfigError

class MonthGrid:
    def __init__(self, config=None):
        from .kenat import Kenat
        if config is None:
            config = {}
        self._validate_config(config)

        current = Kenat.now()
        self.year = config.get('year', current.year)
        self.month = config.get('month', current.month)
        self.week_start = config.get('week_start', 1)
        self.use_geez = config.get('use_geez', False)
        self.weekday_lang = config.get('weekday_lang', 'amharic')
        self.holiday_filter = config.get('holiday_filter', None)

    def _validate_config(self, config):
        """Validates the configuration dictionary."""
        year = config.get('year')
        month = config.get('month')
        week_start = config.get('week_start')
        weekday_lang = config.get('weekday_lang')

        if (year is not None and month is None) or (year is None and month is not None):
            raise InvalidGridConfigError('If providing year or month, both must be provided.')
        if year is not None: validate_numeric_inputs('MonthGrid.constructor', year=year)
        if month is not None: validate_numeric_inputs('MonthGrid.constructor', month=month)
        if week_start is not None:
            validate_numeric_inputs('MonthGrid.constructor', week_start=week_start)
            if not 0 <= week_start <= 6: #
                raise InvalidGridConfigError(f"Invalid week_start value: {week_start}. Must be 0-6.")

        if weekday_lang is not None and weekday_lang not in DAYS_OF_WEEK:
            raise InvalidGridConfigError(f"Invalid weekday_lang: '{weekday_lang}'.")

    @classmethod
    def create(cls, year, month, **options):
        """Creates an instance and generates the grid in one call."""
        config = {'year': year, 'month': month, **options}
        instance = cls(config)
        return instance.generate()

    def generate(self):
        """Generates and returns the structured month grid."""
        from .kenat import Kenat
        y, m = self.year, self.month
        today_eth = Kenat.now()._ethiopian
        
        # Get the raw list of days for the month
        temp = Kenat(year=y, month=m, day=1)
        raw_days = temp.get_month_calendar(y, m, self.use_geez)
        
        # Get language-specific labels
        labels = DAYS_OF_WEEK.get(self.weekday_lang, DAYS_OF_WEEK['amharic'])
        month_labels = MONTH_NAMES.get(self.weekday_lang, MONTH_NAMES['amharic'])

        # Fetch holidays and map them by day for quick lookup
        month_holidays = holidays.get_holidays_in_month(y, m, lang=self.weekday_lang, filter_by=self.holiday_filter)
        holiday_map = {}
        for h in month_holidays:
            day_key = h['ethiopian']['day']
            if day_key not in holiday_map: holiday_map[day_key] = []
            holiday_map[day_key].append(h)
        
        # Enrich each day with additional information
        days_with_weekday = []
        for day_data in raw_days:
            eth = day_data['ethiopian']
            is_today = (eth['year'] == today_eth['year'] and
                        eth['month'] == today_eth['month'] and
                        eth['day'] == today_eth['day'])
            weekday = get_weekday(eth)
            
            days_with_weekday.append({
                'ethiopian': {
                    'year': to_geez(eth['year']) if self.use_geez else eth['year'],
                    'month': month_labels[eth['month'] - 1],
                    'day': to_geez(eth['day']) if self.use_geez else eth['day']
                },
                'gregorian': day_data['gregorian'],
                'weekday': weekday,
                'weekday_name': labels[weekday],
                'is_today': is_today,
                'holidays': holiday_map.get(eth['day'], [])
            })

        # Pad the beginning of the list with 'None' for empty days
        offset = (days_with_weekday[0]['weekday'] - self.week_start + 7) % 7
        padded_days = ([None] * offset) + days_with_weekday
        
        # Reorder headers based on week_start
        headers = labels[self.week_start:] + labels[:self.week_start]
        
        # Structure the final output
        return {
            'headers': headers,
            'days': [padded_days[i:i + 7] for i in range(0, len(padded_days), 7)],
            'year': to_geez(self.year) if self.use_geez else self.year,
            'month': self.month,
            'month_name': month_labels[self.month - 1]
        }