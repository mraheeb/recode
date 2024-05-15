import os
import requests
import pyfiglet
import sys

def print_ascii_art(text):
    ascii_art = pyfiglet.figlet_format(text, font="slant")
    print(ascii_art)
    print("Loading...")

def convert_to_python(input_path, current_lang, valid_extensions):
    try:
        # print("Input Path:", input_path)  # Debugging statement
        
        if os.path.isfile(input_path):  # If input is a file
            print("Input path is a file.")
            convert_file_to_python(input_path, current_lang, valid_extensions)
        elif os.path.isdir(input_path):  # If input is a directory
            print("Input path is a directory.")
            for root, _, files in os.walk(input_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_extension = os.path.splitext(file)[1].lower()
                    print("File found:", file_path)  # Debugging statement
                    print("File extension:", file_extension)  # Debugging statement
                    if file_extension in valid_extensions.keys():
                        # print("Converting:", file_path)  # Debugging statement
                        convert_file_to_python(file_path, current_lang, valid_extensions)
                    else:
                        print("Skipped:", file_path, " - Not a supported file type")  # Debugging statement
        else:
            print("Error: Invalid input path.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")



def convert_file_to_python(input_filename, current_lang,valid_extensions):
    try:
        print("Converting file:", input_filename)  # Debugging statement

        # Check if the input file has a valid extension for any of the current languages
        # valid_extensions = {".cbl": "cobol", ".cob": "cobol", ".pas": "delphi", ".vb": "visual basic"}
        file_extension = os.path.splitext(input_filename)[1].lower()
        current_language = valid_extensions.get(file_extension)
        
        if not current_language or current_language not in current_lang:
            print(f"Error: {input_filename} must have a valid extension for one of the following languages:", ", ".join(current_lang))
            return

        # Read contents of the input file
        with open(input_filename, "r") as input_file:
            file_contents = input_file.read()

        # print("File contents:", file_contents[:50])  # Debugging statement

        # Make POST request to the API
        api_url = "http://192.168.1.207:5050/api/convertCode"
        target_language = "python"

        response = requests.post(api_url, json={"query": file_contents, "current_language": current_language, "target_language": target_language})

        print("Response status code:", response.status_code)  # Debugging statement

        if response.status_code == 200:
            # Write contents to the output file
            output_filename = os.path.splitext(input_filename)[0] + ".py"
            with open(output_filename, "w") as output_file:
                output_file.write(response.json().get("result", ""))
            print(f"File '{output_filename}' generated successfully.")
        elif response.status_code == 400:
            print("Invalid code for the specified language.")
        else:
            print(f"Error: Failed to generate Python code for {input_filename}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <path> <current_lang>")
    else:
        input_path = sys.argv[1]
        current_lang = sys.argv[2].split(',')
        valid_extensions = {".cbl": "cobol", ".cob": "cobol", ".pas": "delphi", ".vb": "visual basic"}
        print_ascii_art("ReCode")
        convert_to_python(input_path, current_lang,valid_extensions)
