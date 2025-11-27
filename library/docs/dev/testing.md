# Testing

This project uses [pytest](https://docs.pytest.org/) as its testing framework, providing comprehensive test coverage for all features with async/await support, fixtures, and powerful assertion capabilities.

## Project Test Structure

Tests are organized in the `tests/` directory with a structure that mirrors the main package:

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and test configuration
├── test_cli.py              # CLI application tests
├── test_celery.py           # Celery task queue tests
├── test_qq.py               # QuasiQueue multiprocessing tests
├── test_settings.py         # Settings and configuration tests
├── test_www.py              # FastAPI web application tests
└── services/
    ├── __init__.py
    ├── test_cache.py        # Cache service tests
    └── test_jinja.py        # Template service tests
```

### Test Organization Principles

- **Mirror package structure**: Test files mirror the structure of the main package
- **Feature-based testing**: Each major feature has its own test file
- **Shared fixtures**: Common test setup is centralized in `conftest.py`

## Running Tests

### Basic Test Execution

```bash
# Run all tests
make test

# Run only pytest (skip linting and type checks)
make pytest

# Run tests with verbose output
make pytest_loud

# Run specific test file
pytest tests/test_www.py

# Run specific test function
pytest tests/test_www.py::test_root_redirects_to_docs

# Run tests matching a pattern
pytest -k "test_cache"
```

### Coverage Reports

The project is configured to generate test coverage reports automatically:

```bash
# Run tests with coverage (default for make pytest)
pytest --cov=./library --cov-report=term-missing tests

# Generate HTML coverage report
pytest --cov=./library --cov-report=html tests
# Open htmlcov/index.html in your browser

# Show coverage for specific file
pytest --cov=./library/services/cache.py tests/services/test_cache.py
```

### Running Specific Test Types

```bash
# Run only async tests
pytest -m asyncio

# Run tests in parallel (requires pytest-xdist)
pytest -n auto

# Stop on first failure
pytest -x

# Show local variables in tracebacks
pytest -l

# Disable captured output (see prints immediately)
pytest -s
```

## Test Fixtures

Test fixtures provide reusable test setup and teardown logic. This project uses fixtures extensively for database sessions, API clients, and other shared resources.

### Core Fixtures (in conftest.py)

#### CLI Fixtures

**runner**

Provides a Typer CLI test runner for invoking CLI commands:

```python
from typer.testing import CliRunner
from library.cli import app

runner = CliRunner()
```

**Usage Example:**

```python
def test_version_command():
    """Test that version command executes successfully."""
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "library" in result.stdout
```

## Testing Async Code

This project extensively uses async/await. pytest-asyncio provides support for testing async functions.

### Async Test Functions

Mark async test functions with `@pytest.mark.asyncio`:

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test an async function."""
    result = await some_async_function()
    assert result == expected_value
```

### Async Fixtures

Use `@pytest_asyncio.fixture` for async fixtures:

```python
import pytest_asyncio

@pytest_asyncio.fixture
async def async_resource():
    """Create an async resource for testing."""
    resource = await create_resource()
    yield resource
    await cleanup_resource(resource)
```

### Testing Async Context Managers

```python
@pytest.mark.asyncio
async def test_async_context_manager():
    """Test async context manager."""
    async with get_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        assert len(users) >= 0
```

## Mocking and Patching

Use pytest's built-in mocking capabilities along with unittest.mock for mocking dependencies.

### Basic Mocking

```python
from unittest.mock import AsyncMock, MagicMock, patch

@pytest.mark.asyncio
async def test_with_mock():
    """Test with a mocked dependency."""
    mock_service = AsyncMock()
    mock_service.get_data.return_value = {"key": "value"}

    result = await function_using_service(mock_service)
    assert result["key"] == "value"
    mock_service.get_data.assert_called_once()
```

### Patching Functions

```python
@pytest.mark.asyncio
@patch('library.services.cache.get_cached')
async def test_with_patched_cache(mock_get_cached):
    """Test with patched cache function."""
    mock_get_cached.return_value = "cached_value"

    result = await function_using_cache("key")
    assert result == "cached_value"
    mock_get_cached.assert_called_with("key")
```

### Patching Environment Variables

```python
@pytest.mark.asyncio
@patch.dict(os.environ, {"DATABASE_URL": "sqlite+aiosqlite:///:memory:"})
async def test_with_custom_env():
    """Test with custom environment variables."""
    from library.settings import settings
    settings.reload()  # Reload settings with new env vars
    assert settings.database_url == "sqlite+aiosqlite:///:memory:"
```

## Testing Patterns by Feature

### Testing CLI Commands

```python
from typer.testing import CliRunner
from library.cli import app

runner = CliRunner()

def test_cli_command():
    """Test CLI command execution."""
    result = runner.invoke(app, ["command", "--arg", "value"])
    assert result.exit_code == 0
    assert "Expected output" in result.stdout

def test_cli_command_with_error():
    """Test CLI command error handling."""
    result = runner.invoke(app, ["command", "--invalid"])
    assert result.exit_code != 0
    assert "Error" in result.stdout

def test_cli_help():
    """Test CLI help output."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.stdout
```

### Testing Settings

```python
def test_settings_load():
    """Test settings are loaded correctly."""
    from library.settings import settings

    assert settings.project_name == "library"
    assert settings.debug is not None

def test_settings_validation():
    """Test settings validation."""
    import os
    from unittest.mock import patch
    from library.settings import Settings

    with patch.dict(os.environ, {"REQUIRED_VAR": "value"}):
        settings = Settings()
        assert settings.required_var == "value"

def test_settings_with_env_file():
    """Test loading settings from .env file."""
    from library.settings import settings

    # Settings automatically loads from .env if present
    assert hasattr(settings, "project_name")
```

## Test Isolation and Independence

### Principles

1. **Each test is independent**: Tests should not depend on the order of execution
2. **Clean state**: Fixtures ensure each test starts with a clean state
3. **No side effects**: Tests should not affect other tests or external systems
4. **Idempotent**: Running tests multiple times produces the same results

### Database Test Isolation

### Cache Test Isolation

## Coverage Requirements and Best Practices

### Coverage Goals

- **Minimum coverage**: 80% overall
- **Critical paths**: 100% coverage for critical business logic
- **New code**: All new features should include tests

### Checking Coverage

```bash
# Generate coverage report
make pytest

# View coverage for specific file
pytest --cov=./library/services/cache.py tests/services/test_cache.py

# Fail if coverage is below threshold
pytest --cov=./library --cov-fail-under=80 tests
```

### Coverage Configuration

Coverage is configured in `pyproject.toml`:

```toml
[tool.coverage.run]
concurrency = ["thread", "greenlet"]
omit = [
  "./library/_version.py",
]
```

## Best Practices

1. **Write descriptive test names**: Test names should clearly describe what they test

   ```python
   # Good
   def test_user_creation_validates_email_format()

   # Bad
   def test_user()
   ```

2. **One assertion per test**: Keep tests focused on a single behavior

   ```python
   # Good
   def test_user_email_validation():
       assert validate_email("test@example.com") is True

   def test_user_email_validation_rejects_invalid():
       assert validate_email("invalid") is False

   # Bad (multiple unrelated assertions)
   def test_user_stuff():
       assert user.name == "Test"
       assert user.email_valid()
       assert user.age > 0
   ```

3. **Use fixtures for setup**: Avoid duplication by using fixtures

   ```python
   @pytest.fixture
   def sample_user():
       return User(name="Test", email="test@example.com")

   def test_user_name(sample_user):
       assert sample_user.name == "Test"
   ```

4. **Test both success and failure cases**: Test happy paths and error conditions

   ```python
   def test_divide_success():
       assert divide(10, 2) == 5

   def test_divide_by_zero_raises_error():
       with pytest.raises(ZeroDivisionError):
           divide(10, 0)
   ```

5. **Use parametrize for multiple test cases**: Test multiple inputs efficiently

   ```python
   @pytest.mark.parametrize("input,expected", [
       ("test@example.com", True),
       ("invalid", False),
       ("test@", False),
       ("@example.com", False),
   ])
   def test_email_validation(input, expected):
       assert validate_email(input) == expected
   ```

6. **Keep tests fast**: Use in-memory databases, mock external services, avoid sleep

   ```python
   # Good - uses in-memory database
   @pytest.mark.asyncio
   async def test_with_db(db_session):
       result = await query_database(db_session)
       assert result is not None

   # Bad - sleeps unnecessarily
   @pytest.mark.asyncio
   async def test_slow():
       await asyncio.sleep(5)  # Avoid this!
       assert True
   ```

7. **Test edge cases and boundary conditions**: Don't just test happy paths

   ```python
   @pytest.mark.parametrize("value", [0, -1, None, "", [], {}])
   def test_handles_edge_cases(value):
       result = process_value(value)
       assert result is not None
   ```

8. **Use async tests for async code**: Always use `@pytest.mark.asyncio` for async functions

   ```python
   # Good
   @pytest.mark.asyncio
   async def test_async_function():
       result = await async_operation()
       assert result == expected

   # Bad - won't work properly
   def test_async_function():
       result = async_operation()  # This returns a coroutine, not a result!
       assert result == expected
   ```

## Continuous Integration

Tests run automatically on every push and pull request via GitHub Actions. The CI pipeline:

1. **Runs all tests** with coverage reporting
2. **Checks code formatting** with ruff
3. **Performs type checking** with mypy
4. **Validates linting rules** with ruff
5. **Checks data formatting** with dapperdata
6. **Verifies TOML formatting** with toml-sort

See the [GitHub Actions documentation](./github.md) for more details on CI configuration.

## Troubleshooting Tests

### Common Issues

**Import Errors**

```bash
# Make sure the package is installed in development mode
make install
```

**Async Tests Not Running**

```python
# Make sure to mark async tests
@pytest.mark.asyncio
async def test_my_async_function():
    await async_operation()
```

**Database Fixture Issues**

```python
# Ensure you're using the correct fixture
@pytest.mark.asyncio
async def test_db_operation(db_session):  # Not db_session_maker
    result = await db_session.execute(query)
```

**Tests Pass Individually But Fail Together**

This usually indicates test isolation issues. Check:

- Are you cleaning up resources?
- Are tests sharing state through global variables?
- Are database transactions being rolled back?

**Coverage Not Including All Files**

Check `pyproject.toml` coverage configuration and ensure files aren't in the omit list.

## References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing Documentation](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)
