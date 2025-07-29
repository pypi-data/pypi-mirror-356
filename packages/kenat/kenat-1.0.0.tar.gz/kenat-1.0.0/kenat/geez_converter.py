from .exceptions import GeezConverterError

# A dictionary holding the Ethiopic numeral symbols
SYMBOLS = {
    'ones': ['', '፩', '፪', '፫', '፬', '፭', '፮', '፯', '፰', '፱'],
    'tens': ['', '፲', '፳', '፴', '፵', '፶', '፷', '፸', '፹', '፺'],
    'hundred': '፻',
    'ten_thousand': '፼'
}

def to_geez(input_num):
    """
    Converts a natural number to an Ethiopic numeral string.
    
    Args:
        input_num (int or str): The positive integer to convert.

    Returns:
        str: The Ethiopic numeral string.
        
    Raises:
        GeezConverterError: If the input is not a valid non-negative integer.
    """
    if not isinstance(input_num, (int, str)):
        raise GeezConverterError("Input must be a number or a string.")

    try:
        num = int(input_num)
        if num < 0:
            raise ValueError
    except (ValueError, TypeError):
        raise GeezConverterError("Input must be a non-negative integer.")

    if num == 0:
        return '0'  # Ge'ez doesn't traditionally have a zero, but useful for modern contexts.

    # Helper for numbers 1-99
    def convert_below_100(n):
        if n <= 0:
            return ''
        tens_digit = n // 10
        ones_digit = n % 10
        return SYMBOLS['tens'][tens_digit] + SYMBOLS['ones'][ones_digit]

    if num < 100:
        return convert_below_100(num)

    if num == 100:
        return SYMBOLS['hundred']

    if num < 10000:
        hundreds = num // 100
        remainder = num % 100
        # For 101, it's ፻፩. If the hundred part is 1, don't add a prefix.
        hundred_part = (convert_below_100(hundreds) if hundreds > 1 else '') + SYMBOLS['hundred']
        return hundred_part + convert_below_100(remainder)

    # For numbers >= 10000, use recursion
    ten_thousand_part = num // 10000
    remainder = num % 10000
    
    # If the ten-thousand part is 1, no prefix is needed (e.g., ፼, not ፩፼)
    ten_thousand_geez = (to_geez(ten_thousand_part) if ten_thousand_part > 1 else '') + SYMBOLS['ten_thousand']
    
    return ten_thousand_geez + (to_geez(remainder) if remainder > 0 else '')

def to_arabic(geez_str):
    """
    Converts a Ge'ez numeral string to its Arabic numeral equivalent.

    Args:
        geez_str (str): The Ge'ez numeral string.

    Returns:
        int: The Arabic numeral.

    Raises:
        GeezConverterError: If the input is not a valid Ge'ez numeral string.
    """
    if not isinstance(geez_str, str):
        raise GeezConverterError('Input must be a non-empty string.')
    if not geez_str.strip():
        return 0

    reverse_map = {char: i for i, char in enumerate(SYMBOLS['ones']) if char}
    reverse_map.update({char: i * 10 for i, char in enumerate(SYMBOLS['tens']) if char})
    reverse_map[SYMBOLS['hundred']] = 100
    reverse_map[SYMBOLS['ten_thousand']] = 10000
    
    total = 0
    current_number = 0

    for char in geez_str:
        value = reverse_map.get(char)
        if value is None:
            raise GeezConverterError(f"Unknown Ge'ez numeral: {char}")

        if value in [100, 10000]:
            # If current_number is 0, it's a standalone ፻ (100) or ፼ (10000).
            current_number = (current_number or 1) * value
            
            # ፼ acts as a separator. Add the completed segment to total.
            if value == 10000:
                total += current_number
                current_number = 0
        else:
            # Add simple digit values (1-99)
            current_number += value
    
    # Add any remaining part (for numbers that don't end in ፼)
    total += current_number
    return total