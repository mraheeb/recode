from langchain_community.llms import Ollama
from flask import Flask, request, send_file
from flask_cors import CORS
import os

from utils import utils

app = Flask(__name__)
llm = Ollama(model = "llama3")

@app.route("/api/generate", methods=["POST"])
def generate():
    print("/api/generate")
    json = request.json
    query = json.get("query")
    response = llm.invoke(query)
    print(response)
    return response

@app.route("/api/generateProjectDocumentation", methods=["POST"])
def generateProjectDocumentation():
    print("------------------------------------------------------------------------------")

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    modified_file_path = utils.uploadFileToServer(request=request)

    if modified_file_path:
        # Send the modified file back to the client
        return send_file(modified_file_path, as_attachment=True)
    else:
        return "Failed to upload and modify file"


@app.route("/api/convertCode", methods=["POST"])
def convertCode():
    print("------------------------------------------------------------------------------")
    json_data = request.json
    query = json_data.get("query")
    current_language = json_data.get("current_language")
    target_language = json_data.get("target_language")

    isCodeValid = utils.validate(query, current_language, llm)
    if "Yes" in isCodeValid:
        response = utils.translate(query, current_language, target_language, llm)
    else:
        response = {"error": f"The code given cannot be converted as it is not a valid {current_language} code."}
        return response
    
    # documented_response = utils.document(query, target_language, llm)

    # print(documented_response.get("result"))
    # print("------------------------------------------------------------------------------")
    # return documented_response
    
    python_code = response.get("result", "")
    start_index = python_code.find("$start$") + len("$start$")
    stop_index = python_code.find("$end$") + len("$end$")

    response = python_code[start_index:stop_index - 5]

    response = {"result": response}

    print(response.get("result"))

    print("------------------------------------------------------------------------------")
    return response

@app.route("/api/generateLegacyDocumentation", methods=["POST"])
def generateLegacyDocumentation():
    print("------------------------------------------------------------------------------")
    json_data = request.json
    query = json_data.get("query")
    current_language = json_data.get("current_language")

    isCodeValid = utils.validate(query, current_language, llm)
    if "Yes" in isCodeValid:
        response = utils.document(query, current_language, llm)
    else:
        response = {"error": f"The code given cannot be documented as it is not a valid {current_language} code."}
        return response


    documentation = response.get("result", "")
    start_index = documentation.find("$start$") + len("$start$")
    stop_index = documentation.find("$end$") + len("$end$")

    documentation = documentation[start_index:stop_index - 5]

    final_documentation = documentation + "\n\n\n" + query

    response = {
        "result": final_documentation
    }

    # response = documentation[start_index:stop_index - 5]

    # response = {"result": response}
    
    print(response.get("result"))

    print("------------------------------------------------------------------------------")
    return response

@app.route("/api/validate", methods=["POST"])
def validate():
    json_data = request.json
    query = json_data.get("query")
    current_language = json_data.get("current_language")
    response = utils.validate(query, current_language, llm)

    return response

def start_app():
    print("This function gets called!")
    app.run(host = "0.0.0.0", port = 5050, debug = True)
    print("Server started at port 5050")

if __name__ == "__main__":
    start_app()