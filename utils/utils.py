import os 

def uploadFileToServer(request):
    print("Inside helper function!")

    if 'file' not in request.files:
        return "No file part"
    
    # if 'prompt_data' not in request.files:
    #     return "No Prompt Data"
    
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
    # Placeholder for your code variable
    code = "{" + query + "}"

    # Prompt for the LLM
    prompt = f"""
{code}
for the given code do as per the given following constraints and respond nothing else other than what i say in the constraints
note:Don't respond with anything other than the {target_language} code with proper documentation
1. Check whether the given code is a {current_language} language code or not. If yes, then continue with other constraints and don't respond with anything else other than the generated {target_language} code and the documentation for the code after the code is completely generated and no other words from you. Else stop executing and respond "invalid {current_language} code" and nothing else.
2. The provided {current_language} code snippet must adhere to standard {current_language} syntax and conventions. It should be a syntactically correct {current_language} program.
3. The {target_language} conversion should accurately reflect the functionality of the original {current_language} code. This includes preserving the logic, structure, and behavior of the {current_language} program.
4. Proper documentation, including comments, should be included in the translated {target_language} code. The comments should explain the logic and purpose of the code, as well as any significant differences between the {current_language} and {target_language} versions.
5. The program should handle errors gracefully. If the provided {current_language} code is not valid or encounters issues during conversion, the program should indicate the problem(s) encountered and provide meaningful error messages.
    """

    # Print prompt for debugging
    print(prompt)

    # Invoke LLN (Large Language Model)
    query_response = llm.invoke(prompt)

    # Print LLN response for debugging
    print(query_response)

    # Prepare response dictionary
    response = {"result": query_response}

    return response
