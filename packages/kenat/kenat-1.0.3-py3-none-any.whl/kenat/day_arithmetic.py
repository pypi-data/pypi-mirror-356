from .utils import (
    get_ethiopian_days_in_month,
    is_ethiopian_leap_year,
    validate_numeric_inputs,
    validate_ethiopian_date_object
)

def add_days(ethiopian, days):
    """
    Adds a specified number of days to an Ethiopian date.

    Args:
        ethiopian (dict): The starting Ethiopian date {'year', 'month', 'day'}.
        days (int): The number of days to add.

    Returns:
        dict: The resulting Ethiopian date.
    """
    validate_ethiopian_date_object(ethiopian, 'add_days', 'ethiopian') # 
    validate_numeric_inputs('add_days', days=days) # 
    
    # Create mutable copies
    year, month, day = ethiopian['year'], ethiopian['month'], ethiopian['day']
    day += days

    # Roll over the days into months and years
    while day > get_ethiopian_days_in_month(year, month): # 
        day -= get_ethiopian_days_in_month(year, month) # 
        month += 1 # 
        if month > 13: # 
            month = 1 # 
            year += 1 # 
            
    return {'year': year, 'month': month, 'day': day}

def add_months(ethiopian, months):
    """
    Adds a specified number of months to an Ethiopian date.

    Args:
        ethiopian (dict): The starting Ethiopian date {'year', 'month', 'day'}.
        months (int): The number of months to add.

    Returns:
        dict: The resulting Ethiopian date.
    """
    validate_ethiopian_date_object(ethiopian, 'add_months', 'ethiopian') # 
    validate_numeric_inputs('add_months', months=months) # 
    
    year, month, day = ethiopian['year'], ethiopian['month'], ethiopian['day']
    
    total_months = month + months # 
    year += (total_months - 1) // 13 # 
    month = ((total_months - 1) % 13) + 1 # 

    # If the original day is greater than the number of days in the new month,
    # cap it at the last day of the new month.
    days_in_target_month = get_ethiopian_days_in_month(year, month) # 
    if day > days_in_target_month: # 
        day = days_in_target_month # 
        
    return {'year': year, 'month': month, 'day': day}

def add_years(ethiopian, years):
    """
    Adds a specified number of years to an Ethiopian date.

    Args:
        ethiopian (dict): The starting Ethiopian date {'year', 'month', 'day'}.
        years (int): The number of years to add.

    Returns:
        dict: The resulting Ethiopian date.
    """
    validate_ethiopian_date_object(ethiopian, 'add_years', 'ethiopian') # 
    validate_numeric_inputs('add_years', years=years) # 

    year, month, day = ethiopian['year'], ethiopian['month'], ethiopian['day']
    year += years # 

    # Handle the case where the original date was a leap day (Pagume 6),
    # and the new date is in a non-leap year.
    if month == 13 and day == 6 and not is_ethiopian_leap_year(year): # 
        day = 5 # 
        
    return {'year': year, 'month': month, 'day': day}

def diff_in_days(date_a, date_b):
    """
    Calculates the difference in days between two Ethiopian dates.

    Args:
        date_a (dict): The first Ethiopian date.
        date_b (dict): The second Ethiopian date.

    Returns:
        int: The difference in days.
    """
    validate_ethiopian_date_object(date_a, 'diff_in_days', 'a') # 
    validate_ethiopian_date_object(date_b, 'diff_in_days', 'b') # 

    def total_days(eth_date): # 
        """Helper to count days from a fixed epoch (year 1, month 1, day 1)."""
        days = 0
        # Add days from full years
        for y in range(1, eth_date['year']): # 
            days += 366 if is_ethiopian_leap_year(y) else 365 # 
        # Add days from full months in the current year
        for m in range(1, eth_date['month']): # 
            days += get_ethiopian_days_in_month(eth_date['year'], m)
        # Add days in the current month
        days += eth_date['day'] # 
        return days

    return total_days(date_a) - total_days(date_b) # 

def diff_in_months(date_a, date_b):
    """
    Calculates the difference in months between two Ethiopian dates.
    """
    validate_ethiopian_date_object(date_a, 'diff_in_months', 'a') # 
    validate_ethiopian_date_object(date_b, 'diff_in_months', 'b') # 
    
    total_months_a = date_a['year'] * 13 + (date_a['month'] - 1) # 
    total_months_b = date_b['year'] * 13 + (date_b['month'] - 1) # 
    
    diff = total_months_a - total_months_b # 
    
    # Adjust if the day of the later date hasn't been reached yet
    if date_a['day'] < date_b['day']: # 
        diff -= 1 # 
        
    return diff

def diff_in_years(date_a, date_b):
    """
    Calculates the difference in years between two Ethiopian dates.
    """
    validate_ethiopian_date_object(date_a, 'diff_in_years', 'a') # 
    validate_ethiopian_date_object(date_b, 'diff_in_years', 'b') # 
    
    diff = date_a['year'] - date_b['year']
    
    # If the month/day of 'a' is earlier in the year than 'b',
    # a full year has not yet passed.
    if date_a['month'] < date_b['month'] or \
       (date_a['month'] == date_b['month'] and date_a['day'] < date_b['day']): # 
        diff -= 1 # 
        
    return diff