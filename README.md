# Personal Finance Tracker CLI

A comprehensive command-line application for tracking personal finances, built with Python, SQLAlchemy ORM, Click CLI framework, and Rich for enhanced terminal output.

## Features

- **Transaction Management**: Track income and expenses with categories, descriptions, and tags
- **Budget Planning**: Set monthly budgets and monitor spending with visual progress indicators
- **Savings Goals**: Create and track progress towards financial goals with progress bars
- **Tag System**: Organize transactions with a flexible many-to-many tagging system
- **User Profiles**: Extended user information with preferences and settings
- **Financial Reports**: Generate detailed monthly financial reports with category breakdowns
- **User Management**: Multi-user support with individual data isolation
- **Rich CLI Interface**: Beautiful tables, progress bars, panels, and colors
- **Database Seeding**: Sample data generation for testing and development
- **Debug Tools**: Comprehensive debugging and performance monitoring utilities

## Project Structure

This project follows Phase 3 requirements with the standardized structure:

```
├── Pipfile
├── Pipfile.lock
├── README.md
├── alembic.ini         # Alembic configuration
└── lib
    ├── cli.py          # Complete CLI interface with Click commands
    ├── db
    │   ├── models.py   # All database models and relationships
    │   ├── seed.py     # Database seeding utilities
    │   └── migrations/ # Alembic database migrations
    │       ├── env.py
    │       ├── README
    │       ├── script.py.mako
    │       └── versions/
    ├── debug.py        # Debug and monitoring tools
    └── helpers.py      # Utility functions and validators
```

### Phase 3 Requirements Compliance

- ✅ **Pipenv Configuration**: Virtual environment with project-specific dependencies
- ✅ **External Libraries**: SQLAlchemy, Click, Rich, Alembic integration
- ✅ **SQLAlchemy ORM**: 6 related database tables with comprehensive relationships
- ✅ **Alembic Migrations**: Database schema versioning and migration management
- ✅ **One-to-Many Relationships**: User → Transactions, Budgets, SavingsGoals
- ✅ **Many-to-Many Relationships**: Transaction ↔ Tags with association table
- ✅ **One-to-One Relationships**: User ↔ UserProfile
- ✅ **CLI Best Practices**: Rich formatting, input validation, error handling
- ✅ **Data Structures**: Extensive use of lists, dicts, and tuples
- ✅ **Proper Project Structure**: Organized lib directory with clear separation of concerns

## Database Schema

### Tables and Relationships

1. **User** (users)
   - Primary table for user accounts
   - Fields: id, name, email, default_currency, monthly_income, created_at, updated_at
   - One-to-many: transactions, budgets, savings_goals
   - One-to-one: profile (UserProfile)

2. **UserProfile** (user_profiles)
   - Extended user information and preferences
   - Fields: id, user_id, phone_number, address, occupation, annual_income, financial_goal, risk_tolerance, currency_preference, notifications_enabled, dark_mode
   - One-to-one relationship with User

3. **Transaction** (transactions)
   - Records income and expense transactions
   - Fields: id, amount, description, category, transaction_type, transaction_date, user_id, created_at, updated_at
   - Foreign key: user_id → users.id
   - Many-to-many: tags (Tag)

4. **Tag** (tags)
   - Flexible tagging system for transactions
   - Fields: id, name, description, color, created_at, updated_at
   - Many-to-many: transactions (Transaction)

5. **TransactionTags** (transaction_tags)
   - Association table for Transaction ↔ Tag many-to-many relationship
   - Fields: transaction_id, tag_id

6. **Budget** (budgets)
   - Monthly spending limits by category
   - Fields: id, category, limit_amount, month, description, user_id, created_at, updated_at
   - Foreign key: user_id → users.id

7. **SavingsGoal** (savings_goals)
   - Financial targets and progress tracking
   - Fields: id, name, target_amount, current_amount, description, is_achieved, user_id, created_at, updated_at
   - Foreign key: user_id → users.id

## Installation

1. **Clone and Setup**:
   ```bash
   cd "finance tracker"
   pipenv install
   pipenv shell
   ```

2. **Initialize Database**:
   ```bash
   # Using Alembic migrations (recommended)
   python3 -m lib.cli init
   
   # Or without Alembic
   python3 -m lib.cli init --no-alembic
   ```

3. **Seed Database with Sample Data** (Optional):
   ```bash
   python3 lib/db/seed.py seed
   ```

## Usage

### Initial Setup

```bash
# Initialize the database
python3 -m lib.cli init

# Seed with sample data (optional)
python3 lib/db/seed.py seed

# Create or login to user account
python3 -m lib.cli login

# Create user profile
python3 -m lib.cli create-profile --occupation "Software Engineer" --annual-income 75000
```

### Command-Line Interface

#### Transaction Management
```bash
# Add basic transactions
python3 -m lib.cli add-transaction --amount 2500 --category "Salary" --description "Monthly salary" --type income

# Add transactions with tags
python3 -m lib.cli add-transaction-with-tags --amount 150 --category "Groceries" --description "Weekly shopping" --type expense --tags "food,weekly"

# View transactions (with Rich formatting)
python3 -m lib.cli view-transactions --limit 10
```

#### Tag Management
```bash
# Create tags
python3 -m lib.cli add-tag --name "work" --description "Work-related expenses" --color "#ff6b6b"
python3 -m lib.cli add-tag --name "food" --description "Food and dining" --color "#4ecdc4"
```

#### Budget Management
```bash
# Manage budgets
python3 -m lib.cli add-budget --category "Groceries" --limit 500
python3 -m lib.cli view-budgets  # Rich table with progress indicators
```

#### Savings Goals
```bash
# Savings goals with progress bars
python3 -m lib.cli add-savings-goal --name "Emergency Fund" --target 10000
python3 -m lib.cli update-savings-goal --name "Emergency Fund" --amount 500
python3 -m lib.cli view-savings-goals  # Rich table with progress bars
```

#### User Profile
```bash
# View profile (Rich panel)
python3 -m lib.cli view-profile

# Update profile
python3 -m lib.cli create-profile --phone "555-1234" --address "123 Main St"
```

#### Reports
```bash
# Generate reports
python3 -m lib.cli generate-report --month 2025-01
```

### Interactive Mode

```bash
# Start interactive menu interface with enhanced Rich formatting
python3 -m lib.cli interactive
```

The interactive mode includes:
- Rich formatted menus and prompts
- Tag management options
- Profile creation and viewing
- Enhanced transaction entry with tag support

### Database Management

#### Sample Data
```bash
# Seed database with sample data
python3 lib/db/seed.py seed

# Clear all data
python3 lib/db/seed.py clear

# Reset and reseed
python3 lib/db/seed.py reset
```

#### Alembic Migrations
```bash
# Initialize database with migrations
python3 -m lib.cli init

# Create a new migration after model changes
python3 -m lib.cli create-migration -m "Add new field to user model"

# Apply migrations
python3 -m lib.cli migrate

# Show migration history
python3 -m lib.cli migration-history

# Show current migration revision
python3 -m lib.cli migration-current

# Apply specific revision
python3 -m lib.cli migrate --revision abc123

# Alternative: Use Alembic directly
PYTHONPATH=lib alembic revision --autogenerate -m "Migration message"
PYTHONPATH=lib alembic upgrade head
```

### Debug and Monitoring

```bash
# Database statistics and integrity check
python3 lib/debug.py

# Export debug data
python3 -c "from lib.debug import export_debug_data; export_debug_data()"
```

## Rich CLI Enhancements

The application features beautiful terminal output using the Rich library:

### Rich Tables
- **Transactions**: Colorized tables with date, type, amount, category, description, and tags
- **Budgets**: Progress indicators showing spent vs. allocated amounts
- **Savings Goals**: Visual progress bars showing completion percentage

### Rich Panels
- **User Profile**: Formatted panels displaying user information and preferences
- **Reports**: Structured financial summaries with categorized breakdowns

### Rich Progress Bars
- **Savings Goals**: Visual progress bars with color coding (red < 50%, blue 50-75%, yellow 75-100%, green 100%+)
- **Budget Status**: Progress indicators for budget utilization

### Rich Colors & Styling
- **Success Messages**: Green text for successful operations
- **Warnings**: Yellow text for warnings and notices
- **Errors**: Red text for error messages
- **Income**: Green highlighting for income transactions
- **Expenses**: Red highlighting for expense transactions

## Data Structures Used

The application extensively uses Python's built-in data structures:

### Lists
- Transaction collections for reporting and analysis
- Budget lists for category management
- Savings goals tracking for multiple objectives
- Tag collections for transaction categorization
- Menu options in interactive CLI
- Tag name lists for transaction tagging

### Dictionaries
- Model serialization (`to_dict()` methods on all models)
- Financial report data aggregation
- Category-based expense/income grouping using `defaultdict`
- Configuration and validation result storage
- User profile data management
- Tag metadata and color information

### Tuples
- Validation function return values (status, result)
- Database query result processing
- Sorted financial data for reports
- Menu choice handling
- Relationship data in many-to-many associations

## Code Examples

### Using Lists for Tag Management
```python
# Filter transactions by tags
def get_transactions_by_tags(tag_names: List[str]) -> List[Transaction]:
    tag_list = session.query(Tag).filter(Tag.name.in_(tag_names)).all()
    transactions = []
    for tag in tag_list:
        transactions.extend(tag.transactions)
    return list(set(transactions))  # Remove duplicates

# Add multiple tags to transaction
tag_names = ["work", "recurring", "salary"]
cli_app.add_transaction_with_tags(5000, "Salary", "Monthly pay", "income", tag_names)
```

### Using Dictionaries for Enhanced Reports
```python
# Enhanced category breakdown with tag analysis
category_data = defaultdict(lambda: {"amount": 0.0, "tags": defaultdict(float)})

for transaction in transactions:
    cat = transaction.category
    category_data[cat]["amount"] += transaction.amount
    
    # Track spending by tags within categories
    for tag in transaction.tags:
        category_data[cat]["tags"][tag.name] += transaction.amount

# Generate comprehensive report dict
report_data = {
    'month': month,
    'totals': {'income': total_income, 'expenses': total_expenses},
    'categories': dict(category_data),
    'top_tags': dict(sorted(tag_totals.items(), key=lambda x: x[1], reverse=True)[:5]),
    'user_profile': user.profile.to_dict() if user.profile else {}
}
```

### Using Tuples for Validation
```python
def validate_amount(amount_str: str) -> Tuple[bool, Union[float, str]]:
    """Validate and convert amount string to float."""
    try:
        cleaned = re.sub(r'[$,€£]', '', str(amount_str).strip())
        amount = float(cleaned)
        if amount < 0:
            return False, "Amount cannot be negative"
        return True, amount
    except ValueError:
        return False, "Invalid amount format"

# Usage with tuple unpacking
is_valid, result = validate_amount("100.50")
if is_valid:
    process_amount(result)  # result is float
else:
    print(f"Error: {result}")  # result is error message
```

## Architecture

### File Structure

#### `lib/cli.py`
Complete CLI interface containing:
- Click command definitions and CLI groups
- FinanceTrackerCLI class with all business logic
- Rich formatting for tables, panels, and progress bars
- Interactive mode with menu-driven interface
- User session management and validation

#### `lib/db/models.py`
Database layer containing:
- SQLAlchemy Base and engine configuration
- All model classes (User, Transaction, Budget, SavingsGoal, Tag, UserProfile)
- Relationship definitions (one-to-one, one-to-many, many-to-many)
- Database session management
- Model methods and utilities

#### `lib/helpers.py`
Utility functions including:
- Input validation functions (email, amount, date, etc.)
- Formatting functions (currency, date, percentage)
- Financial calculations (compound interest, loan payments)
- Data parsing and manipulation utilities
- Type conversion and sanitization

#### `lib/debug.py`
Debug and monitoring tools:
- Enhanced logging with Rich output
- Database statistics and integrity checking
- Performance benchmarking
- Debug data export functionality
- Database operation profiling

#### `lib/db/seed.py`
Database seeding utilities:
- Sample user and profile generation
- Realistic transaction data creation
- Budget and savings goal templates
- Tag system population
- Database reset and cleanup functions

### Key Design Patterns

1. **Repository Pattern**: Database operations encapsulated in model methods
2. **Factory Pattern**: Model creation from dictionaries and sample data
3. **Command Pattern**: CLI commands with clear separation of concerns
4. **Validation Pattern**: Consistent tuple-based validation returns
5. **Observer Pattern**: Rich progress updates for long-running operations
6. **Decorator Pattern**: Rich styling and formatting decorators

### SQLAlchemy Relationships Implemented

#### One-to-Many Relationships
```python
# User → Transactions, Budgets, SavingsGoals
class User(BaseModel):
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")
    savings_goals = relationship("SavingsGoal", back_populates="user", cascade="all, delete-orphan")
```

#### Many-to-Many Relationships
```python
# Transaction ↔ Tags with association table
transaction_tags = Table(
    'transaction_tags', Base.metadata,
    Column('transaction_id', Integer, ForeignKey('transactions.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

class Transaction(BaseModel):
    tags = relationship('Tag', secondary='transaction_tags', back_populates='transactions')
```

#### One-to-One Relationships
```python
# User ↔ UserProfile
class User(BaseModel):
    profile = relationship("UserProfile", back_populates="user", cascade="all, delete-orphan", uselist=False)

class UserProfile(BaseModel):
    user = relationship("User", back_populates="profile", uselist=False)
```

## External Libraries Integration

### Pipenv Dependencies
```toml
[packages]
sqlalchemy = "*"    # ORM and database management
click = "*"         # CLI framework
rich = "*"          # Terminal formatting and styling

[dev-packages]
pytest = "*"        # Testing framework
pytest-cov = "*"    # Coverage reporting
black = "*"         # Code formatting
flake8 = "*"        # Linting
```

### Library Usage Examples

#### Rich Integration
```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Create Rich console
console = Console()

# Rich tables for data display
table = Table(title="Transactions", show_header=True)
table.add_column("Date", style="cyan")
table.add_column("Amount", style="green", justify="right")
console.print(table)

# Rich panels for information display
panel = Panel("User Profile Information", title="Profile", border_style="blue")
console.print(panel)
```

#### Click CLI Framework
```python
import click

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Personal Finance Tracker CLI"""
    pass

@cli.command()
@click.option('--amount', prompt='Amount', help='Transaction amount')
def add_transaction(amount):
    """Add a new transaction."""
    # Implementation with validation and Rich output
```

#### SQLAlchemy ORM
```python
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class Transaction(BaseModel):
    amount = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="transactions")
    tags = relationship('Tag', secondary='transaction_tags', back_populates='transactions')
```

## Development and Testing

### Sample Data Generation
The seeding system creates realistic financial data:
- 5 sample users with complete profiles
- 6 months of transaction history with realistic patterns
- Appropriate tag assignments and relationships
- Monthly budgets and savings goals with progress

### Debug Tools
Comprehensive debugging utilities:
- Database integrity validation
- Performance benchmarking
- Data export for analysis
- Real-time operation logging

### Testing Commands
```bash
# Activate virtual environment
pipenv shell

# Initialize database
python3 -m lib.cli init

# Run with sample data
python3 lib/db/seed.py seed

# Test CLI commands
python3 -m lib.cli login --name "John Doe" --email "john.doe@example.com"
python3 -m lib.cli view-transactions
python3 -m lib.cli view-budgets
python3 -m lib.cli view-savings-goals

# Debug and monitor
python3 lib/debug.py

# Test Alembic migrations
python3 -m lib.cli migration-current
python3 -m lib.cli migration-history
```

## Contributing

This project demonstrates comprehensive Phase 3 Python development skills including:

- **Pipenv Environment Management**: Project-specific dependency management
- **External Library Integration**: SQLAlchemy, Click, Rich
- **SQLAlchemy ORM**: Complex database relationships and schema design
- **Database Relationships**: One-to-one, one-to-many, many-to-many implementations
- **CLI Best Practices**: Rich formatting, input validation, error handling
- **Data Structure Mastery**: Strategic use of lists, dicts, and tuples
- **Project Organization**: Clean separation of concerns with lib structure
- **Development Tools**: Seeding, debugging, and monitoring utilities

## License

MIT License - See LICENSE file for details