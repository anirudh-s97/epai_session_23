# tests.py
import pytest
from datetime import datetime, timedelta
import weakref
import gc
from user_profile_manager import UserProfile, UserProfileManager, ValidatedProperty

def test_validated_property_descriptor():
    class TestClass:
        value = ValidatedProperty(lambda x: isinstance(x, int))
    
    obj = TestClass()
    obj.value = 42
    assert obj.value == 42
    
    with pytest.raises(ValueError):
        obj.value = "not an integer"

def test_valid_profile_creation():
    profile = UserProfile("john_doe", "john@example.com")
    assert profile.username == "john_doe"
    assert profile.email == "john@example.com"
    assert profile.last_login == UserProfile.default_last_login

def test_invalid_username():
    with pytest.raises(ValueError):
        UserProfile("", "john@example.com")
    with pytest.raises(ValueError):
        UserProfile("   ", "john@example.com")

def test_username_edge_cases():
    # Valid cases
    UserProfile("user123", "test@example.com")
    UserProfile("a" * 100, "test@example.com")  # Very long username
    UserProfile("user-name", "test@example.com")  # With hyphen
    UserProfile("user_name", "test@example.com")  # With underscore
    
    # Invalid cases
    with pytest.raises(ValueError):
        UserProfile("\n", "test@example.com")  # Newline
    with pytest.raises(ValueError):
        UserProfile("\t", "test@example.com")  # Tab
    with pytest.raises(ValueError):
        UserProfile(" ", "test@example.com")  # Space
    with pytest.raises(ValueError):
        UserProfile("", "test@example.com")  # Empty string

def test_email_edge_cases():
    # Valid cases
    valid_emails = [
        "test@example.com",
        "test.name@example.com",
        "test+label@example.com",
        "test@subdomain.example.com",
        "test@sub-domain.example.com",
        "123@example.com",
        "test@123.com",
        "test-name@example.com",
    ]
    
    for email in valid_emails:
        try:
            UserProfile("user", email)
        except ValueError as e:
            pytest.fail(f"Valid email failed validation: {email}")
    
    # Invalid cases
    invalid_emails = [
        "",  # Empty string
        "test",  # No @ or domain
        "@example.com",  # No local part
        "test@",  # No domain
        "test@.com",  # No domain name
        "test@example",  # No TLD
        "test.@example.com",  # Dot at end of local part
        "@.com",  # No local part or domain
        "test@example..com",  # Consecutive dots
        "test@.example.com",  # Dot after @
        "test@example-.com",  # Hyphen at end of domain part
        "test@-example.com",  # Hyphen at start of domain part
        "test@exam ple.com",  # Space in domain
        "te st@example.com",  # Space in local part
        "test@example_com",  # Underscore in domain
        "test@@example.com",  # Multiple @
    ]
    
    for email in invalid_emails:
        try:
            UserProfile("user", email)
            pytest.fail(f"Invalid email passed validation: {email}")
        except ValueError:
            pass  # This is expected

def test_last_login_comprehensive():
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    
    # Test with different datetime values
    profile = UserProfile("user", "test@example.com", now)
    assert profile.last_login == now
    
    profile.last_login = yesterday
    assert profile.last_login == yesterday
    
    # Test with None
    profile.last_login = None
    assert profile.last_login == UserProfile.default_last_login
    
    # Test invalid types
    invalid_dates = [
        "2023-01-01",  # String
        123456789,  # Integer
        (2023, 1, 1),  # Tuple
        now.timestamp(),  # Float
    ]
    
    for invalid_date in invalid_dates:
        with pytest.raises(ValueError):
            profile.last_login = invalid_date

def test_profile_manager_comprehensive():
    manager = UserProfileManager()
    
    # Test creation
    profile = manager.create_profile("user1", "user1@example.com")
    assert profile.username == "user1"
    
    # Test retrieval
    retrieved = manager.get_profile("user1")
    assert retrieved is profile
    
    # Test non-existent profile
    assert manager.get_profile("non_existent") is None
    
    # Test removal
    assert manager.remove_profile("user1") is True
    assert manager.get_profile("user1") is None
    assert manager.remove_profile("user1") is False

def test_profile_manager_concurrent_access():
    manager = UserProfileManager()
    
    # Create initial profile
    profile1 = manager.create_profile("user", "user@example.com")
    
    # Update profile through different references
    profile2 = manager.get_profile("user")
    assert profile1 is profile2
    
    # Modify through one reference
    profile1.email = "new@example.com"
    
    # Check if change is visible through other reference
    assert profile2.email == "new@example.com"

def test_weak_references():
    manager = UserProfileManager()
    username = "temp_user"
    
    # Create a profile and only store it in the cache
    profile = manager.create_profile(username, "temp@example.com")
    assert manager.get_profile(username) is profile
    
    # Remove from _profiles to ensure only weak reference remains
    del manager._profiles[username]
    
    # Verify it's still in cache
    assert username in manager._cache
    
    # Delete the last strong reference
    del profile
    
    # Force garbage collection
    gc.collect()
    
    # The profile should now be gone from cache
    assert manager.get_profile(username) is None

def test_profile_manager_cache_limit():
    manager = UserProfileManager()
    
    # Create many profiles to test cache behavior
    for i in range(100):
        username = f"user{i}"
        manager.create_profile(username, f"user{i}@example.com")
        
    # Access profiles in reverse order to test cache behavior
    for i in range(99, -1, -1):
        username = f"user{i}"
        profile = manager.get_profile(username)
        assert profile is not None
        assert profile.username == username

def test_profile_attribute_updates():
    manager = UserProfileManager()
    profile = manager.create_profile("user", "old@example.com")
    
    # Test email update
    profile.email = "new@example.com"
    assert manager.get_profile("user").email == "new@example.com"
    
    # Test last_login update
    now = datetime.now()
    profile.last_login = now
    assert manager.get_profile("user").last_login == now
    
    # Test invalid updates
    with pytest.raises(ValueError):
        profile.email = "invalid_email"
    
    # Ensure original value remains after failed update
    assert profile.email == "new@example.com"

def test_default_last_login_inheritance():
    # Test that default_last_login can be overridden in subclasses
    class CustomProfile(UserProfile):
        default_last_login = datetime(2020, 1, 1)
    
    profile = CustomProfile("user", "test@example.com")
    assert profile.last_login == datetime(2020, 1, 1)