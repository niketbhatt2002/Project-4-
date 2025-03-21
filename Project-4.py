import openai
import json
from flask import Flask, request, jsonify
import datetime
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Azure OpenAI API Configuration
openai.api_type = "azure"
openai.api_base = "https://YOUR_AZURE_OPENAI_ENDPOINT.openai.azure.com/"
openai.api_version = "2023-05-15"
openai.api_key = "YOUR_AZURE_OPENAI_API_KEY"

# Application Configuration
PROMPT_FLOW = {
    "input_nodes": [
        {"name": "user_input", "type": "text", "description": "User-provided query or task."}
    ],
    "model_nodes": [
        {"name": "llm_response", "model": "gpt-4", "temperature": 0.7}
    ],
    "output_nodes": [
        {"name": "response", "type": "json", "description": "LLM-generated output."}
    ]
}

@app.route('/prompt-flow', methods=['POST'])
def prompt_flow():
    try:
        # Capture user input
        user_input = request.json.get("input", "")
        if not user_input:
            return jsonify({"error": "No input provided"}), 400
        
        # Log input
        logging.info(f"User input: {user_input}")
        
        # Process with LLM
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=user_input,
            max_tokens=500,
            temperature=0.7
        )
        
        # Prepare output
        output = {
            "input": user_input,
            "output": response["choices"][0]["text"].strip(),
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Log output
        logging.info(f"LLM Output: {output}")
        
        return jsonify(output), 200
    
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
