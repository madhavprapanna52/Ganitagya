from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Configure Gemini API
genai.configure(api_key="AIzaSyBGd0VOcTyR6Dzx6Fi5T9ZVGBHzmXgXOks") # Api connection

# Routes
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
def home():
    return render_template('home.html')

# Routes
@app.route('/playground')
def playground():
    return render_template('playground.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat API endpoint"""
    try:
        data = request.json
        message = data.get('message', '')
        
        # Generate response using Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        # prompt = f"गणित की इस समस्या को हिंदी में समझाएं: {message}"
        prompt = f"Explain this mathematical problem in very easyway with example: {message}"
        response = model.generate_content(prompt)
        
        return jsonify({
            "response": response.text,
            "video_url": "",  # Add video generation logic here
            "question": message
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "response": "माफ करें, कुछ तकनीकी समस्या हुई है। कृपया फिर से कोशिश करें।"
        }), 500

# Static file routes (for videos from manimation_engine)
@app.route('/videos/<path:filename>')
def serve_generated_video(filename):
    """Serve generated videos"""
    return send_from_directory('manimation_engine/generated_videos', filename)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

