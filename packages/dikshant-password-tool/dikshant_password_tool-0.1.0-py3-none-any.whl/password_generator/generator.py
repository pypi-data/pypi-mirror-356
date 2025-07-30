import random
import string

def password_generator(length=12, include_uppercase=True, include_digits=True, include_special=True):
    """
    Generate a random password with specified complexity.
    
    Args:
        length (int): Length of the password (default: 12)
        include_uppercase (bool): Include uppercase letters (default: True)
        include_digits (bool): Include digits (default: True)
        include_special (bool): Include special characters (default: True)
    
    Returns:
        str: Generated password
    
    Raises:
        ValueError: If no character sets are selected or length is invalid
    """
    if length < 1:
        raise ValueError("Password length must be at least 1")
    
    character_sets = []
    character_sets.append(string.ascii_lowercase)
    
    if include_uppercase:
        character_sets.append(string.ascii_uppercase)
    if include_digits:
        character_sets.append(string.digits)
    if include_special:
        character_sets.append(string.punctuation)
    
    if not character_sets:
        raise ValueError("At least one character set must be included")
    
    # Ensure at least one character from each selected set
    password = []
    for charset in character_sets:
        password.append(random.choice(charset))
    
    # Fill the rest of the password with random choices from all sets
    all_chars = ''.join(character_sets)
    password.extend(random.choices(all_chars, k=length - len(password)))
    
    # Shuffle to avoid predictable patterns
    random.shuffle(password)
    
    return ''.join(password)