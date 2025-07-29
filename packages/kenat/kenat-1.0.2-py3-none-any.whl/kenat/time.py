from .geez_converter import to_geez, to_arabic
from .constants import PERIOD_LABELS
from .exceptions import InvalidTimeError
from .utils import validate_numeric_inputs

class Time:
    """
    A class to represent and work with Ethiopian time (1-12 hour cycles for day/night).
    """
    def __init__(self, hour, minute=0, period='day'):
        """
        Constructs a Time instance representing an Ethiopian time. 
        
        Args:
            hour (int): The Ethiopian hour (1-12). 
            minute (int): The minute (0-59). 
            period (str): The period ('day' or 'night'). 
        """
        validate_numeric_inputs('Time.constructor', hour=hour, minute=minute) # 
        if not 1 <= hour <= 12: # 
            raise InvalidTimeError(f"Invalid Ethiopian hour: {hour}. Must be between 1 and 12.") # 
        if not 0 <= minute <= 59: # 
            raise InvalidTimeError(f"Invalid minute: {minute}. Must be between 0 and 59.") # 
        if period not in ['day', 'night']: # 
            raise InvalidTimeError(f"Invalid period: \"{period}\". Must be 'day' or 'night'.") # 

        self.hour = hour # 
        self.minute = minute # 
        self.period = period # 

    @classmethod
    def from_gregorian(cls, hour, minute=0):
        """
        Creates a Time instance from a Gregorian 24-hour time. 
        """
        validate_numeric_inputs('Time.from_gregorian', hour=hour, minute=minute) # 
        if not 0 <= hour <= 23: # 
            raise InvalidTimeError(f"Invalid Gregorian hour: {hour}. Must be between 0 and 23.") # 
        
        # Normalize Gregorian hour to an Ethiopian base (where 6 AM is 0)
        temp_hour = hour - 6 # 
        if temp_hour < 0: # 
            temp_hour += 24 # 

        period = 'day' if temp_hour < 12 else 'night' # 
        eth_hour = temp_hour % 12 # 
        eth_hour = 12 if eth_hour == 0 else eth_hour # 

        return cls(eth_hour, minute, period) # 

    def to_gregorian(self):
        """
        Converts the Ethiopian time to Gregorian 24-hour format. 
        """
        # Convert Ethiopian 1-12 hour to a 0-11 offset, with 12 o'clock as 0.
        greg_hour = self.hour % 12 # 
        
        if self.period == 'day': # 
            greg_hour += 6 # 
        else:  # 'night'
            greg_hour += 18 # 

        # Handle the 24-hour wrap-around
        greg_hour %= 24 # 
        return {'hour': greg_hour, 'minute': self.minute} # 

    @classmethod
    def from_string(cls, time_string):
        """
        Creates a Time object from a string representation (e.g., "6:30 night", "፮:፴ ማታ"). 
        """
        if not isinstance(time_string, str) or not time_string.strip(): # 
            raise InvalidTimeError("Input must be a non-empty string.") # 
        if ':' not in time_string: # 
            raise InvalidTimeError(f"Invalid time string: \"{time_string}\". Must include a ':' separator.") # 

        def parse_number(s):
            try:
                return int(s)
            except ValueError:
                try:
                    return to_arabic(s) # 
                except Exception:
                    return float('nan') # 
        
        parts = time_string.replace(':', ' ').split()
        if len(parts) < 2: # 
            raise InvalidTimeError(f"Invalid time string format: \"{time_string}\".") # 

        hour = parse_number(parts[0]) # 
        minute = parse_number(parts[1]) # 

        if hour != hour or minute != minute: # Check for NaN
            raise InvalidTimeError(f"Invalid number in time string: \"{time_string}\"") # 

        period = 'day' # 
        if len(parts) > 2: # 
            period_str = parts[2].lower() # 
            if period_str in ['night', 'ማታ']: # 
                period = 'night' # 
        
        return cls(hour, minute, period) # 

    def add(self, duration):
        """
        Adds a duration to the current time.
        Returns a new Time instance.
        """
        if not isinstance(duration, dict):
            raise InvalidTimeError('Duration must be an object.')
        hours = duration.get('hours', 0)
        minutes = duration.get('minutes', 0)
        validate_numeric_inputs('Time.add', hours=hours, minutes=minutes)
        
        greg = self.to_gregorian()
        total_minutes = (greg['hour'] * 60 + greg['minute'] + hours * 60 + minutes) % 1440

        return Time.from_gregorian(total_minutes // 60, total_minutes % 60)
    
    def subtract(self, duration):
        """
        Subtracts a duration from the current time.
        Returns a new Time instance.
        """
        if not isinstance(duration, dict):
            raise InvalidTimeError('Duration must be an object.')
        hours = duration.get('hours', 0)
        minutes = duration.get('minutes', 0)
        # Subtracting is the same as adding a negative duration
        return self.add({'hours': -hours, 'minutes': -minutes})

    def diff(self, other_time):
        """
        Calculates the shortest difference in hours and minutes between two times.
        """
        if not isinstance(other_time, Time):
            raise InvalidTimeError('Can only compare with another Time instance.')
        
        t1 = self.to_gregorian()
        t2 = other_time.to_gregorian()
        
        total_minutes1 = t1['hour'] * 60 + t1['minute']
        total_minutes2 = t2['hour'] * 60 + t2['minute']
        
        diff = abs(total_minutes1 - total_minutes2)
        
        # The shortest path around a 24h clock
        if diff > 720: # 720 minutes = 12 hours
            diff = 1440 - diff
            
        return {'hours': diff // 60, 'minutes': diff % 60}
    
    def format(self, lang=None, use_geez=None, show_period=True, zero_as_dash=True):
        """Formats the time as a string."""
        # Set intelligent defaults if arguments are not provided
        if use_geez is None:
            use_geez = True
        
        if lang is None:
            # If use_geez is false, the language should default to English
            lang = 'amharic' if use_geez else 'english'

        # --- The rest of the logic works with the corrected defaults ---

        hour_str = to_geez(self.hour) if use_geez else f"{self.hour:02d}"
        
        minute_str = ''
        if zero_as_dash and self.minute == 0:
            minute_str = '_'
        else:
            minute_str = to_geez(self.minute) if use_geez else f"{self.minute:02d}"

        period_label = ''
        if show_period:
            if lang == 'english':
                period_label = f" {self.period}"
            else:
                from .constants import PERIOD_LABELS
                period_label = f" {PERIOD_LABELS.get(self.period, '')}"

        return f"{hour_str}:{minute_str}{period_label}"
        
    def __repr__(self):
        return f"Time(hour={self.hour}, minute={self.minute}, period='{self.period}')"

    def __str__(self):
        return self.format(lang='english', use_geez=False)
    
    def __eq__(self, other):
        """Checks if two Time objects are equal."""
        if not isinstance(other, Time):
            return NotImplemented
        return (self.hour == other.hour and
                self.minute == other.minute and
                self.period == other.period)

