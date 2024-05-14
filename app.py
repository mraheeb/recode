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
    print("/generateProjectDocumentation")

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    modified_file_path = utils.uploadFileToServer(request=request)

    if modified_file_path:
        # Send the modified file back to the client
        return send_file(modified_file_path, as_attachment=True)
    else:
        return "Failed to upload and modify file"


@app.route("/api/generateInlineDocumentation", methods=["POST"])
def generateInlineDocumentation():
    print("/generateInlineDocumentation")
    json_data = request.json
    query = json_data.get("query")
    current_language = json_data.get("current_language")
    target_language = json_data.get("target_language")

    response = utils.translate(query, current_language, target_language, llm)

    return response
    #return "Working"


def start_app():
    print("This function gets called!")
    app.run(host = "0.0.0.0", port = 5050, debug = True)
    print("Server started at port 5050")

if __name__ == "__main__":
    start_app()