from .utils import validate_numeric_inputs, get_weekday
from .day_arithmetic import add_days
from .conversions import to_gc
from .exceptions import UnknownHolidayError
from .constants import (
    DAYS_OF_WEEK,
    EVANGELIST_NAMES,
    TEWSAK_MAP,
    MOVABLE_HOLIDAY_TEWSAK,
    KEY_TO_TEWSAK_MAP,
    HOLIDAY_INFO,
    MOVABLE_HOLIDAYS
)

def _calculate_bahire_hasab_base(ethiopian_year):
    """
    Calculates and returns all base values for the Bahire Hasab system. 
    This internal helper is the single source of truth for the core computational logic. 
    """
    amete_alem = 5500 + ethiopian_year  
    metene_rabiet = amete_alem // 4  
    medeb = amete_alem % 19  
    wenber = 18 if medeb == 0 else medeb - 1  
    abektie = (wenber * 11) % 30  
    metqi = (wenber * 19) % 30  

    beale_metqi_month = 1 if metqi > 14 else 2  
    beale_metqi_day = metqi  
    beale_metqi_date = {'year': ethiopian_year, 'month': beale_metqi_month, 'day': beale_metqi_day}  
    
    beale_metqi_weekday = DAYS_OF_WEEK['english'][get_weekday(beale_metqi_date)]  
    tewsak = TEWSAK_MAP[beale_metqi_weekday]  
    
    mebaja_hamer_sum = beale_metqi_day + tewsak  
    mebaja_hamer = mebaja_hamer_sum % 30 if mebaja_hamer_sum > 30 else mebaja_hamer_sum  
    
    nineveh_month = 5 if metqi > 14 else 6  
    if mebaja_hamer_sum > 30:  
        nineveh_month += 1  
        
    nineveh_date = {'year': ethiopian_year, 'month': nineveh_month, 'day': mebaja_hamer}  
    
    return {  
        'amete_alem': amete_alem,  
        'metene_rabiet': metene_rabiet,  
        'medeb': medeb,  
        'wenber': wenber,  
        'abektie': abektie,  
        'metqi': metqi,  
        'beale_metqi_date': beale_metqi_date,  
        'beale_metqi_weekday': beale_metqi_weekday,  
        'mebaja_hamer': mebaja_hamer,  
        'nineveh_date': nineveh_date,  
    }

def get_bahire_hasab(ethiopian_year, lang='amharic'):
    """
    Calculates all Bahire Hasab values for a given Ethiopian year. 

    Args:
        ethiopian_year (int): The Ethiopian year to calculate for.
        lang (str): The language for names ('amharic' or 'english'). 

    Returns:
        dict: An object containing all the calculated Bahire Hasab values. 
    """
    validate_numeric_inputs('get_bahire_hasab', ethiopian_year=ethiopian_year)  
    
    base = _calculate_bahire_hasab_base(ethiopian_year)  


    evangelist_remainder = base['amete_alem'] % 4  
    evangelist_name = EVANGELIST_NAMES.get(lang, EVANGELIST_NAMES['english'])[evangelist_remainder]  

    tinte_qemer = (base['amete_alem'] + base['metene_rabiet']) % 7  
    weekday_index = (tinte_qemer + 1) % 7  
    new_year_weekday = DAYS_OF_WEEK.get(lang, DAYS_OF_WEEK['english'])[weekday_index]  

    movable_feasts = {}  
    tewsak_to_key_map = {v: k for k, v in KEY_TO_TEWSAK_MAP.items()}  
    
    for tewsak_key, tewsak_value in MOVABLE_HOLIDAY_TEWSAK.items():  
        holiday_key = tewsak_to_key_map.get(tewsak_key)  
        if holiday_key:  
            date = add_days(base['nineveh_date'], tewsak_value)  
            info = HOLIDAY_INFO.get(holiday_key, {})  
            rules = MOVABLE_HOLIDAYS.get(holiday_key, {})  
            
            movable_feasts[holiday_key] = {  
                'key': holiday_key,  
                'tags': rules.get('tags', []),  
                'movable': True,  
                'name': info.get('name', {}).get(lang) or info.get('name', {}).get('english'),  
                'description': info.get('description', {}).get(lang) or info.get('description', {}).get('english'),  
                'ethiopian': date,  
                'gregorian': to_gc(date['year'], date['month'], date['day'])  
            }

    return {  
        'ameteAlem': base['amete_alem'],
        'meteneRabiet': base['metene_rabiet'],
        'evangelist': {'name': evangelist_name, 'remainder': evangelist_remainder},
        'newYear': {'dayName': new_year_weekday, 'tinteQemer': tinte_qemer},
        'medeb': base['medeb'],
        'wenber': base['wenber'],
        'abektie': base['abektie'],
        'metqi': base['metqi'],
        'bealeMetqi': {'date': base['beale_metqi_date'], 'weekday': base['beale_metqi_weekday']},
        'mebajaHamer': base['mebaja_hamer'],
        'nineveh': base['nineveh_date'],
        'movableFeasts': movable_feasts
    }

def get_movable_holiday(holiday_key, ethiopian_year):
    """
    Calculates the date of a movable holiday for a given year. 

    Args:
        holiday_key (str): The key of the holiday (e.g., 'ABIY_TSOME', 'TINSAYE'). 
        ethiopian_year (int): The Ethiopian year. 

    Returns:
        dict: An Ethiopian date object {'year', 'month', 'day'}. 
    """
    validate_numeric_inputs('get_movable_holiday', ethiopian_year=ethiopian_year)  

    tewsak = MOVABLE_HOLIDAY_TEWSAK.get(holiday_key)  
    if tewsak is None:  
        raise UnknownHolidayError(holiday_key)  
    
    base = _calculate_bahire_hasab_base(ethiopian_year)  

    return add_days(base['nineveh_date'], tewsak) 
