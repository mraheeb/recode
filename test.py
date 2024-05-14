import sys
import os
import requests

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
        current_language = None
        for ext, lang in valid_extensions.items():
            if file_extension == ext:
                current_language = lang
                break

        if current_language is None or current_language not in current_languages:
            print("Error: Input file must have a valid extension for one of the following languages:", ", ".join(current_languages))
            return

        # Read contents of the input file
        with open(input_filename, "r") as input_file:
            file_contents = input_file.read()

        # Make POST request to the API
        api_url = "https://3895-202-140-36-183.ngrok-free.app/api/convertCode"
        target_language = "python"

        data = {"query": file_contents,
                "current_language": current_language,
                "target_language": target_language}

        response = requests.post(api_url, json=data)

        if response.status_code == 200:
            # Parse the response
            response_data = response.json()
            python_code = response_data.get("result", "")

            # Write contents to the output file
            output_filename = os.path.splitext(input_filename)[0] + ".py"
            with open(output_filename, "w") as output_file:
                output_file.write(python_code)

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
    # Check if filename argument is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
    else:
        input_filename = sys.argv[1]
        current_languages = ["cobol", "delphi", "visual basic"]
        convert_to_python(input_filename, current_languages)
