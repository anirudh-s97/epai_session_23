# user_profile_manager_2.py
from datetime import datetime
import weakref
from typing import Any, Callable, Optional

class ValidatedProperty:
    def __init__(self, validator: Callable[[Any], bool]):
        self.validator = validator
        self.name = None
        
    def __set_name__(self, owner: type, name: str):
        self.name = f"_{name}"
        
    def __get__(self, instance: Any, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.name, None)
        
    def __set__(self, instance: Any, value: Any):
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name[1:]}")
        setattr(instance, self.name, value)

class UserProfile:
    default_last_login = datetime(2000, 1, 1)
    
    def __init__(self, username: str, email: str, last_login: Optional[datetime] = None):
        self.username = username
        self.email = email
        self._last_login = last_login
    
    @staticmethod
    def validate_username(value: str) -> bool:
        return isinstance(value, str) and len(value.strip()) > 0
    
    @staticmethod
    def validate_email(value: str) -> bool:
        if not isinstance(value, str) or not value:
            raise ValueError("Email cannot be empty")
        
        # Split into local and domain parts
        try:
            if value.count('@') != 1:
                raise ValueError("Email must contain exactly one @ symbol")
            local_part, domain = value.split('@')
        except ValueError:
            raise ValueError("Invalid email format")
        
        # Check local part
        if not local_part:
            raise ValueError("Local part cannot be empty")
        if ' ' in local_part:
            raise ValueError("Local part cannot contain spaces")
        if '..' in local_part:
            raise ValueError("Local part cannot contain consecutive dots")
        
        # More comprehensive local part validation
        if local_part.startswith('.') or local_part.endswith('.'):
            raise ValueError("Local part cannot start or end with a dot")
        
        # Ensure local part contains valid characters
        local_valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-+_')
        if not all(c in local_valid_chars for c in local_part):
            raise ValueError("Local part contains invalid characters")
        
        # Check domain
        if not domain:
            raise ValueError("Domain cannot be empty")
        if ' ' in domain:
            raise ValueError("Domain cannot contain spaces")
        if domain.startswith('.') or domain.endswith('.'):
            raise ValueError("Domain cannot start or end with a dot")
        if '..' in domain:
            raise ValueError("Domain cannot contain consecutive dots")
        if '_' in domain:
            raise ValueError("Domain cannot contain underscores")
        
        # Check domain parts
        domain_parts = domain.split('.')
        if len(domain_parts) < 2:
            raise ValueError("Domain must have at least one dot")
        
        # Check each domain part
        for part in domain_parts:
            if not part:
                raise ValueError("Domain parts cannot be empty")
            if part.startswith('-') or part.endswith('-'):
                raise ValueError("Domain parts cannot start or end with a hyphen")
            
            # Ensure domain parts contain valid characters
            domain_valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-')
            if not all(c in domain_valid_chars for c in part):
                raise ValueError("Domain parts contain invalid characters")
        
        return True
    
    username = ValidatedProperty(validate_username)
    email = ValidatedProperty(validate_email)
    
    @property
    def last_login(self) -> datetime:
        return self._last_login if self._last_login is not None else self.default_last_login
    
    @last_login.setter
    def last_login(self, value: Optional[datetime]):
        if value is not None and not isinstance(value, datetime):
            raise ValueError("last_login must be a datetime object or None")
        self._last_login = value

class UserProfileManager:
    def __init__(self):
        self._profiles = {}
        self._cache = weakref.WeakValueDictionary()
        
    def create_profile(self, username: str, email: str, 
                      last_login: Optional[datetime] = None) -> UserProfile:
        profile = UserProfile(username, email, last_login)
        self._profiles[username] = profile
        self._cache[username] = profile
        return profile
        
    def get_profile(self, username: str) -> Optional[UserProfile]:
        # Try cache first
        profile = self._cache.get(username)
        if profile is not None:
            return profile
        
        # Try strong references
        profile = self._profiles.get(username)
        if profile is not None:
            self._cache[username] = profile
            return profile
        
        return None
        
    def remove_profile(self, username: str) -> bool:
        if username in self._profiles:
            del self._profiles[username]
            self._cache.pop(username, None)
            return True
        return False