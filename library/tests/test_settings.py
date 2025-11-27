"""Tests for settings configuration."""

from library.settings import settings
from library.conf.settings import Settings


def test_settings_exists():
    """Test that settings instance exists."""
    assert settings is not None


def test_settings_is_settings_class():
    """Test that settings is an instance of Settings."""
    assert isinstance(settings, Settings)


def test_settings_has_project_name():
    """Test that settings has project_name attribute."""
    assert hasattr(settings, "project_name")
    assert settings.project_name is not None
    assert len(settings.project_name) > 0


def test_settings_has_debug():
    """Test that settings has debug attribute."""
    assert hasattr(settings, "debug")
    assert isinstance(settings.debug, bool)


def test_settings_class_exists():
    """Test that Settings class exists."""
    assert Settings is not None


def test_settings_can_be_instantiated():
    """Test that Settings can be instantiated."""
    test_settings = Settings()
    assert test_settings is not None
    assert isinstance(test_settings, Settings)


def test_debug_defaults_to_false():
    """Test that debug defaults to False."""
    test_settings = Settings()
    assert test_settings.debug is False


def test_all_required_attributes_present():
    """Test that all required attributes are present."""
    required_attrs = [
        "debug",
    ]

    for attr in required_attrs:
        assert hasattr(settings, attr), f"Missing attribute: {attr}"


def test_settings_can_load_from_env():
    """Test that settings can be overridden by environment variables."""
    # This tests that the Settings class is properly configured
    # to load from environment variables using pydantic-settings
    test_settings = Settings()
    assert hasattr(test_settings, "model_config") or hasattr(test_settings, "Config")


def test_debug_from_env(monkeypatch):
    """Test that debug can be set from environment."""
    monkeypatch.setenv("DEBUG", "True")
    test_settings = Settings()
    assert test_settings.debug is True


def test_settings_validates_types():
    """Test that settings validates types correctly."""
    # This is implicitly tested by pydantic, but we verify it works
    test_settings = Settings()
    assert isinstance(test_settings.debug, bool)
