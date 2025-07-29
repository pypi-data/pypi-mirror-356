import json
import datetime
from . import conversions, bahire_hasab
from .constants import (
    FIXED_HOLIDAYS,
    MOVABLE_HOLIDAYS,
    HOLIDAY_INFO,
    KEY_TO_TEWSAK_MAP
)
from .utils import validate_numeric_inputs
from .exceptions import InvalidInputTypeError

def _find_all_islamic_occurrences(ethiopian_year, hijri_month, hijri_day):
    """
    Finds all occurrences of an Islamic date within an Ethiopian year.
    This version is a faithful port of the original JS logic.
    """
    start_gc = conversions.to_gc(ethiopian_year, 1, 1)
    end_gc = conversions.to_gc(ethiopian_year, 13, 5)
    
    occurrences = []
    
    # Check both the Gregorian year of the start and end of the Ethiopian year
    for g_year in range(start_gc.year, end_gc.year + 1):
        # Get the Hijri year at the start of this Gregorian year
        hijri_year_at_start = conversions.get_hijri_year(datetime.date(g_year, 1, 1))
        
        # An Islamic date can only fall in one of two Hijri years for a given Gregorian year
        for h_year in [hijri_year_at_start, hijri_year_at_start + 1]:
            # Use our new search-based conversion function
            greg_date = conversions.hijri_to_gregorian(h_year, hijri_month, hijri_day, g_year)
            
            if greg_date: # If a date was found
                ec_date = conversions.to_ec(greg_date.year, greg_date.month, greg_date.day)
                if ec_date['year'] == ethiopian_year:
                    occurrences.append({
                        'gregorian': {'year': greg_date.year, 'month': greg_date.month, 'day': greg_date.day},
                        'ethiopian': ec_date
                    })
                
    # Remove duplicates
    return list({json.dumps(item['ethiopian']): item for item in occurrences}.values())

_get_all_moulid_dates = lambda year: _find_all_islamic_occurrences(year, 3, 12)
_get_all_eid_fitr_dates = lambda year: _find_all_islamic_occurrences(year, 10, 1)
_get_all_eid_adha_dates = lambda year: _find_all_islamic_occurrences(year, 12, 10)

def get_holiday(holiday_key, eth_year, lang='amharic'):
    """Gets details for a single holiday for a given year."""
    validate_numeric_inputs('get_holiday', eth_year=eth_year)
    info = HOLIDAY_INFO.get(holiday_key)
    if not info:
        return None
        
    name = info.get('name', {}).get(lang) or info.get('name', {}).get('english')
    description = info.get('description', {}).get(lang) or info.get('description', {}).get('english')

    if holiday_key in FIXED_HOLIDAYS:
        rules = FIXED_HOLIDAYS[holiday_key]
        return {
            'key': holiday_key, 'tags': rules.get('tags', []), 'movable': False,
            'name': name, 'description': description,
            'ethiopian': {'year': eth_year, 'month': rules['month'], 'day': rules['day']}
        }

    tewsak_key = KEY_TO_TEWSAK_MAP.get(holiday_key)
    if tewsak_key:
        date = bahire_hasab.get_movable_holiday(tewsak_key, eth_year)
        gregorian = conversions.to_gc(date['year'], date['month'], date['day'])
        return {
            'key': holiday_key, 'tags': MOVABLE_HOLIDAYS.get(holiday_key, {}).get('tags', []), 'movable': True,
            'name': name, 'description': description, 'ethiopian': date, 
            'gregorian': {'year': gregorian.year, 'month': gregorian.month, 'day': gregorian.day}
        }

    all_dates = []
    if holiday_key == 'eidFitr': all_dates = _get_all_eid_fitr_dates(eth_year)
    elif holiday_key == 'eidAdha': all_dates = _get_all_eid_adha_dates(eth_year)
    elif holiday_key == 'moulid': all_dates = _get_all_moulid_dates(eth_year)
    
    if all_dates:
        data = all_dates[0]
        return {
            'key': holiday_key, 'tags': MOVABLE_HOLIDAYS.get(holiday_key, {}).get('tags', []), 'movable': True,
            'name': name, 'description': description, 'ethiopian': data['ethiopian'], 'gregorian': data['gregorian']
        }
    
    return None

def get_holidays_in_month(eth_year, eth_month, lang='amharic', filter_by=None):
    """Gets all holidays for a given Ethiopian month."""
    validate_numeric_inputs("get_holidays_in_month", eth_year=eth_year, eth_month=eth_month)
    if not 1 <= eth_month <= 13:
        raise InvalidInputTypeError("get_holidays_in_month", "eth_month", "number between 1 and 13", eth_month)

    all_holidays_for_month = []
    
    for key in HOLIDAY_INFO.keys():
        holiday = get_holiday(key, eth_year, lang)
        if holiday and holiday['ethiopian']['month'] == eth_month:
            all_holidays_for_month.append(holiday)

    muslim_holidays_data = {
        'moulid': _get_all_moulid_dates(eth_year),
        'eidFitr': _get_all_eid_fitr_dates(eth_year),
        'eidAdha': _get_all_eid_adha_dates(eth_year),
    }

    for key, dates in muslim_holidays_data.items():
        for data in dates:
            if data['ethiopian']['month'] == eth_month:
                is_duplicate = any(
                    json.dumps(h['ethiopian']) == json.dumps(data['ethiopian'])
                    for h in all_holidays_for_month
                )
                if not is_duplicate:
                    info = HOLIDAY_INFO[key]
                    all_holidays_for_month.append({
                        'key': key, 'tags': MOVABLE_HOLIDAYS[key]['tags'], 'movable': True,
                        'name': info.get('name', {}).get(lang) or info.get('name', {}).get('english'),
                        'description': info.get('description', {}).get(lang) or info.get('description', {}).get('english'),
                        'ethiopian': data['ethiopian'], 'gregorian': data['gregorian'],
                    })

    filter_tags = filter_by if isinstance(filter_by, list) else ([filter_by] if filter_by else None)
    final_holidays = all_holidays_for_month
    if filter_tags:
        final_holidays = [h for h in all_holidays_for_month if any(tag in h.get('tags', []) for tag in filter_tags)]
    
    final_holidays.sort(key=lambda x: x['ethiopian']['day'])
    return final_holidays

# --- THIS FUNCTION WAS MISSING AND IS NOW ADDED ---
def get_holidays_for_year(eth_year, lang='amharic', filter_by=None):
    """Gets all holidays for a given Ethiopian year."""
    validate_numeric_inputs('get_holidays_for_year', eth_year=eth_year)
    all_holidays_for_year = []

    # Process all fixed and Christian movable holidays 
    single_occurrence_keys = list(FIXED_HOLIDAYS.keys()) + list(KEY_TO_TEWSAK_MAP.keys())
    for key in single_occurrence_keys:
        holiday = get_holiday(key, eth_year, lang)
        if holiday:
            all_holidays_for_year.append(holiday)
    
    # Process all occurrences of Islamic holidays 
    def add_muslim_holidays(key, date_array):
        for data in date_array:
            info = HOLIDAY_INFO[key]
            all_holidays_for_year.append({
                'key': key,
                'tags': MOVABLE_HOLIDAYS[key]['tags'],
                'movable': True,
                'name': info.get('name', {}).get(lang) or info.get('name', {}).get('english'),
                'description': info.get('description', {}).get(lang) or info.get('description', {}).get('english'),
                'ethiopian': data['ethiopian'],
                'gregorian': data['gregorian'],
            })

    add_muslim_holidays('moulid', _get_all_moulid_dates(eth_year))
    add_muslim_holidays('eidFitr', _get_all_eid_fitr_dates(eth_year))
    add_muslim_holidays('eidAdha', _get_all_eid_adha_dates(eth_year))

    # Filter and sort the final list
    filter_tags = filter_by if isinstance(filter_by, list) else ([filter_by] if filter_by else None)
    final_holidays = all_holidays_for_year
    if filter_tags:
        final_holidays = [h for h in all_holidays_for_year if any(tag in h.get('tags', []) for tag in filter_tags)]
        
    final_holidays.sort(key=lambda x: (x['ethiopian']['month'], x['ethiopian']['day']))
    return final_holidays
