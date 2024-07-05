def validate_signup_fields(data):
    """
    Validates to see if all fields are present in the json returned by the signup endpoint

    Args:
        data (json): Data returned from the signup form

    Returns:
        tuple(bool, str | None): Determines if all fields are present
    """
    required_fields = ["first_name", "last_name", "email", "password", "confirm_password"]
    
    for field in required_fields:
        if field not in data or data.get(field) == "":
            return False, field
    return True, None

def validate_confirm_password(data):
    """
    Checks to see if the password and confirm password fields match

    Args:
        data (json): Data returned from the signup form

    Returns:
        bool: Determines if the password and confirm password fields are the same
    """
    return data.get('password') == data.get('confirm_password')