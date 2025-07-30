import random
import string
from typing import List

def generate(
    length: int = 12,
    lowercase: bool = True,
    uppercase: bool = True,
    digits: bool = True,
    special: bool = True
) -> str:
    """
    Generate a secure random password with guaranteed character sets.
    
    Args:
        length: Password length (8-64)
        lowercase: Include a-z
        uppercase: Include A-Z
        digits: Include 0-9
        special: Include !@#$%^&*
    
    Returns:
        Generated password string
    
    Raises:
        ValueError: If invalid parameters are provided
    """
    # Validate length
    if not 8 <= length <= 64:
        raise ValueError("Password length must be between 8 and 64 characters")
    
    # Validate at least one character set
    if not any([lowercase, uppercase, digits, special]):
        raise ValueError("At least one character set must be enabled")

    # Collect enabled character sets
    char_sets = []
    if lowercase:
        char_sets.append(string.ascii_lowercase)
    if uppercase:
        char_sets.append(string.ascii_uppercase)
    if digits:
        char_sets.append(string.digits)
    if special:
        char_sets.append(string.punctuation)

    # Ensure at least one character from each enabled set
    password = []
    for charset in char_sets:
        password.append(random.choice(charset))
    
    # Fill remaining length with random choices from all enabled sets
    all_chars = ''.join(char_sets)
    remaining_length = length - len(password)
    password.extend(random.choices(all_chars, k=remaining_length))
    
    # Shuffle to avoid predictable patterns
    random.shuffle(password)
    
    return ''.join(password)