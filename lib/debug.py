"""Debug utilities for the finance tracker application."""

import logging
import sys
from datetime import datetime
from typing import Dict, List, Any
from contextlib import contextmanager

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.pretty import pprint

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.models import get_db_session, User, Transaction, Budget, SavingsGoal, Tag, UserProfile


class DebugLogger:
    """Enhanced logging for debugging finance tracker operations."""
    
    def __init__(self, log_level=logging.DEBUG):
        self.console = Console()
        self.logger = logging.getLogger('finance_tracker')
        self.logger.setLevel(log_level)
        
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger if not already added
        if not self.logger.handlers:
            self.logger.addHandler(handler)
    
    def log_transaction(self, transaction_data: Dict):
        """Log transaction creation/update."""
        self.logger.info(f"Transaction operation: {transaction_data}")
        
        self.console.print(Panel(
            f"[bold cyan]Transaction Debug[/bold cyan]\n"
            f"Amount: ${transaction_data.get('amount', 'N/A')}\n"
            f"Type: {transaction_data.get('transaction_type', 'N/A')}\n"
            f"Category: {transaction_data.get('category', 'N/A')}\n"
            f"User ID: {transaction_data.get('user_id', 'N/A')}",
            title="Transaction Log",
            border_style="blue"
        ))
    
    def log_budget_status(self, budget_data: Dict):
        """Log budget analysis."""
        self.logger.info(f"Budget analysis: {budget_data}")
        
        spent = budget_data.get('spent', 0)
        limit = budget_data.get('limit_amount', 0)
        remaining = limit - spent
        
        status_color = "green" if remaining >= 0 else "red"
        
        self.console.print(Panel(
            f"[bold yellow]Budget Debug[/bold yellow]\n"
            f"Category: {budget_data.get('category', 'N/A')}\n"
            f"Limit: ${limit}\n"
            f"Spent: ${spent}\n"
            f"Remaining: [{status_color}]${remaining}[/{status_color}]",
            title="Budget Analysis",
            border_style="yellow"
        ))
    
    def log_database_query(self, query_type: str, table: str, filters: Dict = None):
        """Log database operations."""
        filters = filters or {}
        self.logger.debug(f"DB Query - Type: {query_type}, Table: {table}, Filters: {filters}")
        
        if self.logger.level <= logging.DEBUG:
            self.console.print(f"[dim]DB: {query_type} on {table} with {filters}[/dim]")
    
    def log_validation_error(self, field: str, value: Any, error: str):
        """Log validation failures."""
        self.logger.warning(f"Validation failed - Field: {field}, Value: {value}, Error: {error}")
        
        self.console.print(Panel(
            f"[bold red]Validation Error[/bold red]\n"
            f"Field: {field}\n"
            f"Value: {value}\n"
            f"Error: {error}",
            title="Validation Failed",
            border_style="red"
        ))
    
    def log_user_session(self, user_id: int, action: str):
        """Log user session activities."""
        self.logger.info(f"User {user_id} performed action: {action}")
        
        self.console.print(f"[dim cyan]User {user_id}: {action}[/dim cyan]")


# Global debug logger instance
debug_logger = DebugLogger()


@contextmanager
def debug_database_operation(operation_name: str):
    """Context manager for debugging database operations."""
    start_time = datetime.now()
    debug_logger.logger.debug(f"Starting database operation: {operation_name}")
    
    try:
        yield
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        debug_logger.logger.debug(f"Completed {operation_name} in {duration:.3f} seconds")
    except Exception as e:
        debug_logger.logger.error(f"Database operation {operation_name} failed: {str(e)}")
        raise


def print_database_stats():
    """Print comprehensive database statistics."""
    console = Console()
    
    try:
        with get_db_session() as session:
            # Count records in each table
            user_count = session.query(User).count()
            transaction_count = session.query(Transaction).count()
            budget_count = session.query(Budget).count()
            savings_goal_count = session.query(SavingsGoal).count()
            tag_count = session.query(Tag).count()
            profile_count = session.query(UserProfile).count()
            
            # Create stats table
            table = Table(title="Database Statistics", show_header=True, header_style="bold magenta")
            table.add_column("Table", style="cyan", width=20)
            table.add_column("Count", style="green", justify="right")
            
            table.add_row("Users", str(user_count))
            table.add_row("Transactions", str(transaction_count))
            table.add_row("Budgets", str(budget_count))
            table.add_row("Savings Goals", str(savings_goal_count))
            table.add_row("Tags", str(tag_count))
            table.add_row("User Profiles", str(profile_count))
            
            console.print(table)
            
            # Additional stats
            if transaction_count > 0:
                total_income = session.query(Transaction).filter_by(transaction_type='income').count()
                total_expenses = session.query(Transaction).filter_by(transaction_type='expense').count()
                
                console.print(f"\n[cyan]Transaction Breakdown:[/cyan]")
                console.print(f"Income transactions: {total_income}")
                console.print(f"Expense transactions: {total_expenses}")
    
    except Exception as e:
        console.print(f"[red]Error getting database stats: {str(e)}[/red]")


def print_user_debug_info(user_id: int):
    """Print comprehensive debug information for a specific user."""
    console = Console()
    
    try:
        with get_db_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            
            if not user:
                console.print(f"[red]User {user_id} not found[/red]")
                return
            
            # User basic info
            console.print(Panel(
                f"[bold cyan]User Information[/bold cyan]\n"
                f"ID: {user.id}\n"
                f"Name: {user.name}\n"
                f"Email: {user.email}\n"
                f"Currency: {user.default_currency}\n"
                f"Monthly Income: ${user.monthly_income}",
                title=f"User {user_id} Debug",
                border_style="blue"
            ))
            
            # Profile info
            profile = session.query(UserProfile).filter_by(user_id=user_id).first()
            if profile:
                console.print(Panel(
                    f"[bold green]Profile Information[/bold green]\n"
                    f"Phone: {profile.phone_number or 'Not set'}\n"
                    f"Occupation: {profile.occupation or 'Not set'}\n"
                    f"Annual Income: ${profile.annual_income or 0}\n"
                    f"Risk Tolerance: {profile.risk_tolerance}",
                    title="Profile",
                    border_style="green"
                ))
            
            # Transaction summary
            transactions = session.query(Transaction).filter_by(user_id=user_id).all()
            total_income = sum(t.amount for t in transactions if t.transaction_type.value == 'income')
            total_expenses = sum(t.amount for t in transactions if t.transaction_type.value == 'expense')
            
            console.print(Panel(
                f"[bold yellow]Financial Summary[/bold yellow]\n"
                f"Total Transactions: {len(transactions)}\n"
                f"Total Income: ${total_income:.2f}\n"
                f"Total Expenses: ${total_expenses:.2f}\n"
                f"Net Amount: ${total_income - total_expenses:.2f}",
                title="Financial Overview",
                border_style="yellow"
            ))
            
            # Recent transactions
            recent_transactions = session.query(Transaction).filter_by(user_id=user_id)\
                                         .order_by(Transaction.created_at.desc()).limit(5).all()
            
            if recent_transactions:
                table = Table(title="Recent Transactions", show_header=True, header_style="bold magenta")
                table.add_column("Date", style="cyan")
                table.add_column("Type", style="yellow")
                table.add_column("Amount", style="green", justify="right")
                table.add_column("Category", style="blue")
                
                for t in recent_transactions:
                    table.add_row(
                        t.transaction_date.strftime("%Y-%m-%d"),
                        t.transaction_type.value,
                        f"${t.amount:.2f}",
                        t.category
                    )
                
                console.print(table)
    
    except Exception as e:
        console.print(f"[red]Error getting user debug info: {str(e)}[/red]")


def validate_database_integrity():
    """Validate database integrity and relationships."""
    console = Console()
    issues = []
    
    try:
        with get_db_session() as session:
            console.print("[cyan]Checking database integrity...[/cyan]")
            
            # Check for orphaned transactions
            orphaned_transactions = session.query(Transaction).filter(
                ~Transaction.user_id.in_(session.query(User.id))
            ).count()
            
            if orphaned_transactions > 0:
                issues.append(f"Found {orphaned_transactions} orphaned transactions")
            
            # Check for orphaned budgets
            orphaned_budgets = session.query(Budget).filter(
                ~Budget.user_id.in_(session.query(User.id))
            ).count()
            
            if orphaned_budgets > 0:
                issues.append(f"Found {orphaned_budgets} orphaned budgets")
            
            # Check for orphaned savings goals
            orphaned_goals = session.query(SavingsGoal).filter(
                ~SavingsGoal.user_id.in_(session.query(User.id))
            ).count()
            
            if orphaned_goals > 0:
                issues.append(f"Found {orphaned_goals} orphaned savings goals")
            
            # Check for orphaned profiles
            orphaned_profiles = session.query(UserProfile).filter(
                ~UserProfile.user_id.in_(session.query(User.id))
            ).count()
            
            if orphaned_profiles > 0:
                issues.append(f"Found {orphaned_profiles} orphaned user profiles")
            
            # Check for invalid transaction amounts
            invalid_amounts = session.query(Transaction).filter(
                Transaction.amount <= 0
            ).count()
            
            if invalid_amounts > 0:
                issues.append(f"Found {invalid_amounts} transactions with invalid amounts")
            
            # Report results
            if issues:
                console.print(Panel(
                    "\n".join([f"⚠️ {issue}" for issue in issues]),
                    title="Database Integrity Issues",
                    border_style="red"
                ))
            else:
                console.print("[green]✓ Database integrity check passed![/green]")
    
    except Exception as e:
        console.print(f"[red]Error during integrity check: {str(e)}[/red]")


def export_debug_data(user_id: int = None, filename: str = None):
    """Export debug data to a file."""
    import json
    from datetime import date
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"debug_data_{timestamp}.json"
    
    debug_data = {
        "export_timestamp": datetime.now().isoformat(),
        "database_stats": {},
        "users": [],
        "integrity_issues": []
    }
    
    try:
        with get_db_session() as session:
            # Database stats
            debug_data["database_stats"] = {
                "users": session.query(User).count(),
                "transactions": session.query(Transaction).count(),
                "budgets": session.query(Budget).count(),
                "savings_goals": session.query(SavingsGoal).count(),
                "tags": session.query(Tag).count(),
                "profiles": session.query(UserProfile).count()
            }
            
            # User data
            if user_id:
                users = session.query(User).filter_by(id=user_id).all()
            else:
                users = session.query(User).all()
            
            for user in users:
                user_data = user.to_dict()
                
                # Add related data
                user_data["transactions"] = [t.to_dict() for t in user.transactions]
                user_data["budgets"] = [b.to_dict() for b in user.budgets]
                user_data["savings_goals"] = [g.to_dict() for g in user.savings_goals]
                
                if user.profile:
                    user_data["profile"] = user.profile.to_dict()
                
                debug_data["users"].append(user_data)
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(debug_data, f, indent=2, default=str)
        
        console = Console()
        console.print(f"[green]Debug data exported to {filename}[/green]")
    
    except Exception as e:
        console = Console()
        console.print(f"[red]Error exporting debug data: {str(e)}[/red]")


def benchmark_database_operations():
    """Benchmark common database operations."""
    import time
    from rich.progress import Progress, TimeElapsedColumn, BarColumn, TextColumn
    
    console = Console()
    
    operations = [
        ("User Query", lambda s: s.query(User).all()),
        ("Transaction Query", lambda s: s.query(Transaction).all()),
        ("Budget Query", lambda s: s.query(Budget).all()),
        ("Complex Join", lambda s: s.query(Transaction).join(User).all()),
        ("Tag Relationships", lambda s: s.query(Transaction).join(Transaction.tags).all())
    ]
    
    results = []
    
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        
        for name, operation in operations:
            task = progress.add_task(f"Benchmarking {name}", total=100)
            
            times = []
            for i in range(10):  # Run each operation 10 times
                try:
                    with get_db_session() as session:
                        start_time = time.time()
                        operation(session)
                        end_time = time.time()
                        times.append(end_time - start_time)
                except Exception as e:
                    times.append(None)
                    console.print(f"[red]Error in {name}: {str(e)}[/red]")
                
                progress.update(task, advance=10)
            
            # Calculate stats
            valid_times = [t for t in times if t is not None]
            if valid_times:
                avg_time = sum(valid_times) / len(valid_times)
                min_time = min(valid_times)
                max_time = max(valid_times)
                
                results.append({
                    "operation": name,
                    "avg_time": avg_time,
                    "min_time": min_time,
                    "max_time": max_time,
                    "success_rate": len(valid_times) / len(times)
                })
    
    # Display results
    table = Table(title="Database Performance Benchmark", show_header=True, header_style="bold magenta")
    table.add_column("Operation", style="cyan")
    table.add_column("Avg Time (s)", style="green", justify="right")
    table.add_column("Min Time (s)", style="blue", justify="right")
    table.add_column("Max Time (s)", style="yellow", justify="right")
    table.add_column("Success Rate", style="white", justify="right")
    
    for result in results:
        table.add_row(
            result["operation"],
            f"{result['avg_time']:.4f}",
            f"{result['min_time']:.4f}",
            f"{result['max_time']:.4f}",
            f"{result['success_rate']:.1%}"
        )
    
    console.print(table)


if __name__ == "__main__":
    # Demo debug functions
    console = Console()
    
    console.print("[bold cyan]Finance Tracker Debug Utilities[/bold cyan]\n")
    
    # Database stats
    print_database_stats()
    
    # Integrity check
    validate_database_integrity()
    
    # Benchmark (comment out if not needed)
    # benchmark_database_operations()