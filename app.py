import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import re

app = Flask(__name__)

# Set your Gemini API Key here
API_KEY = "AIzaSyByNiZP2vD3IW1hZRrT923JZNvTSVoQZ7c"

# Configure the Gemini API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-002")

# Store user conversations (simple in-memory storage)
user_conversations = {}

def clean_response(response_text):
    # Convert bold markdown to <strong> tags
    response_text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", response_text)
    
    # Convert italic markdown to <em> tags
    response_text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", response_text)
    response_text = re.sub(r"_(.*?)_", r"<em>\1</em>", response_text)
    
    # Replace numbered lists with properly formatted HTML
    response_text = re.sub(r"(?m)^\d+\.\s+(.*?)$", r"<strong>\1</strong>", response_text)
    
    # Convert bullet lists to HTML
    response_text = re.sub(r"(?m)^- (.*?)$", r"• \1", response_text)
    
    # Convert line breaks to <br> tags
    response_text = response_text.replace("\n\n", "<br><br>")
    response_text = response_text.replace("\n", "<br>")
    
    return response_text

@app.route('/')
def index():
    # Serve the HTML file directly
    return render_template('index.html')

@app.route('/', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    user_id = data.get('user_id', 'default_user')
    
    # Store the user message in conversation history
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    user_conversations[user_id].append({"role": "user", "content": user_message})
    
    # Create a prompt that focuses on recipes
    prompt = f"""You are Culinary Companion, an AI chef assistant that helps with recipe recommendations.
    Only answer questions related to cooking, recipes, food, and culinary topics.
    If asked about non-food topics, politely redirect the conversation to culinary subjects.
    Based on this user message, provide a helpful recipe recommendation or culinary advice and note(I want output like in ingredient, how to cook(briefly) format. you dont have to ask question to the user. just recommend what the user already said):
    
    {user_message}"""
    
    try:
        # Generate response from Gemini
        response = model.generate_content(prompt)
        bot_response = clean_response(response.text)
        
        # Store the bot response in conversation history
        user_conversations[user_id].append({"role": "assistant", "content": bot_response})
        
        return jsonify({"response": bot_response})
    
    except Exception as e:
        print(f"Error generating response: {e}")
        return jsonify({"response": "I'm having trouble connecting to my recipe database right now. Please try again in a moment!"})

@app.route('/', methods=['POST'])
def set_api_key():
    data = request.json
    api_key = data.get('api_key', '')
    
    # This would normally validate the API key with Gemini
    # For demonstration purposes, we'll accept any non-empty string
    if api_key and len(api_key) > 10:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Invalid API key format"})

if __name__ == '__main__':
    app.run(debug=True)