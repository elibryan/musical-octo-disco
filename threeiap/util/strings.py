import base64
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


def encode_to_base64_url_safe(input_string):
    # Encode the string to bytes using UTF-8
    string_bytes = input_string.encode('utf-8')

    # Encode the bytes to Base64
    base64_bytes = base64.urlsafe_b64encode(string_bytes)

    # Decode the Base64 bytes back to a string
    base64_string = base64_bytes.decode('utf-8')

    # Remove trailing '=' padding
    base64_string = base64_string.rstrip('=')

    return base64_string


def decode_from_base64_url_safe(base64_string):
    # Add padding if necessary
    padding_length = 4 - (len(base64_string) % 4)
    base64_string += '=' * padding_length

    # Decode the Base64 string to bytes
    base64_bytes = base64.urlsafe_b64decode(base64_string)

    # Decode the bytes to the original string using UTF-8
    original_string = base64_bytes.decode('utf-8')

    return original_string
