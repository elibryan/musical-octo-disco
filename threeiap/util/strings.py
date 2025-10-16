import re


def to_snake_case(input_string):
    try:

        # Replace non-alphanumeric characters with a single underscore
        cleaned_string = re.sub(r'[^a-zA-Z0-9]+', '_', input_string)

        # Convert to lowercase and remove leading/trailing underscores
        snake_case_string = cleaned_string.strip('_').lower()

        return snake_case_string
    except:
        return input_string
