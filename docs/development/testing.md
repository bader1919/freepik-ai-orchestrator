# Testing Strategy and Guide

This document outlines the comprehensive testing strategy for the Freepik AI Orchestrator project, including test types, frameworks, and best practices.

## Table of Contents

- [Testing Philosophy](#testing-philosophy)
- [Test Types](#test-types)
- [Testing Framework](#testing-framework)
- [Test Structure](#test-structure)
- [Writing Tests](#writing-tests)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Continuous Integration](#continuous-integration)
- [Performance Testing](#performance-testing)
- [Security Testing](#security-testing)

## Testing Philosophy

Our testing approach follows these principles:

- **Test-Driven Development (TDD)**: Write tests before implementation
- **Comprehensive Coverage**: Aim for 90%+ code coverage
- **Fast Feedback**: Tests should run quickly and provide immediate feedback
- **Reliable**: Tests should be deterministic and not flaky
- **Maintainable**: Tests should be easy to read and maintain
- **Realistic**: Use realistic test data and scenarios

## Test Types

### 1. Unit Tests

Test individual components in isolation.

**Scope:**
- Individual functions and methods
- Class behavior
- Edge cases and error conditions
- Business logic

**Example:**

```python
import pytest
from unittest.mock import Mock, patch
from freepik_ai_orchestrator.core import AIOrchestrator
from freepik_ai_orchestrator.exceptions import ModelNotFoundError


class TestAIOrchestrator:
    """Unit tests for AIOrchestrator class."""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration for testing."""
        return {
            "openai_api_key": "test-key",
            "default_model": "dall-e-3",
            "timeout": 30
        }
    
    @pytest.fixture
    def orchestrator(self, mock_config):
        """Create orchestrator instance for testing."""
        return AIOrchestrator(mock_config)
    
    def test_initialization(self, orchestrator, mock_config):
        """Test proper initialization of orchestrator."""
        assert orchestrator.config == mock_config
        assert orchestrator.default_model == "dall-e-3"
        assert len(orchestrator.available_models) > 0
    
    @patch('freepik_ai_orchestrator.models.dalle.OpenAI')
    def test_generate_success(self, mock_openai, orchestrator):
        """Test successful content generation."""
        # Setup mock
        mock_response = Mock()
        mock_response.data = [Mock(url="https://example.com/image.jpg")]
        mock_openai.return_value.images.generate.return_value = mock_response
        
        # Execute
        result = orchestrator.generate(
            prompt="A beautiful sunset",
            model="dall-e-3"
        )
        
        # Assert
        assert result is not None
        assert "image_url" in result
        assert result["image_url"] == "https://example.com/image.jpg"
        assert result["model"] == "dall-e-3"
    
    def test_generate_invalid_model(self, orchestrator):
        """Test generation with invalid model raises exception."""
        with pytest.raises(ModelNotFoundError) as exc_info:
            orchestrator.generate(
                prompt="Test prompt",
                model="invalid-model"
            )
        
        assert "invalid-model" in str(exc_info.value)
    
    @pytest.mark.parametrize("prompt,expected_length", [
        ("Short prompt", 50),
        ("A" * 1000, 1000),
        ("", 0)
    ])
    def test_prompt_validation(self, orchestrator, prompt, expected_length):
        """Test prompt validation with various inputs."""
        validated = orchestrator._validate_prompt(prompt)
        assert len(validated) <= 1000  # Max length check
```

### 2. Integration Tests

Test component interactions and API endpoints.

**Scope:**
- API endpoint functionality
- Database interactions
- External service integration
- Workflow testing

**Example:**

```python
import pytest
import requests
from fastapi.testclient import TestClient
from freepik_ai_orchestrator.api import app
from freepik_ai_orchestrator.database import get_db


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def test_db():
    """Create test database session."""
    # Setup test database
    yield test_session
    # Cleanup


class TestGenerationAPI:
    """Integration tests for generation API."""
    
    def test_generate_endpoint_success(self, client):
        """Test successful generation through API."""
        response = client.post(
            "/api/v1/generate",
            json={
                "prompt": "A beautiful landscape",
                "model": "dall-e-3",
                "size": "1024x1024"
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "image_url" in data
        assert data["model"] == "dall-e-3"
    
    def test_generate_endpoint_unauthorized(self, client):
        """Test generation without authentication."""
        response = client.post(
            "/api/v1/generate",
            json={
                "prompt": "Test prompt",
                "model": "dall-e-3"
            }
        )
        
        assert response.status_code == 401
    
    def test_generate_endpoint_validation_error(self, client):
        """Test generation with invalid input."""
        response = client.post(
            "/api/v1/generate",
            json={
                "prompt": "",  # Empty prompt
                "model": "dall-e-3"
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 422
        assert "prompt" in response.json()["detail"][0]["loc"]


class TestWorkflowIntegration:
    """Test complete workflows."""
    
    def test_generate_and_store_workflow(self, client, test_db):
        """Test complete generation and storage workflow."""
        # Generate content
        response = client.post(
            "/api/v1/generate",
            json={
                "prompt": "Test workflow",
                "model": "dall-e-3",
                "store_result": True
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        generation_id = response.json()["id"]
        
        # Verify storage
        stored_response = client.get(
            f"/api/v1/generations/{generation_id}",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert stored_response.status_code == 200
        assert stored_response.json()["id"] == generation_id
```

### 3. End-to-End Tests

Test complete user workflows through the UI.

**Scope:**
- User interface functionality
- Complete user journeys
- Cross-browser compatibility
- Performance under load

**Example:**

```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    """Setup WebDriver for testing."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


class TestStreamlitApp:
    """End-to-end tests for Streamlit application."""
    
    def test_generate_image_workflow(self, driver):
        """Test complete image generation workflow."""
        # Navigate to app
        driver.get("http://localhost:8501")
        
        # Wait for page load
        wait = WebDriverWait(driver, 10)
        prompt_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea"))
        )
        
        # Enter prompt
        prompt_input.send_keys("A beautiful sunset over mountains")
        
        # Select model
        model_select = driver.find_element(By.CSS_SELECTOR, "select")
        model_select.click()
        model_option = driver.find_element(By.XPATH, "//option[text()='DALL-E 3']")
        model_option.click()
        
        # Generate image
        generate_button = driver.find_element(By.XPATH, "//button[text()='Generate']")
        generate_button.click()
        
        # Wait for result
        result_image = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img[src*='generated']"))
        )
        
        assert result_image.is_displayed()
        
    def test_analytics_dashboard(self, driver):
        """Test analytics dashboard functionality."""
        driver.get("http://localhost:8501")
        
        # Navigate to analytics
        analytics_tab = driver.find_element(By.XPATH, "//span[text()='Analytics']")
        analytics_tab.click()
        
        # Verify charts are loaded
        wait = WebDriverWait(driver, 10)
        chart_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".stPlotlyChart"))
        )
        
        assert chart_element.is_displayed()
```

## Testing Framework

### Primary Tools

- **pytest**: Main testing framework
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Mocking utilities
- **pytest-asyncio**: Async test support
- **hypothesis**: Property-based testing
- **factory_boy**: Test data factories

### Installation

```bash
pip install pytest pytest-cov pytest-mock pytest-asyncio hypothesis factory_boy selenium
```

### Configuration

**pytest.ini:**

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --cov=freepik_ai_orchestrator
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=90
    --strict-markers
    --disable-warnings
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
    external: Tests requiring external services
```

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests
│   ├── test_orchestrator.py
│   ├── test_models/
│   │   ├── test_dalle.py
│   │   ├── test_midjourney.py
│   │   └── test_stable_diffusion.py
│   ├── test_utils/
│   │   ├── test_image_processing.py
│   │   └── test_analytics.py
│   └── test_api/
│       ├── test_auth.py
│       └── test_endpoints.py
├── integration/             # Integration tests
│   ├── test_api_integration.py
│   ├── test_database.py
│   └── test_workflows.py
├── e2e/                     # End-to-end tests
│   ├── test_streamlit_app.py
│   └── test_user_journeys.py
├── performance/             # Performance tests
│   ├── test_load.py
│   └── test_stress.py
├── security/                # Security tests
│   ├── test_auth_security.py
│   └── test_input_validation.py
├── fixtures/                # Test data and fixtures
│   ├── sample_images/
│   ├── mock_responses.json
│   └── test_data.py
└── utils/                   # Test utilities
    ├── factories.py
    ├── helpers.py
    └── mocks.py
```

## Writing Tests

### Test Fixtures

**conftest.py:**

```python
import pytest
import tempfile
from unittest.mock import Mock
from freepik_ai_orchestrator.core import AIOrchestrator
from freepik_ai_orchestrator.database import Base, engine


@pytest.fixture(scope="session")
def test_config():
    """Test configuration."""
    return {
        "openai_api_key": "test-key",
        "anthropic_api_key": "test-key",
        "default_model": "dall-e-3",
        "database_url": "sqlite:///test.db",
        "redis_url": "redis://localhost:6379/1"
    }


@pytest.fixture
def temp_directory():
    """Create temporary directory for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    mock_response = Mock()
    mock_response.data = [
        Mock(url="https://example.com/generated_image.jpg")
    ]
    return mock_response


@pytest.fixture(scope="function")
def test_database():
    """Create test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
```

### Data Factories

**tests/utils/factories.py:**

```python
import factory
from factory import fuzzy
from datetime import datetime
from freepik_ai_orchestrator.models import Generation, User


class UserFactory(factory.Factory):
    """Factory for User model."""
    
    class Meta:
        model = User
    
    id = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.id}@example.com")
    api_key = factory.LazyFunction(lambda: f"sk-{factory.Faker('uuid4')}")
    created_at = factory.LazyFunction(datetime.utcnow)
    is_active = True


class GenerationFactory(factory.Factory):
    """Factory for Generation model."""
    
    class Meta:
        model = Generation
    
    id = factory.LazyFunction(lambda: factory.Faker('uuid4').generate())
    prompt = factory.Faker('sentence', nb_words=10)
    model = fuzzy.FuzzyChoice(['dall-e-3', 'midjourney', 'stable-diffusion'])
    image_url = factory.LazyAttribute(
        lambda obj: f"https://example.com/{obj.id}.jpg"
    )
    user = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(datetime.utcnow)
    processing_time = fuzzy.FuzzyFloat(1.0, 30.0)
    cost = fuzzy.FuzzyFloat(0.01, 1.0)
```

### Property-Based Testing

```python
from hypothesis import given, strategies as st
from freepik_ai_orchestrator.utils import validate_prompt


class TestPromptValidation:
    """Property-based tests for prompt validation."""
    
    @given(st.text(min_size=1, max_size=1000))
    def test_validate_prompt_length(self, prompt):
        """Test prompt validation with various string lengths."""
        result = validate_prompt(prompt)
        assert len(result) <= 1000
        assert isinstance(result, str)
    
    @given(st.text().filter(lambda x: len(x.strip()) == 0))
    def test_validate_empty_prompt(self, empty_prompt):
        """Test validation rejects empty prompts."""
        with pytest.raises(ValueError):
            validate_prompt(empty_prompt)
    
    @given(st.text(alphabet=st.characters(blacklist_categories=['Cc'])))
    def test_validate_prompt_characters(self, prompt):
        """Test prompt validation handles various characters."""
        if len(prompt.strip()) > 0:
            result = validate_prompt(prompt)
            assert result is not None
```

## Running Tests

### Local Testing

```bash
# Run all tests
pytest

# Run specific test type
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Run with coverage
pytest --cov=freepik_ai_orchestrator

# Run specific test file
pytest tests/unit/test_orchestrator.py

# Run specific test method
pytest tests/unit/test_orchestrator.py::TestAIOrchestrator::test_generate_success

# Run tests with specific markers
pytest -m "unit"
pytest -m "not slow"
pytest -m "integration and not external"

# Run tests in parallel
pytest -n auto

# Run tests with verbose output
pytest -v

# Stop on first failure
pytest -x
```

### Test Environment Variables

```bash
# Set test environment
export TESTING=true
export TEST_DATABASE_URL=sqlite:///test.db
export TEST_REDIS_URL=redis://localhost:6379/1

# Disable external API calls
export MOCK_EXTERNAL_APIS=true
```

## Test Coverage

### Coverage Configuration

**.coveragerc:**

```ini
[run]
source = freepik_ai_orchestrator
omit = 
    */tests/*
    */venv/*
    */migrations/*
    setup.py
    conftest.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:

[html]
directory = htmlcov
```

### Coverage Targets

- **Overall**: 90% minimum
- **Critical modules**: 95% minimum
- **New code**: 100% coverage required

### Viewing Coverage

```bash
# Generate HTML coverage report
pytest --cov=freepik_ai_orchestrator --cov-report=html

# Open coverage report
open htmlcov/index.html

# Generate console report
pytest --cov=freepik_ai_orchestrator --cov-report=term-missing
```

## Continuous Integration

### GitHub Actions Configuration

**.github/workflows/test.yml:**

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    services:
      redis:
        image: redis:6
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88
    
    - name: Type check with mypy
      run: mypy freepik_ai_orchestrator/
    
    - name: Test with pytest
      run: |
        pytest --cov=freepik_ai_orchestrator --cov-report=xml
      env:
        TESTING: true
        REDIS_URL: redis://localhost:6379/1
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

## Performance Testing

### Load Testing

```python
import pytest
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor


class TestPerformance:
    """Performance tests for API endpoints."""
    
    @pytest.mark.slow
    def test_generation_performance(self):
        """Test generation endpoint performance under load."""
        import time
        
        def make_request():
            response = requests.post(
                "http://localhost:8000/api/v1/generate",
                json={
                    "prompt": "Performance test",
                    "model": "dall-e-3"
                },
                headers={"Authorization": "Bearer test-token"}
            )
            return response.elapsed.total_seconds()
        
        # Measure response times
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(100)]
            times = [future.result() for future in futures]
        
        # Assert performance criteria
        avg_time = sum(times) / len(times)
        max_time = max(times)
        
        assert avg_time < 5.0  # Average under 5 seconds
        assert max_time < 15.0  # Max under 15 seconds
        assert sum(1 for t in times if t < 2.0) / len(times) > 0.8  # 80% under 2s
    
    @pytest.mark.asyncio
    async def test_concurrent_generations(self):
        """Test concurrent generation handling."""
        async def make_async_request(session):
            async with session.post(
                "http://localhost:8000/api/v1/generate",
                json={
                    "prompt": "Concurrent test",
                    "model": "dall-e-3"
                },
                headers={"Authorization": "Bearer test-token"}
            ) as response:
                return await response.json()
        
        async with aiohttp.ClientSession() as session:
            tasks = [make_async_request(session) for _ in range(50)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Verify all requests succeeded
        successful = [r for r in results if not isinstance(r, Exception)]
        assert len(successful) >= 45  # At least 90% success rate
```

### Memory and Resource Testing

```python
import psutil
import pytest
from memory_profiler import profile


class TestResourceUsage:
    """Test memory and resource usage."""
    
    def test_memory_usage_generation(self):
        """Test memory usage during generation."""
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        
        # Perform multiple generations
        for i in range(10):
            result = orchestrator.generate(
                prompt=f"Test generation {i}",
                model="dall-e-3"
            )
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (under 100MB)
        assert memory_increase < 100 * 1024 * 1024
    
    @profile
    def test_memory_profile_generation(self):
        """Profile memory usage during generation."""
        # This will output memory usage line by line
        result = orchestrator.generate(
            prompt="Memory profile test",
            model="dall-e-3"
        )
        return result
```

## Security Testing

### Input Validation Tests

```python
class TestSecurityValidation:
    """Security tests for input validation."""
    
    @pytest.mark.parametrize("malicious_input", [
        "<script>alert('xss')</script>",
        "'; DROP TABLE users; --",
        "{{config.__class__.__init__.__globals__}}",
        "../../../etc/passwd",
        "\x00\x01\x02\x03"
    ])
    def test_malicious_input_rejection(self, client, malicious_input):
        """Test rejection of malicious inputs."""
        response = client.post(
            "/api/v1/generate",
            json={
                "prompt": malicious_input,
                "model": "dall-e-3"
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        # Should either reject with 422 or sanitize the input
        if response.status_code == 200:
            # If accepted, verify input was sanitized
            result = response.json()
            assert malicious_input not in str(result)
        else:
            assert response.status_code == 422
    
    def test_authentication_required(self, client):
        """Test that authentication is required."""
        response = client.post(
            "/api/v1/generate",
            json={
                "prompt": "Test prompt",
                "model": "dall-e-3"
            }
        )
        
        assert response.status_code == 401
    
    def test_rate_limiting(self, client):
        """Test rate limiting protection."""
        # Make many requests quickly
        responses = []
        for i in range(100):
            response = client.post(
                "/api/v1/generate",
                json={
                    "prompt": f"Rate limit test {i}",
                    "model": "dall-e-3"
                },
                headers={"Authorization": "Bearer test-token"}
            )
            responses.append(response)
        
        # Should see some rate limiting responses
        rate_limited = [r for r in responses if r.status_code == 429]
        assert len(rate_limited) > 0
```

## Best Practices

### 1. Test Organization

- Group related tests in classes
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Keep tests independent and isolated

### 2. Mock External Dependencies

```python
@patch('freepik_ai_orchestrator.external.openai_client')
def test_with_mocked_openai(mock_client):
    """Test with mocked external dependency."""
    mock_client.generate.return_value = {"url": "test.jpg"}
    # Test implementation
```

### 3. Use Parameterized Tests

```python
@pytest.mark.parametrize("model,expected_provider", [
    ("dall-e-3", "openai"),
    ("midjourney", "midjourney"),
    ("stable-diffusion", "stability")
])
def test_model_providers(model, expected_provider):
    """Test model provider mapping."""
    provider = get_provider_for_model(model)
    assert provider == expected_provider
```

### 4. Test Edge Cases

- Empty inputs
- Maximum/minimum values
- Invalid data types
- Network failures
- Timeouts

### 5. Performance Considerations

- Mark slow tests appropriately
- Use fixtures for expensive setup
- Clean up resources properly
- Consider parallel test execution

## Debugging Tests

### Running Specific Tests

```bash
# Run failed tests only
pytest --lf

# Run tests with debugging
pytest --pdb

# Run with extra verbose output
pytest -vvv

# Disable capturing for debugging
pytest -s
```

### Test Debugging Tools

```python
# Use pytest debugging
def test_debug_example():
    import pdb; pdb.set_trace()  # Debugger breakpoint
    # Test code here

# Use logging in tests
import logging
logging.basicConfig(level=logging.DEBUG)

def test_with_logging():
    logger = logging.getLogger(__name__)
    logger.debug("Debug information")
    # Test code here
```

This comprehensive testing strategy ensures high-quality, reliable software with good coverage and proper validation of all functionality.
