# Test Generation Guidelines

## Test Organization
- All test files should be placed in the `./tests/` directory
- Name test files using the pattern: `test_{module_name}.py` (e.g., `test_utils.py`, or `test_subfolder_utils.py` if for files within subfolders)
- Organize tests by module, with each module having its own test file

## Testing Framework
- Use `pytest` as the primary testing framework
- Leverage pytest fixtures when appropriate for test setup
- Use parametrized tests for testing multiple input/output combinations

## Test Structure
- Use descriptive class names that clearly state the test case purpose
- Follow the AAA (Arrange, Act, Assert) pattern for all test cases:
  1. **Arrange**: Set up test prerequisites and inputs
  2. **Act**: Execute the functionality being tested
  3. **Assert**: Verify the expected behavior occurred

## Example Test Structure
```python
# Example test file: ./tests/test_example_module.py
import pytest
from uuid_extension import example_module

class TestExampleFunctionality:
    def test_should_perform_expected_behavior_when_given_valid_input(self):
        # Arrange
        test_input = "valid_input"
        expected_output = "expected_result"

        # Act
        actual_output = example_module.function_under_test(test_input)

        # Assert
        assert actual_output == expected_output
```

## Best Practices
- Write tests before implementing functionality (TDD) when possible
- Each test should focus on testing a single behavior
- Create separate test classes for different groups of functionality
- Keep tests independent and avoid dependencies between tests
- Use meaningful assertions that clearly communicate the expected behavior
