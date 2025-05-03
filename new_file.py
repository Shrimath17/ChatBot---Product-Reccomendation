from flask import Flask, request, jsonify, render_template, session
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from typing import Dict, List
from dotenv import load_dotenv
import os
import re
import uuid
import json
import ollama

# Download NLTK resources
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    print("Warning: NLTK download failed. Some features may be limited.")

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'product_recommendation_secret_key')

class ProductRecommendationEngine:
    def __init__(self):
        """Initialize the Product Recommendation Engine"""
        # Ollama configuration
        self.MODEL_NAME = "qwen3:8b"  # Adjust to your Qwen3 model variant
        
        # Initialize NLTK components
        self.lemmatizer = WordNetLemmatizer()
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            # Fallback if NLTK data isn't available
            self.stop_words = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
                                   "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 
                                   'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 
                                   'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 
                                   'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 
                                   'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 
                                   'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 
                                   'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 
                                   'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 
                                   'about', 'against', 'between', 'into', 'through', 'during', 'before', 
                                   'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 
                                   'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 
                                   'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 
                                   'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 
                                   'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 
                                   'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 
                                   'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 
                                   'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', 
                                   "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 
                                   'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', 
                                   "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 
                                   'won', "won't", 'wouldn', "wouldn't"])
        
        # Initialize conversation history storage
        self.conversation_histories = {}
        
        # Initialize product categories
        self.product_categories = {
            'electronics': ['smartphone', 'laptop', 'headphones', 'smartwatch', 'tablet'],
            'clothing': ['jacket', 'shoes', 'shirt', 'jeans', 'dress'],
            'home': ['lamp', 'sofa', 'vacuum', 'cookware', 'bedding'],
            'sports': ['bicycle', 'yoga mat', 'dumbbells', 'running shoes', 'fitness tracker'],
            'beauty': ['skincare', 'makeup', 'perfume', 'hair dryer', 'electric razor']
        }

    def clean_response(self, response_text):
        """Clean and format response text for HTML rendering"""
        # Convert bold markdown to <strong> tags
        response_text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", response_text)
        
        # Convert italic markdown to <em> tags
        response_text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", response_text)
        response_text = re.sub(r"_(.*?)_", r"<em>\1</em>", response_text)
        
        # Convert list-style markdown to <ul> and <li>
        lines = response_text.split('\n')
        in_list = False
        cleaned_lines = []
        for line in lines:
            if line.strip().startswith('- '):
                if not in_list:
                    cleaned_lines.append('<ul>')
                    in_list = True
                cleaned_lines.append(f"<li>{line.strip()[2:].strip()}</li>")
            else:
                if in_list:
                    cleaned_lines.append('</ul>')
                    in_list = False
                cleaned_lines.append(line)
        if in_list:
            cleaned_lines.append('</ul>')
        response_text = '\n'.join(cleaned_lines)
        
        # Convert line breaks to <br> tags for paragraph breaks
        response_text = response_text.replace('\n', '<br>')
        
        return response_text

    def get_response_ollama(self, prompt):
        """Get response from Ollama Qwen3 model"""
        try:
            response = ollama.generate(model=self.MODEL_NAME, prompt=prompt)
            return response.get("response", "No response received")
        except Exception as e:
            return f"Error: {str(e)}"

    def ollama_response(self, message):
        """Generate a product recommendation response using Ollama Qwen3 model"""
        # Craft a prompt with product context
        context = "You are a product recommendation assistant. Your task is to recommend up to 5 products based on the user's prompt, even if vague. Provide a brief comparison of features, price range, and use case for each product. Here are example product categories and items:\n"
        for category, items in self.product_categories.items():
            context += f"- {category}: {', '.join(items)}\n"
        context += "\nBased on the user's request, suggest relevant products. If the prompt is vague, infer the most likely category or use case. Format the response as a numbered list with each product including: product name, features, price range, and use case. Use plain text, no markdown. Do not include any reasoning, commentary, or intermediate thoughts—only the final product recommendations. Do not recommend recipes or non-product items.\n\n"
        prompt = f"{context}User request: {message}"
        # Get response from Ollama
        response = self.get_response_ollama(prompt)
        
        # Clean and format the response
        cleaned_response = self.clean_response(response)
        
        return cleaned_response

    def process_user_message(self, user_id, message):
        """Process user message and return a response"""
        # Initialize conversation history for this user if needed
        if user_id not in self.conversation_histories:
            self.conversation_histories[user_id] = []
        
        # Add user message to conversation history
        self.conversation_histories[user_id].append({"role": "user", "content": message})
        
        # Check if the message is recipe-related
        recipe_keywords = ['recipe', 'cook', 'ingredient', 'meal', 'dish']
        if any(keyword in message.lower() for keyword in recipe_keywords):
            response = "I am a product recommendation chatbot. Please ask for product-related recommendations."
        else:
            # Get product recommendation response from Ollama
            response = self.ollama_response(message)
        
        # Add response to conversation history
        self.conversation_histories[user_id].append({"role": "assistant", "content": response})
        
        return response

# Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    """Single route to handle all functionality"""
    if request.method == 'GET':
        return render_template('index.html')
    
    elif request.method == 'POST':
        try:
            data = request.json
            user_message = data.get('message', '')
            
            # Get or create user ID from session
            if 'user_id' not in session:
                session['user_id'] = str(uuid.uuid4())
            user_id = session['user_id']
            
            # Process the message
            response = recommendation_engine.process_user_message(user_id, user_message)
            
            return jsonify({"response": response})
        except Exception as e:
            return jsonify({"error": str(e)})

# Initialize recommendation engine
recommendation_engine = ProductRecommendationEngine()

if __name__ == '__main__':
    app.run(debug=True)