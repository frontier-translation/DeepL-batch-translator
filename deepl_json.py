import json
import sys
import requests
import os
import dotenv

# Validate CLI arguments
if len(sys.argv) != 2:
    print("Usage: deepl_json.py <json_file>")
    sys.exit(1)

def main():
    """Get the translations from the DeepL API"""

    # Read the json file
    json_file = sys.argv[1]
    print(f"Reading {json_file}")
    data = read_json(json_file)
    print(data)

    # Import the environment variables from the .env file
    dotenv.load_dotenv()
    api_url = os.getenv("DEEPL_API_URL")
    api_key = os.getenv("DEEPL_API_KEY")
    target_language = os.getenv("DEEPL_TARGET_LANGUAGE")
    
    # Load all the keys from data to a list
    keys = []
    for key in data:
        keys.append(key)
    print(keys)

    # Create a new dictionary
    translated_data = {}

    # Loop through each key and print the value
    for key in keys:
        print(f"{key}: {data[key]}")

        # Make a POST request with form data
        form_data = {
            "text": key,
            "target_lang": target_language,
            "auth_key": api_key
        }
        response = requests.post(api_url, data=form_data, headers={"Authorization": api_key})

        # Check for errors
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            sys.exit(1)

        # Load the response as json
        response_json = response.json()
        print(f"Translated response: {response_json}")

        # Print the translated text
        print(f"{key}: {response_json['translations'][0]['text']}")

        # Save the translated text to the dictionary
        translated_data[key] = response_json['translations'][0]['text']

    # Save the translated text to a new json file
    translated_json_file = f"{json_file}_translated.json"
    print(f"Saving translated data to {translated_json_file}")
    write_json(translated_json_file, translated_data)

def read_json(json_file):
    """Read the json file"""

    with open(json_file, 'r') as f:
        data = json.load(f)
    return data

def write_json(json_file, data):
    """Write the json file"""

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

# Call the main function
if __name__ == "__main__":
    main()