from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from flask_cors import CORS


app = Flask(__name__)

# Integrating VUE js for frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8080", "http://127.0.0.1:8080"]
    }
})


# Configure Google GenAI with the provided API key
genai.configure(api_key="AIzaSyBGd0VOcTyR6Dzx6Fi5T9ZVGBHzmXgXOks")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        if not message:
            return jsonify({"error": "Message required"}), 400

        # Initialize the Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Get explanation from Gemini
        prompt = f"Explain the mathematical concept in this question: {message}"
        response = model.generate_content(prompt)
        explanation = response.text if response.text else "Sorry, I couldn't generate a response."

        return jsonify({
            "response": explanation,
            "video_url": "",  # Empty as per your request
            "question": ""    # Empty to maintain UI compatibility
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "response": "Error processing request.",
            "video_url": "",
            "question": ""
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
