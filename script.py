import requests
import json
import os
import sys

def get_wled_ip():
    """Get the WLED IP address from the environment variable, default to 192.168.3.242"""
    return os.getenv('WLED_IP', '192.168.3.242')

def get_env_variable(var_name, default):
    """Get an environment variable, return default value if not set"""
    value = os.getenv(var_name, default)
    print(f"{var_name} from env: {value}")  # For debugging purposes
    return value

def get_color_from_env():
    """Get the color value from the environment variable"""
    color_value = os.getenv('COLOR_TO_SET')
    print(f"Raw COLOR_TO_SET value from env: {color_value}")  # For debugging purposes

    if color_value.startswith('"') and color_value.endswith('"'):
        color_value = color_value[1:-1]  # Strip extraneous quotes if present

    try:
        color_value = json.loads(color_value)  # Parse the JSON string into a list
        if isinstance(color_value, list) and len(color_value) == 3:
            return color_value
        else:
            raise ValueError("Invalid color format for COLOR_TO_SET")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error loading color COLOR_TO_SET: {e}", file=sys.stderr)
        sys.exit(1)

def create_payload(start, stop, fx, color):
    """Create the JSON payload to set the LED color and segment properties"""
    payload = {
        "seg": [
            {
                "start": int(start),
                "stop": int(stop),
                "fx": int(fx),
                "col": [color, [0, 0, 0], [0, 0, 0]],
                "rev": True
            }
        ]
    }
    return payload

def send_post_request(url, headers, payload):
    """Send a POST request to the WLED device"""
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error sending POST request: {e}", file=sys.stderr)
        sys.exit(1)
    return response

def main():
    WLED_IP = get_wled_ip()
    url = f'http://{WLED_IP}/json/state'
    headers = {'Content-Type': 'application/json'}
    
    # Get segment properties and color from environment variables
    start = get_env_variable('SEG_START', 0)
    stop = get_env_variable('SEG_STOP', 20)
    fx = get_env_variable('SEG_FX', 3)
    color_to_set = get_color_from_env()

    # Create payload
    payload = create_payload(start, stop, fx, color_to_set)

    # Send the POST request
    response = send_post_request(url, headers, payload)

    # Validate the JSON response
    try:
        response_data = response.json()  # Validate if the response is a valid JSON
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}", file=sys.stderr)
        sys.exit(1)

    if response.status_code == 200:
        print(f"Successfully set the LED strip to the specified color and segment properties.")
    else:
        print(f"Failed to set the color: {response.status_code} - {response.text}", file=sys.stderr)

if __name__ == '__main__':
    main()