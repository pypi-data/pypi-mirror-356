# DikshantLock  
[![PyPI](https://img.shields.io/pypi/v/dikshantlock)](https://pypi.org/project/dikshantlock/) 
[![Python](https://img.shields.io/pypi/pyversions/dikshantlock)](https://pypi.org/project/dikshantlock/) 
[![License](https://img.shields.io/pypi/l/dikshantlock)](https://pypi.org/project/dikshantlock/) 
[![Downloads](https://img.shields.io/pypi/dm/dikshantlock)](https://pypi.org/project/dikshantlock/)  

A secure password generation toolkit for Python applications with guaranteed character inclusion.  

## Table of Contents  
- [Features](#features)  
- [Installation](#installation)  
- [Basic Usage](#basic-usage)  
- [Advanced Usage](#advanced-usage)  
- [API Reference](#api-reference)  
- [Examples](#examples)  
- [Security Guarantees](#security-guarantees)  
- [Contributing](#contributing)  
- [License](#license)  

## Features  
- Generate cryptographically strong passwords  
- Customizable length (8-64 characters)  
- Toggle character sets:  
  - Lowercase letters (a-z)  
  - Uppercase letters (A-Z)  
  - Digits (0-9)  
  - Special characters (!@#$%^&*)  
- Guaranteed to include at least one character from each enabled set  
- Properly shuffled to avoid predictable patterns  

## Installation  
```bash
pip install dikshantlock
```

## Basic Usage  
```python
from dikshantlock import generate  

# Generate a default 12-character password  
password = generate()  
print(password)  # Example: "k7@j9Lp2#qR!" (contains at least one of each character type)

# Generate a 16-character password without special chars  
simple_pass = generate(length=16, special=False)  
```

## Advanced Usage  

### Custom Character Sets  
```python
# Numbers only (6-digit PIN code)  
pin = generate(length=6, lowercase=False, uppercase=False, special=False)  

# Letters only (no numbers/special chars)  
memorable = generate(length=20, digits=False, special=False)  

# No lowercase letters  
password = generate(lowercase=False)  
```

### Maximum Security Password  
```python
max_security = generate(length=32)  # 32 chars with all character sets enabled  
```

## API Reference  
```python
generate(
    length=12,
    lowercase=True,
    uppercase=True,
    digits=True,
    special=True
)
```

**Parameters:**  
- `length`: Password length (8-64, default: 12)  
- `lowercase`: Include a-z (default: True)  
- `uppercase`: Include A-Z (default: True)  
- `digits`: Include 0-9 (default: True)  
- `special`: Include special chars (default: True)  

**Returns:**  
- `str` - Generated password containing at least one character from each enabled set  

**Raises:**  
- `ValueError` if length is invalid or no character sets are enabled  

## Examples  

### Generate API Key  
```python
api_key = generate(length=32, special=False)  # Alphanumeric only  
```

### Create Database Password  
```python
db_pass = generate(length=24, lowercase=False)  # Uppercase + digits + special chars only  
```

### Temporary Access Token  
```python
token = generate(length=16, special=False, uppercase=False)  # Lowercase + digits only  
```

## Security Guarantees  
- Uses cryptographically secure random number generation  
- Always includes at least one character from each enabled character set  
- Passwords are properly shuffled to avoid predictable patterns  
- Validates all inputs to prevent weak password generation  

## Contributing  
1. Fork the repository  
2. Create your feature branch   
3. Commit your changes   
4. Push to the branch   
5. Open a Pull Request  

## License  
Distributed under the MIT License. See `LICENSE` for more information.  

📫 **Contact**: Dikshant Ghimire - dikkughimire@gmail.com  
🔗 **Project Link**: https://github.com/dikshantgh/dikshantlock  
🐛 **Report Issues**: https://github.com/dikshantgh/dikshantlock/issues