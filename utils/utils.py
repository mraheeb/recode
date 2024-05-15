import os

def upload_file_to_server(request):
    print("Inside helper function!")

    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        filename = file.filename
        filepath = os.path.join('uploads', filename)
        print(filepath)
        file.save(filepath)

        with open(filepath, 'w') as f:
            f.write("\nThis text was added by the upload_file_to_server function.")

        return filepath
    return None

def translate(query, current_language, target_language, llm):
    code = "{\n" + query + "\n}"

    prompt = f"""
    Convert the provided {current_language} code to equivalent {target_language} code. Ensure the {target_language} code follows {target_language} naming conventions and idiomatic usage of built-in functions. Identify the equivalent entry point to the main function in {target_language}.
    {code}
    """
#     In the provided code snippet:
# 1. Determine the purpose of the {current_language} program.
# 2. Identify input parameters, functions, conditions, and cases.
# 3. Based on the above, perform the following tasks:
#    A. Translate the {current_language} code into equivalent {target_language} code maintaining functionality.
#    B. Avoid creating an explicit main function() in the {target_language} code.
#    C. Prefix non-{target_language} lines with `#`.
#    D. Enclose the generated {target_language} code between `$start$` and `$end$`. Example: $start$ print("hello world") $end$.
#     print("utils.py", prompt)

    query_response = llm.invoke(prompt)

    response = {"result": query_response}

    return response

def document(query, current_language, llm):
    code = "{" + query + "}"

    prompt = f"""
{code}
Generate comprehensive documentation for the code enclosed between $start$ and $end$.
    """

    query_response = llm.invoke(prompt)

    response = {"result": query_response}

    return response

def validate(query, current_language, llm):
    code = "{\n" + query + "\n}"

    prompt = f"""
{code}
Provide a one-word response (Yes/No). Is the given code {current_language} syntax?
    """

    query_response = llm.invoke(prompt)

    response = {"result": query_response}

    return response.get("result")
