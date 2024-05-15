import os
import requests
import pyfiglet
import sys

def print_ascii_art(text):
    ascii_art = pyfiglet.figlet_format(text, font="slant")
    print(ascii_art)
    print("Loading...")

def convert_to_python(input_filename, current_languages):
    try:
        # Check if the input file exists
        if not os.path.exists(input_filename):
            print(f"Error: File '{input_filename}' does not exist.")
            return

        # Extract file extension
        file_extension = os.path.splitext(input_filename)[1].lower()

        # Check if the input file has a valid extension for any of the current languages
        valid_extensions = {".cbl": "cobol", ".cob": "cobol", ".pas": "delphi", ".vb": "visual basic"}
        current_language = valid_extensions.get(file_extension)
        
        if not current_language or current_language not in current_languages:
            print("Error: Input file must have a valid extension for one of the following languages:", ", ".join(current_languages))
            return

        # Read contents of the input file
        with open(input_filename, "r") as input_file:
            file_contents = input_file.read()

        # Make POST request to the API
        api_url = "http://192.168.1.207:5050/api/convertCode"
        target_language = "python"

        response = requests.post(api_url, json={"query": file_contents, "current_language": current_language, "target_language": target_language})

        if response.status_code == 200:
            # Write contents to the output file
            output_filename = os.path.splitext(input_filename)[0] + ".py"
            with open(output_filename, "w") as output_file:
                output_file.write(response.json().get("result", ""))
            print(f"File '{output_filename}' generated successfully.")
        elif response.status_code == 400:
            print("Invalid code for the specified language.")
        else:
            print(f"Error: Failed to generate Python code. Status code: {response.status_code}")
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
    else:
        input_filename = sys.argv[1]
        current_languages = ["cobol", "delphi", "visual basic"]
        print_ascii_art("ReCode")
        convert_to_python(input_filename, current_languages)
