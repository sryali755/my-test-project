def validate_email(email):
    """Validate email format"""
    return "@" in email and "." in email

def format_name(first_name, last_name):
    """Format full name"""
    return f"{first_name.title()} {last_name.title()}"

def calculate_discount(price, percentage):
    """Calculate discounted price"""
    discount = price * (percentage / 100)
    return price - discount