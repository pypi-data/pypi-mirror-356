# CLAUDE.md

## Development Commands

```bash
# Testing
python -m pytest tests/ -v

# Code Quality  
mypy flake8_elegant_objects/
ruff check flake8_elegant_objects/
ruff format flake8_elegant_objects/

# Plugin Usage
python -m flake8_elegant_objects --show-source path/to/files/*.py
flake8 --select=EO path/to/files/
```

## Architecture

Flake8 plugin enforcing Elegant Objects principles (14 error codes EO001-EO014).

**Core Components:**
- `__init__.py`: ElegantObjectsPlugin orchestrating analysis
- `base.py`: Principles base class, Violations type, ErrorCodes
- `naming.py`: NoErNamePrinciple (EO001-EO004) 
- `core.py`: CorePrinciples (EO005-EO008)
- `advanced.py`: AdvancedPrinciples (EO009-EO014)

**Pattern:** Plugin uses Principles which provides Violations (no None)

## Elegant Objects Principles

**MUST follow:**
- No null (None) - use empty lists instead
- No code in constructors  
- No getters/setters
- No mutable objects
- NO "-ER" NAMES: Manager, Controller, Helper, Handler, Parser, etc
- No static methods
- No instanceof/type casting  
- No public methods without contracts
- No statements in test methods except assertThat
- No ORM/ActiveRecord
- No implementation inheritance

**Philosophy:**
- Objects are living partners, not data containers
- Declarative over imperative (`new Sorted(apples)` not `new Sorter().sort(apples)`)
- Fail fast with exceptions, not null checks
- Composition over inheritance
- Immutability implied by design, not keywords

## Code Style

- No useless comments
- Types: `Violations = list[Violation]`
- Return empty lists `[]` instead of `None`
- Extend lists instead of checking for None