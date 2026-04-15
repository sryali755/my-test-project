def calculate_age(birth_year):
    """Calculate age from birth year"""
    current_year = 2026
    return current_year - birth_year

class User:
    """User class for managing user data"""
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def get_info(self):
        return f"{self.name} ({self.email})"

if __name__ == "__main__":
    user = User("John Doe", "john@example.com")
    print(greet(user.name))
    print(f"Age: {calculate_age(1990)}")