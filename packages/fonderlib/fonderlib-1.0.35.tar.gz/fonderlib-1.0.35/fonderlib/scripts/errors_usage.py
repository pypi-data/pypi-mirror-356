# test_errors.py

from fonderlib.common.error import (
    ConfigError,
    AuthError,
    DatabaseError,
    NotFoundError,
    ValidationError,
    ExternalServiceError,
)


def test_error(error_class, custom_message=None):
    try:
        raise error_class(custom_message)
    except Exception as e:
        print(f"{error_class.__name__} raised:")
        print(f" → Message: {str(e)}")
        print("-" * 40)


def main():
    print("🔍 Testing FonderErrors...\n")

    test_error(ConfigError)
    test_error(AuthError)
    test_error(DatabaseError, "Custom DB error: connection refused.")
    test_error(NotFoundError)
    test_error(ValidationError, "Custom validation failed: 'email' is invalid.")
    test_error(ExternalServiceError)


if __name__ == "__main__":
    main()
