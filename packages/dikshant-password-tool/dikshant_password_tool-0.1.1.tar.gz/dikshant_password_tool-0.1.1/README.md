# Dikshant Password Tool

![PyPI](https://img.shields.io/pypi/v/dikshant-password-tool)
![Python](https://img.shields.io/pypi/pyversions/dikshant-password-tool)
![License](https://img.shields.io/pypi/l/dikshant-password-tool)
![Downloads](https://img.shields.io/pypi/dm/dikshant-password-tool)

A secure, customizable password generator for Python applications.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features](#features)
- [Advanced Usage](#advanced-usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

```bash
pip install dikshant-password-tool


## Quick Start

from dikshant_password_tool import password_generator

# Generate a default 12-character password
print(password_generator())
# Example output: "J7$k9Lp2@qR!"


## Features
✔️ Customizable password length (4-64 characters)
✔️ Toggle character sets:
 - Uppercase (A-Z)
 - Lowercase (a-z)
 - Digits (0-9)
 - Special characters (!@#$%^&*)
✔️ Cryptographically secure randomization
✔️ Lightweight with no dependencies


## Advanced Usage
* Custom Length Password

# 16-character password
password_generator(length=16)

## Specific Character Sets

# Only letters
password_generator(include_digits=False, include_special=False)

# Only numbers (PIN code)
password_generator(length=6, include_uppercase=False, include_special=False)


## Exclude Similar Characters
# Exclude similar looking characters (1, l, I, etc.)
from dikshant_password_tool import password_generator, exclude_similar_chars
password = password_generator(exclude_chars=exclude_similar_chars)


## API Reference
* password_generator()
password_generator(
    length=12,                   # Password length (4-64)
    include_uppercase=True,      # Include A-Z
    include_digits=True,         # Include 0-9
    include_special=True,        # Include !@#$%^&*
    exclude_chars=""             # Characters to exclude
) -> str


## Raises:
ValueError - If invalid parameters are provided

Examples
## Generate API Key

api_key = password_generator(length=32, include_special=False)


## Create Memorable Password

# Longer password without special chars
memorable_pass = password_generator(length=20, include_special=False)


## Secure Database Password

db_password = password_generator(length=24)


## Contributing
Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some amazing feature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request


## License
Distributed under the MIT License. See LICENSE for more information.


📫 Contact: Dikshant Ghimire - dikshantghimire.com.np - dikkughimire@gmail.com
🔗 Project Link: https://github.com/dikshantgh/dikshant-password-tool
