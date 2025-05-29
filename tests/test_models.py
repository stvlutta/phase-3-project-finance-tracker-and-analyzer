"""Tests for database models."""

import pytest
from datetime import date
from finance_tracker.models import User, Transaction, Budget, SavingsGoal, TransactionType


def test_user_creation():
    """Test User model creation."""
    user = User(
        name="John Doe",
        email="john@example.com",
        default_currency="USD",
        monthly_income=5000.0
    )
    
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    assert user.default_currency == "USD"
    assert user.monthly_income == 5000.0


def test_transaction_creation():
    """Test Transaction model creation."""
    transaction = Transaction(
        amount=100.50,
        description="Grocery shopping",
        category="Food",
        transaction_type=TransactionType.EXPENSE,
        transaction_date=date.today(),
        user_id=1
    )
    
    assert transaction.amount == 100.50
    assert transaction.description == "Grocery shopping"
    assert transaction.category == "Food"
    assert transaction.transaction_type == TransactionType.EXPENSE
    assert transaction.user_id == 1


def test_budget_creation():
    """Test Budget model creation."""
    budget = Budget(
        category="Food",
        limit_amount=500.0,
        month="2025-01",
        user_id=1
    )
    
    assert budget.category == "Food"
    assert budget.limit_amount == 500.0
    assert budget.month == "2025-01"
    assert budget.user_id == 1


def test_savings_goal_creation():
    """Test SavingsGoal model creation."""
    goal = SavingsGoal(
        name="Emergency Fund",
        target_amount=10000.0,
        current_amount=2500.0,
        user_id=1
    )
    
    assert goal.name == "Emergency Fund"
    assert goal.target_amount == 10000.0
    assert goal.current_amount == 2500.0
    assert goal.user_id == 1


def test_savings_goal_methods():
    """Test SavingsGoal calculation methods."""
    goal = SavingsGoal(
        name="Vacation",
        target_amount=2000.0,
        current_amount=500.0,
        user_id=1
    )
    
    # Test progress percentage
    assert goal.get_progress_percentage() == 25.0
    
    # Test remaining amount
    assert goal.get_remaining_amount() == 1500.0
    
    # Test contribution
    result = goal.add_contribution(300.0)
    assert result is True
    assert goal.current_amount == 800.0
    
    # Test achievement
    goal.add_contribution(1200.0)
    assert goal.is_achieved is True