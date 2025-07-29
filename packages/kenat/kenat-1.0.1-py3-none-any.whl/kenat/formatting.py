from .geez_converter import to_geez
from .constants import MONTH_NAMES, DAYS_OF_WEEK
from .utils import get_weekday

def format_standard(et_date, lang='amharic'):
    """
    Formats an Ethiopian date using a language-specific month name and Arabic numerals.
    Example: "መስከረም 10 2016" 
    """
    names = MONTH_NAMES.get(lang, MONTH_NAMES['amharic']) 
    month_name = names[et_date['month'] - 1] 
    return f"{month_name} {et_date['day']} {et_date['year']}" 

def format_in_geez_amharic(et_date):
    """
    Formats an Ethiopian date in Geez numerals with Amharic month name.
    Example: "መስከረም ፲፩ ፳፻፲፮" 
    """
    month_name = MONTH_NAMES['amharic'][et_date['month'] - 1] 
    return f"{month_name} {to_geez(et_date['day'])} {to_geez(et_date['year'])}" 

def format_with_time(et_date, time_obj, lang='amharic'):
    """
    Formats an Ethiopian date and time as a string.
    Example: "መስከረም 10 2016 08:30 ጠዋት" 
    """
    base = format_standard(et_date, lang)
    time_string = time_obj.format(lang=lang, use_geez=False, zero_as_dash=False)  
    return f"{base} {time_string}" 

def format_with_weekday(et_date, lang='amharic', use_geez=False):
    """
    Formats a date with the weekday name, month name, day, and year. 
    Example: "ማክሰኞ, መስከረም 1 2016" 
    """
    weekday_index = get_weekday(et_date) 
    weekday_name = DAYS_OF_WEEK.get(lang, DAYS_OF_WEEK['amharic'])[weekday_index] 
    month_name = MONTH_NAMES.get(lang, MONTH_NAMES['amharic'])[et_date['month'] - 1] 
    day = to_geez(et_date['day']) if use_geez else et_date['day'] 
    year = to_geez(et_date['year']) if use_geez else et_date['year'] 

    return f"{weekday_name}, {month_name} {day} {year}" 

def format_short(et_date):
    """
    Returns Ethiopian date in short "yyyy/mm/dd" format. 
    Example: "2017/10/25"
    """
    y = et_date['year'] 
    m = str(et_date['month']).zfill(2) 
    d = str(et_date['day']).zfill(2) 
    return f"{y}/{m}/{d}" 

def to_iso_date_string(et_date, time_obj=None):
    """
    Returns an ISO-like string: "YYYY-MM-DD" or "YYYY-MM-DDTHH:mm". 
    """
    y = et_date['year'] 
    m = str(et_date['month']).zfill(2) 
    d = str(et_date['day']).zfill(2) 

    if not time_obj: 
        return f"{y}-{m}-{d}" 

    hr = str(time_obj.hour).zfill(2) 
    minute = str(time_obj.minute).zfill(2) 
    return f"{y}-{m}-{d}T{hr}:{minute}" 
