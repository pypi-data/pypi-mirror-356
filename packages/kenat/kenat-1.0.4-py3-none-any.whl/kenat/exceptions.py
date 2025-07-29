class KenatError(Exception):
    """Base class for all custom errors in the Kenat library."""
    def __init__(self, message):
        super().__init__(message)
        self.name = self.__class__.__name__

class InvalidEthiopianDateError(KenatError):
    """Thrown when an Ethiopian date is numerically invalid (e.g., month 14)."""
    def __init__(self, year, month, day):
        super().__init__(f"Invalid Ethiopian date: {year}/{month}/{day}")
        self.date = {'year': year, 'month': month, 'day': day}

class InvalidGregorianDateError(KenatError):
    """Thrown when a Gregorian date is numerically invalid."""
    def __init__(self, year, month, day):
        super().__init__(f"Invalid Gregorian date: {year}/{month}/{day}")
        self.date = {'year': year, 'month': month, 'day': day}

class InvalidDateFormatError(KenatError):
    """Thrown when a date string provided to the constructor has an invalid format."""
    def __init__(self, input_string):
        message = f"Invalid date string format: \"{input_string}\". Expected 'yyyy/mm/dd' or 'yyyy-mm-dd'."
        super().__init__(message)
        self.input_string = input_string
class UnrecognizedInputError(KenatError):
    """Thrown when the Kenat constructor receives an input type it cannot handle."""
    def __init__(self, input_data):
        input_type = type(input_data).__name__
        super().__init__(f"Unrecognized input type for Kenat constructor: {input_type}")
        self.input = input_data

class GeezConverterError(KenatError):
    """Thrown for errors occurring during Ge'ez numeral conversion."""
    def __init__(self, message):
        super().__init__(message)

class InvalidInputTypeError(KenatError):
    """Thrown when a function receives an argument of an incorrect type."""
    def __init__(self, function_name, parameter_name, expected_type, received_value):
        received_type = type(received_value).__name__
        message = (f"Invalid type for parameter '{parameter_name}' in function '{function_name}'. "
                   f"Expected '{expected_type}' but got '{received_type}'.")
        super().__init__(message)
        self.function_name = function_name 
        self.parameter_name = parameter_name 
        self.expected_type = expected_type 
        self.received_value = received_value 

class InvalidTimeError(KenatError):
    """Thrown for errors related to invalid time components."""
    def __init__(self, message):
        super().__init__(message)

class InvalidGridConfigError(KenatError):
    """Thrown for invalid configuration options passed to MonthGrid."""
    def __init__(self, message):
        super().__init__(message)

class UnknownHolidayError(KenatError):
    """Thrown when an unknown holiday key is used."""
    def __init__(self, holiday_key):
        super().__init__(f"Unknown movable holiday key: \"{holiday_key}\"")
        self.holiday_key = holiday_key