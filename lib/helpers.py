"""Helper functions for the finance tracker application."""

import re
from datetime import datetime, date
from typing import Tuple, Union


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency string."""
    if currency == "USD":
        return f"${amount:,.2f}"
    elif currency == "EUR":
        return f"€{amount:,.2f}"
    elif currency == "GBP":
        return f"£{amount:,.2f}"
    else:
        return f"{currency} {amount:,.2f}"


def format_date(date_obj: date) -> str:
    """Format date object as string."""
    if date_obj:
        return date_obj.strftime("%Y-%m-%d")
    return ""


def format_percentage(percentage: float) -> str:
    """Format percentage as string."""
    return f"{percentage:.1f}%"


def validate_amount(amount_str: str) -> Tuple[bool, Union[float, str]]:
    """Validate and convert amount string to float."""
    try:
        # Remove currency symbols and commas
        cleaned = re.sub(r'[$,€£]', '', str(amount_str).strip())
        amount = float(cleaned)
        
        if amount < 0:
            return False, "Amount cannot be negative"
        
        if amount > 1000000000:  # 1 billion limit
            return False, "Amount is too large"
        
        return True, amount
    except ValueError:
        return False, "Invalid amount format. Please enter a valid number."


def validate_email(email: str) -> Tuple[bool, Union[str, str]]:
    """Validate email format."""
    email = email.strip()
    
    if not email:
        return False, "Email cannot be empty"
    
    if len(email) > 255:
        return False, "Email is too long"
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, email.lower()


def validate_category(category: str) -> Tuple[bool, Union[str, str]]:
    """Validate category string."""
    category = category.strip()
    
    if not category:
        return False, "Category cannot be empty"
    
    if len(category) > 100:
        return False, "Category name is too long (max 100 characters)"
    
    # Check for invalid characters
    if re.search(r'[<>"\']', category):
        return False, "Category contains invalid characters"
    
    return True, category.title()  # Capitalize first letter of each word


def validate_date(date_str: str) -> Tuple[bool, Union[date, str]]:
    """Validate and convert date string to date object."""
    try:
        if not date_str:
            return False, "Date cannot be empty"
        
        # Try different date formats
        formats = ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']
        
        for fmt in formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt).date()
                
                # Check if date is reasonable (not too far in past or future)
                today = date.today()
                min_date = date(1900, 1, 1)
                max_date = date(2100, 12, 31)
                
                if parsed_date < min_date:
                    return False, "Date is too far in the past"
                
                if parsed_date > max_date:
                    return False, "Date is too far in the future"
                
                return True, parsed_date
            except ValueError:
                continue
        
        return False, "Invalid date format. Use YYYY-MM-DD"
        
    except Exception:
        return False, "Invalid date format"


def validate_month(month_str: str) -> Tuple[bool, Union[str, str]]:
    """Validate month string in YYYY-MM format."""
    try:
        if not month_str:
            return False, "Month cannot be empty"
        
        # Check format YYYY-MM
        if not re.match(r'^\d{4}-\d{2}$', month_str):
            return False, "Invalid month format. Use YYYY-MM (e.g., 2023-12)"
        
        year, month = month_str.split('-')
        year_int = int(year)
        month_int = int(month)
        
        if year_int < 1900 or year_int > 2100:
            return False, "Year must be between 1900 and 2100"
        
        if month_int < 1 or month_int > 12:
            return False, "Month must be between 01 and 12"
        
        return True, month_str
        
    except Exception:
        return False, "Invalid month format"


def validate_name(name: str) -> Tuple[bool, Union[str, str]]:
    """Validate name string."""
    name = name.strip()
    
    if not name:
        return False, "Name cannot be empty"
    
    if len(name) < 2:
        return False, "Name must be at least 2 characters long"
    
    if len(name) > 100:
        return False, "Name is too long (max 100 characters)"
    
    # Check for invalid characters (allow letters, spaces, hyphens, apostrophes)
    if not re.match(r"^[a-zA-Z\s\-'\.]+$", name):
        return False, "Name contains invalid characters"
    
    # Check for reasonable structure
    if re.match(r'^[\s\-\'\.]+$', name):  # Only special characters
        return False, "Name must contain letters"
    
    return True, name.title()  # Capitalize properly


def validate_description(description: str) -> Tuple[bool, Union[str, str]]:
    """Validate description string."""
    description = description.strip()
    
    # Description can be empty
    if not description:
        return True, ""
    
    if len(description) > 255:
        return False, "Description is too long (max 255 characters)"
    
    # Check for potentially harmful content
    if re.search(r'[<>]', description):
        return False, "Description contains invalid characters"
    
    return True, description


def calculate_compound_interest(principal: float, rate: float, time: float, 
                              compound_frequency: int = 12) -> float:
    """Calculate compound interest."""
    if principal <= 0 or rate < 0 or time < 0:
        return 0.0
    
    # A = P(1 + r/n)^(nt)
    amount = principal * (1 + rate / compound_frequency) ** (compound_frequency * time)
    return round(amount, 2)


def calculate_monthly_payment(principal: float, annual_rate: float, years: int) -> float:
    """Calculate monthly payment for a loan."""
    if principal <= 0 or annual_rate < 0 or years <= 0:
        return 0.0
    
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    
    if monthly_rate == 0:
        return principal / num_payments
    
    payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / \
              ((1 + monthly_rate) ** num_payments - 1)
    
    return round(payment, 2)


def get_budget_status(spent: float, limit: float) -> Tuple[str, str]:
    """Get budget status and color."""
    if limit <= 0:
        return "No limit", "gray"
    
    percentage = (spent / limit) * 100
    
    if percentage <= 50:
        return "Good", "green"
    elif percentage <= 75:
        return "Warning", "yellow"
    elif percentage <= 100:
        return "High", "orange"
    else:
        return "Over", "red"


def get_savings_progress_color(percentage: float) -> str:
    """Get color for savings progress based on percentage."""
    if percentage >= 100:
        return "green"
    elif percentage >= 75:
        return "yellow"
    elif percentage >= 50:
        return "blue"
    else:
        return "red"


def parse_tag_string(tags_str: str) -> list:
    """Parse comma-separated tag string into list."""
    if not tags_str:
        return []
    
    # Split by comma and clean up
    tags = [tag.strip().lower() for tag in tags_str.split(',')]
    
    # Remove empty tags and duplicates
    tags = list(set(tag for tag in tags if tag))
    
    # Validate each tag
    valid_tags = []
    for tag in tags:
        if len(tag) <= 50 and re.match(r'^[a-zA-Z0-9\-_]+$', tag):
            valid_tags.append(tag)
    
    return valid_tags


def calculate_emergency_fund_target(monthly_expenses: float, months: int = 6) -> float:
    """Calculate emergency fund target amount."""
    if monthly_expenses <= 0 or months <= 0:
        return 0.0
    
    return monthly_expenses * months


def get_financial_health_score(income: float, expenses: float, savings: float, 
                              debt: float = 0) -> Tuple[int, str]:
    """Calculate a simple financial health score (0-100)."""
    if income <= 0:
        return 0, "No income data"
    
    # Calculate ratios
    savings_rate = (savings / income) * 100 if income > 0 else 0
    expense_ratio = (expenses / income) * 100 if income > 0 else 0
    debt_ratio = (debt / income) * 100 if income > 0 else 0
    
    score = 100
    
    # Deduct points for high expenses
    if expense_ratio > 80:
        score -= 30
    elif expense_ratio > 60:
        score -= 20
    elif expense_ratio > 50:
        score -= 10
    
    # Deduct points for high debt
    if debt_ratio > 40:
        score -= 25
    elif debt_ratio > 20:
        score -= 15
    elif debt_ratio > 10:
        score -= 5
    
    # Add points for good savings rate
    if savings_rate >= 20:
        score += 10
    elif savings_rate >= 10:
        score += 5
    
    # Ensure score is between 0 and 100
    score = max(0, min(100, score))
    
    # Determine description
    if score >= 80:
        description = "Excellent"
    elif score >= 60:
        description = "Good"
    elif score >= 40:
        description = "Fair"
    elif score >= 20:
        description = "Poor"
    else:
        description = "Critical"
    
    return score, description


def format_large_number(number: float) -> str:
    """Format large numbers with appropriate suffixes."""
    if number >= 1_000_000_000:
        return f"{number/1_000_000_000:.1f}B"
    elif number >= 1_000_000:
        return f"{number/1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number/1_000:.1f}K"
    else:
        return f"{number:.2f}"


def get_transaction_category_emoji(category: str) -> str:
    """Get emoji for transaction category."""
    category_lower = category.lower()
    
    emoji_map = {
        'food': '🍔',
        'groceries': '🛒',
        'transport': '🚗',
        'gas': '⛽',
        'rent': '🏠',
        'utilities': '💡',
        'entertainment': '🎬',
        'shopping': '🛍️',
        'health': '🏥',
        'education': '📚',
        'salary': '💰',
        'bonus': '🎉',
        'investment': '📈',
        'savings': '🏦',
        'insurance': '🛡️',
        'travel': '✈️',
        'gym': '💪',
        'subscription': '📺',
        'coffee': '☕',
        'restaurant': '🍽️'
    }
    
    for key, emoji in emoji_map.items():
        if key in category_lower:
            return emoji
    
    return '📋'  # Default emoji


def validate_phone_number(phone: str) -> Tuple[bool, Union[str, str]]:
    """Validate phone number format."""
    if not phone:
        return True, ""  # Phone is optional
    
    phone = phone.strip()
    
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    
    # Check if it contains only digits
    if not cleaned.isdigit():
        return False, "Phone number should contain only digits and common separators"
    
    # Check length (between 7 and 15 digits is reasonable)
    if len(cleaned) < 7 or len(cleaned) > 15:
        return False, "Phone number should be between 7 and 15 digits"
    
    return True, phone


def validate_hex_color(color: str) -> Tuple[bool, Union[str, str]]:
    """Validate hex color code."""
    if not color:
        return True, "#007bff"  # Default color
    
    color = color.strip()
    
    # Add # if missing
    if not color.startswith('#'):
        color = '#' + color
    
    # Check format
    if not re.match(r'^#[0-9A-Fa-f]{6}$', color):
        return False, "Invalid color format. Use hex format like #FF0000"
    
    return True, color.lower()


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text with ellipsis if too long."""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."