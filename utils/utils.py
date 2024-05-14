import os 

def uploadFileToServer(request):
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
            f.write("\nThis text was added by the uploadFileToServer function.")

        return filepath
    return None

def translate(query, current_language, target_language, llm):
    code = "{" + query + "}"

#     prompt = f"""
# {code}
# for the given code do as per the given following constraints and respond nothing else other than what i say in the constraints
# note:Don't respond with anything other than the {target_language} code with proper documentation
# 1. Check whether the given code is a {current_language} language code or not. If yes, then continue with other constraints and don't respond with anything else other than the generated {target_language} code and the documentation for the code after the code is completely generated and no other words from you. Else stop executing and respond "invalid {current_language} code" and nothing else.
# 2. The provided {current_language} code snippet must adhere to standard {current_language} syntax and conventions. It should be a syntactically correct {current_language} program.
# 3. The {target_language} conversion should accurately reflect the functionality of the original {current_language} code. This includes preserving the logic, structure, and behavior of the {current_language} program.
# 4. Proper documentation, including comments, should be included in the translated {target_language} code. The comments should explain the logic and purpose of the code, as well as any significant differences between the {current_language} and {target_language} versions.
# 5. The program should handle errors gracefully. If the provided {current_language} code is not valid or encounters issues during conversion, the program should indicate the problem(s) encountered and provide meaningful error messages.
#     """

#     prompt = f"""
# {code}
# Identify the language the program is written in; if not a programming language return response as "NOT A PROGRAMMING LANGUAGE".
# After Identifying the language, accurately predict what the program does, dont output it out yet.
# Convert the input code into equivalent python code, if there are missing code snippets like external library/modules mention it using python comments.
# The previous prediction also needs to be commented inline where appropriate.

# Always enclose the executable python code within $start$ and $end$.
#     """

    prompt = f"""
{code}
Identify the language the program is written in; if not a programming language return response as "NOT A PROGRAMMING LANGUAGE".
After Identifying the language, accurately predict what the program does, dont output it out yet.
Convert the input code into equivalent {target_language} code, if there are missing code snippets like external library/modules mention it using {target_language} comments.
The previous prediction also needs to be commented inline where appropriate.

Always enclose the executable {target_language} code within $start$ and $end$.
    """


    query_response = llm.invoke(prompt)


    response = {"result": query_response}

    return response

def document(query, current_language, llm):
    code = "{" + query + "}"

    prompt = f"""
{code}
 Generate documentation for the code and respond back always by enclosing the documentation  $start$ and $end$
    """


    query_response = llm.invoke(prompt)


    response = {"result": query_response}

    return response

def validate(query, current_language, llm):
    code = "{" + query + "}"

    prompt = f"""
{code}
Respond back with a one word(Yes/No). Is the given code {code} written in {current_language}
    """


    query_response = llm.invoke(prompt)


    response = {"result": query_response}

    return response.get("result")