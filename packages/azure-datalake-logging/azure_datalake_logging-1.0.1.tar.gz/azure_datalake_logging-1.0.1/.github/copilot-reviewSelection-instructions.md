# GitHub Copilot Code Generation Instructions

## Python Code Style

### General Requirements
- Use Python 3.10 or higher
- Include appropriate docstrings for modules, classes, and functions
- Follow object-oriented programming principles where appropriate

### Formatting
- Adhere to PEP8 standards
- Use `snake_case` for variables and function names
- Use `PascalCase` for class names
- Use double quotes for strings
- Indent with 4 spaces (no tabs)
- Use type annotations with the `typing` module
- Limit lines to 80 characters maximum
- Add meaningful comments for complex logic
- Use blank lines to separate logical sections
- Include appropriate exception handling

### Example
```python
def calculate_average(numbers: list[float]) -> float:
    """
    Calculate the average of a list of numbers.

    Args:
        numbers: List of numerical values

    Returns:
        The average of the input numbers

    Raises:
        ValueError: If the list is empty
    """
    if not numbers:
        msg = "Cannot calculate average of empty list"
        raise ValueError(msg)

    return sum(numbers) / len(numbers)
```

### Testing
- Include unit tests for all significant functionality
- Use pytest for testing framework
- Aim for high test coverage

### Libraries and Dependencies
- Prefer standard library solutions when available
- Document external dependencies in requirements.txt
- Use virtual environments for dependency management

### Linting
- Use `ruff` as the primary linter.
- Check for `[tool.ruff.lint]` entries in `pyproject.toml` or rules in `ruff.toml`.
- Follow rule `EM101`: Exception messages must not use string literals directly, assign to a variable first.
- Resolve all linting violations before committing code.
- If `ruff` is unavailable, use an alternative linter that supports `PEP8` compliance.
- Regularly update linting configurations to align with project standards.
- Document custom linting rules or exceptions in the repository.

---

## SQL Code Style (T-SQL)

### Naming Conventions
- Use `snake_case` for database objects (tables, views, columns)
- Use descriptive prefixes for stored procedures and functions
- Include schema name when referencing objects (e.g., `dbo.user_accounts`)

### Formatting
- Write SQL keywords in UPPERCASE
- Use comma-first style for columns
- Indent with 4 spaces
- Start each major clause on a new line
- Use meaningful table aliases
- Align similar elements vertically for readability
- Add comments for complex operations

### Example
```sql
SELECT
      u.user_id
  , u.first_name
  , u.last_name
  , a.email_address
FROM
  dbo.users AS u
INNER JOIN
  dbo.email_addresses AS a
  ON u.user_id = a.user_id
WHERE 1=1
  AND u.is_active = 1
  AND a.is_primary = 1
ORDER BY
    u.last_name
  , u.first_name
;
```

### Query Performance
- Consider query performance in all SQL code
- Avoid SELECT * in production code
- Use appropriate indexing strategies
- Minimize subqueries when possible
- Use CTEs for complex queries rather than nested subqueries
- Consider transaction isolation levels for data modification

### Error Handling
- Include appropriate error handling in stored procedures
- Use TRY/CATCH blocks for transaction management
- Return meaningful error messages
