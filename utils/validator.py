def input_with_validation(prompt, validation_fn, error_message="Invalid input. Please try again."):
    while True:
        value = input(prompt).strip()
        if validation_fn(value):
            return value
        print(error_message)


def valid_integer(value):
    try:
        return int(value) > 0
    except ValueError:
        return False


def valid_float(value):
    try:
        return float(value) > 0
    except ValueError:
        return False


def valid_string(value):
    return len(value.strip()) > 0


def yes_or_no(value):
    return value.lower() in ['yes', 'no']
