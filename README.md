# UserProfileManager 🚀

## Overview

UserProfileManager is a robust Python library for managing user profiles with advanced validation, caching, and memory-efficient reference handling. It provides a flexible system for creating, storing, and managing user profiles with strong data integrity checks.

## 🌟 Key Features

- **Robust Validation**
  - Custom descriptor-based property validation
  - Strict email and username format checks
  - Immutable validation rules

- **Smart Caching**
  - Weak reference-based caching mechanism
  - Automatic memory management
  - Efficient profile retrieval

- **Flexible Profile Management**
  - Configurable default login timestamp
  - Nullable last login support
  - Easy profile creation and manipulation

## 🛠 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/user-profile-manager.git

# Install dependencies
pip install -r requirements.txt
```

## 💡 Usage Examples

### Creating a User Profile

```python
from user_profile_manager import UserProfile, UserProfileManager
from datetime import datetime

# Initialize Profile Manager
manager = UserProfileManager()

# Create a new profile
profile = manager.create_profile(
    username="johndoe", 
    email="john.doe@example.com",
    last_login=datetime.now()
)
```

### Retrieving and Updating Profiles

```python
# Retrieve a profile
retrieved_profile = manager.get_profile("johndoe")

# Update email (with built-in validation)
retrieved_profile.email = "new.email@example.com"
```

## 🧪 Validation Rules

### Username Validation
- Must be a non-empty string
- Cannot contain only whitespace
- Supports alphanumeric characters, hyphens, and underscores

### Email Validation
- Must contain exactly one "@" symbol
- Local part and domain must follow strict formatting rules
- No consecutive dots
- No spaces allowed
- Domain must have at least two parts

## 🔍 Technical Details

### ValidatedProperty Descriptor
- Provides runtime validation for class attributes
- Uses custom validation functions
- Automatically binds property names

### Caching Strategy
- Uses `weakref.WeakValueDictionary` for efficient memory management
- Automatically removes unused profiles
- Prevents memory leaks

## 🚦 Testing

Run comprehensive test suite:

```bash
pytest tests.py
```

### Test Coverage
- Username validation
- Email format checks
- Last login handling
- Profile creation and management
- Weak reference and caching behavior

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 💌 Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/user-profile-manager](https://github.com/yourusername/user-profile-manager)