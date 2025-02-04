# Object-Oriented Programming Inheritance Project

## Overview

This project demonstrates advanced object-oriented programming (OOP) concepts in Python, including:
- Class inheritance
- Method overriding
- Multiple inheritance
- Delegation
- Usage of `__slots__`

The project creates a simple system of people (Person, Student, Professor, Employee) with various attributes and behaviors.

## Features

- Base `Person` class with core personal details
- Specialized classes:
  - `Student`: Extends Person with grade information
  - `Professor`: Extends Person with teaching courses
  - `Employee`: Extends Person with department details
- `StudentProfessor`: Demonstrates multiple inheritance
- `Location` class using `__slots__` for efficient memory management

## Requirements

- Python 3.10+
- pytest (for running tests)

## Project Structure

```
project_root/
│
├── your_module.py        # Main implementation of classes
├── test_module.py        # Pytest test cases
└── .github/workflows/
    └── python-app.yml   # GitHub Actions configuration
```

## Setup and Installation

1. Clone the repository
2. Create a virtual environment (optional but recommended)
3. Install dependencies:
   ```bash
   pip install pytest
   ```

## Running Tests

To run the test suite:
```bash
pytest
```

## Continuous Integration

GitHub Actions is configured to automatically run tests on:
- Pushes to the main branch
- Pull requests targeting the main branch

## Learning Objectives

This project helps demonstrate:
- Inheritance principles
- Method overriding
- Multiple inheritance strategies
- Python class design patterns
- Advanced OOP techniques

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[Choose an appropriate license for your project]

## Author

[Your Name]
```

## Key Concepts Demonstrated

- Base class creation
- Inheritance hierarchies
- Method extension and overriding
- Multiple inheritance
- Use of `super()` for method delegation
- Memory-efficient class design with `__slots__`