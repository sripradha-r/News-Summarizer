from flask import Flask, request, jsonify, send_file
import json
from main import process_company_news_with_audio
import os

app = Flask(__name__)

@app.route("/process_company_news", methods=["POST"])
def process_company_news_api():
    data = request.get_json()
    company_name = data.get("company_name")

    if not company_name:
        return jsonify({"error": "Company name is required"}), 400

    try:
        result_json = process_company_news_with_audio(company_name)
        
        # Check for missing "Audio" in the result
        audio_file_path = result_json.get("Audio", None)
        if audio_file_path and os.path.exists(audio_file_path):
            return send_file(audio_file_path, as_attachment=True, mimetype='audio/wav')
        else:
            return jsonify({"error": "Audio file not found."}), 500

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
