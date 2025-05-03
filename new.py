# import json
# import random
# import pickle
# import os
# import numpy as np
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.naive_bayes import MultinomialNB
# import nltk
# from nltk.stem import WordNetLemmatizer
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords

# # Ensure NLTK data is downloaded
# try:
#     nltk.data.find('tokenizers/punkt')
# except LookupError:
#     nltk.download('punkt', quiet=True)

# try:
#     nltk.data.find('corpora/wordnet')
# except LookupError:
#     nltk.download('wordnet', quiet=True)

# try:
#     nltk.data.find('corpora/stopwords')
# except LookupError:
#     nltk.download('stopwords', quiet=True)

# class RecipeChatBot:
#     def __init__(self, intents_file='recipe_intents.json', recipes_file='recipes.json'):
#         # Create necessary files if they don't exist
#         self.create_sample_files(intents_file, recipes_file)
        
#         # Initialize lemmatizer
#         self.lemmatizer = WordNetLemmatizer()
        
#         # Load recipe data
#         with open(recipes_file, 'r') as file:
#             self.recipes = json.load(file)
        
#         # Load conversation intents
#         with open(intents_file, 'r') as file:
#             self.intents = json.load(file)
        
#         # Train or load the model
#         self.train_conversation_model()
        
#         # Create cuisine lookup
#         self.cuisine_recipes = {}
#         for recipe in self.recipes:
#             cuisine = recipe['cuisine']
#             if cuisine not in self.cuisine_recipes:
#                 self.cuisine_recipes[cuisine] = []
#             self.cuisine_recipes[cuisine].append(recipe)
        
#         # Create ingredient index for recommendations
#         self.ingredient_recipes = {}
#         for recipe in self.recipes:
#             for ingredient in recipe['ingredients']:
#                 if ingredient not in self.ingredient_recipes:
#                     self.ingredient_recipes[ingredient] = []
#                 self.ingredient_recipes[ingredient].append(recipe)
        
#         # Track conversation context
#         self.context = {
#             "current_cuisine": None,
#             "liked_ingredients": [],
#             "disliked_ingredients": [],
#             "previous_recommendations": []
#         }
    
#     def create_sample_files(self, intents_file, recipes_file):
#         """Create sample data files if they don't exist"""
#         # Create sample recipe intents
#         if not os.path.exists(intents_file):
#             intents = {
#                 "intents": [
#                     {
#                         "tag": "greeting",
#                         "patterns": ["Hi", "Hey", "Hello", "Good day", "Howdy", "What's up", "Hi there", "Hello there"],
#                         "responses": [
#                             "Hello! I'm your recipe assistant. How can I help you today?",
#                             "Hi there! Looking for recipe recommendations?",
#                             "Hey! Need help finding a delicious recipe?",
#                             "Greetings! Ready to discover some amazing recipes?"
#                         ]
#                     },
#                     {
#                         "tag": "goodbye",
#                         "patterns": ["Bye", "See you later", "Goodbye", "I'm leaving", "Have a good day", "That's all", "Thanks bye"],
#                         "responses": [
#                             "Goodbye! Enjoy your cooking!",
#                             "See you later! Hope you find the perfect recipe!",
#                             "Bye! Come back when you're hungry for more recipes!",
#                             "Take care and happy cooking!"
#                         ]
#                     },
#                     {
#                         "tag": "thanks",
#                         "patterns": ["Thanks", "Thank you", "That's helpful", "Thanks for the help", "Appreciate it", "Great thanks"],
#                         "responses": [
#                             "You're welcome! Cooking is all about sharing good food.",
#                             "Happy to help! Enjoy your meal!",
#                             "My pleasure! Let me know how the recipe turns out!",
#                             "Anytime! Good luck with your cooking adventure!"
#                         ]
#                     },
#                     {
#                         "tag": "recommend_recipe",
#                         "patterns": [
#                             "Can you suggest a recipe?", 
#                             "What should I cook?",
#                             "I need a recipe",
#                             "Recommend something to cook",
#                             "Give me a recipe",
#                             "What's good to make?",
#                             "I'm hungry",
#                             "I want to cook",
#                             "Show me a recipe",
#                             "Recipe recommendation please"
#                         ],
#                         "responses": ["Here's a recipe recommendation for you:"]
#                     },
#                     {
#                         "tag": "cuisine_inquiry",
#                         "patterns": [
#                             "What cuisines do you know?",
#                             "What types of food can you recommend?",
#                             "Tell me about cuisines",
#                             "What food types are available?",
#                             "What kind of food do you have?",
#                             "Which cuisines?",
#                             "What ethnicity of food?"
#                         ],
#                         "responses": ["I can recommend various cuisines like:"]
#                     },
#                     {
#                         "tag": "ingredient_inquiry",
#                         "patterns": [
#                             "What ingredients are popular?",
#                             "Tell me about ingredients",
#                             "What ingredients should I use?",
#                             "Common ingredients in recipes",
#                             "What can I cook with?",
#                             "What ingredients do you know?",
#                             "Tell me ingredients"
#                         ],
#                         "responses": ["Some popular ingredients include:"]
#                     }
#                 ]
#             }
            
#             with open(intents_file, 'w') as f:
#                 json.dump(intents, f, indent=4)
        
#         # Create sample recipes
#         if not os.path.exists(recipes_file):
#             recipes = [
#                 {
#                     "id": 10259,
#                     "cuisine": "greek",
#                     "ingredients": [
#                         "romaine lettuce",
#                         "black olives",
#                         "grape tomatoes",
#                         "garlic",
#                         "pepper",
#                         "purple onion",
#                         "seasoning",
#                         "garbanzo beans",
#                         "feta cheese crumbles"
#                     ]
#                 },
#                 {
#                     "id": 10260,
#                     "cuisine": "italian",
#                     "ingredients": [
#                         "pasta",
#                         "tomato sauce",
#                         "garlic",
#                         "basil",
#                         "parmesan cheese",
#                         "olive oil"
#                     ]
#                 },
#                 {
#                     "id": 10261,
#                     "cuisine": "mexican",
#                     "ingredients": [
#                         "tortillas",
#                         "beans",
#                         "cheese",
#                         "avocado",
#                         "salsa",
#                         "cilantro",
#                         "lime"
#                     ]
#                 },
#                 {
#                     "id": 10262,
#                     "cuisine": "indian",
#                     "ingredients": [
#                         "rice",
#                         "chicken",
#                         "curry powder",
#                         "onion",
#                         "garlic",
#                         "ginger",
#                         "tomatoes",
#                         "yogurt",
#                         "coriander"
#                     ]
#                 },
#                 {
#                     "id": 10263,
#                     "cuisine": "chinese",
#                     "ingredients": [
#                         "rice",
#                         "soy sauce",
#                         "sesame oil",
#                         "chicken",
#                         "green onions",
#                         "ginger",
#                         "garlic",
#                         "vegetables"
#                     ]
#                 }
#             ]
            
#             with open(recipes_file, 'w') as f:
#                 json.dump(recipes, f, indent=4)
    
#     def train_conversation_model(self):
#         """Train the intent classification model using scikit-learn"""
#         # Process intents data
#         training_sentences = []
#         training_labels = []
#         self.classes = []
        
#         # Extract training data from intents
#         for intent in self.intents['intents']:
#             for pattern in intent['patterns']:
#                 training_sentences.append(pattern)
#                 training_labels.append(intent['tag'])
#             if intent['tag'] not in self.classes:
#                 self.classes.append(intent['tag'])
        
#         # Create vectorizer
#         self.vectorizer = CountVectorizer(
#             tokenizer=self.tokenize_and_lemmatize,
#             ngram_range=(1, 2)
#         )
        
#         # Fit vectorizer and transform training data
#         X = self.vectorizer.fit_transform(training_sentences)
#         y = training_labels
        
#         # Train classifier
#         self.classifier = MultinomialNB()
#         self.classifier.fit(X, y)
    
#     def tokenize_and_lemmatize(self, text):
#         """Tokenize and lemmatize text"""
#         tokens = word_tokenize(text.lower())
#         return [self.lemmatizer.lemmatize(token) for token in tokens]
    
#     def predict_intent(self, message):
#         """Predict the intent of a user message"""
#         # Transform the message using vectorizer
#         X = self.vectorizer.transform([message])
        
#         # Get predictions
#         intent_id = self.classifier.predict(X)[0]
        
#         # Get probabilities
#         probs = self.classifier.predict_proba(X)[0]
#         prob = max(probs)
        
#         # Return intent and probability
#         return {'intent': intent_id, 'probability': prob}
    
#     def extract_ingredients(self, message):
#         """Extract ingredients mentioned in a message"""
#         words = self.tokenize_and_lemmatize(message)
#         stop_words = set(stopwords.words('english'))
#         potential_ingredients = [word for word in words if word not in stop_words and len(word) > 2]
        
#         # Check against known ingredients
#         all_ingredients = set()
#         for recipe in self.recipes:
#             for ingredient in recipe['ingredients']:
#                 all_ingredients.add(ingredient.lower())
        
#         found_ingredients = []
#         for word in potential_ingredients:
#             for ingredient in all_ingredients:
#                 if word in ingredient:
#                     found_ingredients.append(ingredient)
#                     break
        
#         return list(set(found_ingredients))  # Remove duplicates
    
#     def extract_cuisine(self, message):
#         """Extract cuisine type from message"""
#         words = self.tokenize_and_lemmatize(message)
#         cuisines = set(recipe['cuisine'] for recipe in self.recipes)
        
#         for word in words:
#             if word in cuisines:
#                 return word
        
#         return None
    
#     def recommend_recipe(self):
#         """Recommend a recipe based on current context"""
#         candidate_recipes = []
        
#         # First, filter by cuisine if specified
#         if self.context["current_cuisine"]:
#             candidate_recipes = self.cuisine_recipes.get(self.context["current_cuisine"], [])
#         else:
#             candidate_recipes = self.recipes
        
#         # Score recipes based on liked and disliked ingredients
#         scored_recipes = []
#         for recipe in candidate_recipes:
#             # Skip previously recommended recipes if we have alternatives
#             if recipe in self.context["previous_recommendations"] and len(self.context["previous_recommendations"]) < len(candidate_recipes):
#                 continue
                
#             score = 0
#             for ingredient in recipe['ingredients']:
#                 if ingredient in self.context["liked_ingredients"]:
#                     score += 2
#                 if ingredient in self.context["disliked_ingredients"]:
#                     score -= 3
            
#             scored_recipes.append((recipe, score))
        
#         # Sort by score
#         scored_recipes.sort(key=lambda x: x[1], reverse=True)
        
#         # Return top recipe or random if no preferences
#         if scored_recipes:
#             recommended_recipe = scored_recipes[0][0]
#             self.context["previous_recommendations"].append(recommended_recipe)
#             return recommended_recipe
#         elif candidate_recipes:
#             recommended_recipe = random.choice(candidate_recipes)
#             self.context["previous_recommendations"].append(recommended_recipe)
#             return recommended_recipe
#         else:
#             return None
    
#     def format_recipe(self, recipe):
#         """Format a recipe for display"""
#         if not recipe:
#             return "I'm sorry, I couldn't find a recipe matching your preferences."
        
#         result = f"Here's a {recipe['cuisine']} recipe I think you'll like:\n\n"
#         result += f"Recipe ID: {recipe['id']}\n"
#         result += "Ingredients:\n"
#         for ingredient in recipe['ingredients']:
#             result += f"- {ingredient}\n"
        
#         # Add a cooking suggestion
#         result += "\nTo prepare this dish, you'll typically want to combine these ingredients "
        
#         if recipe['cuisine'] == 'italian':
#             result += "and simmer them with pasta for a delicious meal."
#         elif recipe['cuisine'] == 'mexican':
#             result += "in a flavorful combination perfect for tacos or burritos."
#         elif recipe['cuisine'] == 'indian':
#             result += "with aromatic spices and cook them slowly for a rich flavor."
#         elif recipe['cuisine'] == 'chinese':
#             result += "and stir-fry them quickly over high heat."
#         elif recipe['cuisine'] == 'greek':
#             result += "in a fresh salad or wrap for a Mediterranean treat."
#         else:
#             result += "according to your preference."
        
#         return result
    
#     def generate_response(self, intent, message):
#         """Generate a response based on intent and message content"""
#         tag = intent['intent']
        
#         # Extract context from message
#         cuisine = self.extract_cuisine(message)
#         if cuisine:
#             self.context["current_cuisine"] = cuisine
        
#         ingredients = self.extract_ingredients(message)
#         if "like" in message.lower() or "love" in message.lower():
#             for ingredient in ingredients:
#                 if ingredient not in self.context["liked_ingredients"]:
#                     self.context["liked_ingredients"].append(ingredient)
        
#         if "dislike" in message.lower() or "hate" in message.lower() or "don't like" in message.lower():
#             for ingredient in ingredients:
#                 if ingredient not in self.context["disliked_ingredients"]:
#                     self.context["disliked_ingredients"].append(ingredient)
        
#         # Handle different intents
#         if tag == 'recommend_recipe':
#             recipe = self.recommend_recipe()
#             return self.format_recipe(recipe)
        
#         elif tag == 'cuisine_inquiry':
#             cuisines = list(self.cuisine_recipes.keys())
#             return f"I can recommend recipes from these cuisines: {', '.join(cuisines)}. Which one would you like to try?"
        
#         elif tag == 'ingredient_inquiry':
#             # Get the most common ingredients across all recipes
#             all_ingredients = []
#             for recipe in self.recipes:
#                 all_ingredients.extend(recipe['ingredients'])
            
#             # Count occurrences
#             ingredient_counts = {}
#             for ingredient in all_ingredients:
#                 if ingredient in ingredient_counts:
#                     ingredient_counts[ingredient] += 1
#                 else:
#                     ingredient_counts[ingredient] = 1
            
#             # Get top ingredients
#             top_ingredients = sorted(ingredient_counts.items(), key=lambda x: x[1], reverse=True)[:10]
#             top_ingredient_names = [item[0] for item in top_ingredients]
            
#             return f"Some popular ingredients in my recipes are: {', '.join(top_ingredient_names)}. Do you have any preferences?"
        
#         else:
#             # Find the matching intent and return a response
#             for intent_data in self.intents['intents']:
#                 if intent_data['tag'] == tag:
#                     return random.choice(intent_data['responses'])
        
#         # Default response if no matching intent is found
#         return "I'm not sure I understand. Would you like me to recommend a recipe?"
    
#     def chat(self, message):
#         """Process a message and return a response"""
#         try:
#             # Predict intent
#             intent = self.predict_intent(message)
            
#             # Generate response based on intent
#             return self.generate_response(intent, message)
#         except Exception as e:
#             # Error handling
#             print(f"Error processing message: {e}")
#             return "I'm having trouble understanding that. Would you like a recipe recommendation instead?"

# import time
# def slow_print(text, delay=0.02):
#     for char in text:
#         print(char, end='', flush=True)
#         time.sleep(delay)
#     print()  # New line after printing

# import google.generativeai as genai
# API_KEY = "AIzaSyByNiZP2vD3IW1hZRrT923JZNvTSVoQZ7c"
# genai.configure(api_key=API_KEY)
# model = genai.GenerativeModel("gemini-1.5-flash-002")
# def get_gemini_response(user_input):

#     # Make the request to the Gemini API
#     print(user_input)
#     response = model.generate_content("Recipe Recommendation Chatbot for the user input: (Deny answers for the user input that is not related to recipes or foods) Users input: "+user_input+"This is sample output. Give me output like this.")
#     return response.text  


# # Main function to run the chatbot
# def main():
#     try:
#         chatbot = RecipeChatBot()
        
#         print("Recipe Chatbot: Hello! I'm your recipe assistant. How can I help you today? (type 'quit' to exit)")
        
#         while True:
#             user_input = input("You: ")
#             if user_input.lower() == 'quit':
#                 print("Recipe Chatbot: Goodbye! Enjoy your cooking!")
#                 break
            
#             #response = chatbot.chat(user_input)
#             print("THIS IS USER INPUT :"+user_input)
#             response = get_gemini_response(user_input)
#             print(f"Recipe Chatbot: {slow_print(response)}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         print("Please make sure you have the required libraries installed: nltk, numpy, scikit-learn")

# if __name__ == "__main__":
#     main()


import json
import random
import pickle
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import google.generativeai as genai
import asyncio
import dotenv

# Ensure NLTK data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class RecipeChatBot:
    def __init__(self, intents_file='recipe_intents.json', recipes_file='recipes.json', api_key=None):
        # Create necessary files if they don't exist
        self.create_sample_files(intents_file, recipes_file)
        
        # Initialize lemmatizer
        self.lemmatizer = WordNetLemmatizer()
        
        # Load recipe data
        with open(recipes_file, 'r') as file:
            self.recipes = json.load(file)
        
        # Load conversation intents
        with open(intents_file, 'r') as file:
            self.intents = json.load(file)
        
        # Initialize Gemini API if key is provided
        self.gemini_available = False
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
                self.gemini_available = True
                print("Gemini API initialized successfully!")
            except Exception as e:
                print(f"Failed to initialize Gemini API: {e}")
                print("Falling back to basic response generation.")
        
        # Train or load the model
        self.train_conversation_model()
        
        # Create cuisine lookup
        self.cuisine_recipes = {}
        for recipe in self.recipes:
            cuisine = recipe['cuisine']
            if cuisine not in self.cuisine_recipes:
                self.cuisine_recipes[cuisine] = []
            self.cuisine_recipes[cuisine].append(recipe)
        
        # Create ingredient index for recommendations
        self.ingredient_recipes = {}
        for recipe in self.recipes:
            for ingredient in recipe['ingredients']:
                if ingredient not in self.ingredient_recipes:
                    self.ingredient_recipes[ingredient] = []
                self.ingredient_recipes[ingredient].append(recipe)
        
        # Track conversation context
        self.context = {
            "current_cuisine": None,
            "liked_ingredients": [],
            "disliked_ingredients": [],
            "previous_recommendations": [],
            "conversation_history": []  # Track conversation for context
        }
    
    def create_sample_files(self, intents_file, recipes_file):
        """Create sample data files if they don't exist"""
        # Create sample recipe intents
        if not os.path.exists(intents_file):
            intents = {
                "intents": [
                    {
                        "tag": "greeting",
                        "patterns": ["Hi", "Hey", "Hello", "Good day", "Howdy", "What's up", "Hi there", "Hello there"],
                        "responses": [
                            "Hello! I'm your recipe assistant. How can I help you today?",
                            "Hi there! Looking for recipe recommendations?",
                            "Hey! Need help finding a delicious recipe?",
                            "Greetings! Ready to discover some amazing recipes?"
                        ]
                    },
                    {
                        "tag": "goodbye",
                        "patterns": ["Bye", "See you later", "Goodbye", "I'm leaving", "Have a good day", "That's all", "Thanks bye"],
                        "responses": [
                            "Goodbye! Enjoy your cooking!",
                            "See you later! Hope you find the perfect recipe!",
                            "Bye! Come back when you're hungry for more recipes!",
                            "Take care and happy cooking!"
                        ]
                    },
                    {
                        "tag": "thanks",
                        "patterns": ["Thanks", "Thank you", "That's helpful", "Thanks for the help", "Appreciate it", "Great thanks"],
                        "responses": [
                            "You're welcome! Cooking is all about sharing good food.",
                            "Happy to help! Enjoy your meal!",
                            "My pleasure! Let me know how the recipe turns out!",
                            "Anytime! Good luck with your cooking adventure!"
                        ]
                    },
                    {
                        "tag": "recommend_recipe",
                        "patterns": [
                            "Can you suggest a recipe?", 
                            "What should I cook?",
                            "I need a recipe",
                            "Recommend something to cook",
                            "Give me a recipe",
                            "What's good to make?",
                            "I'm hungry",
                            "I want to cook",
                            "Show me a recipe",
                            "Recipe recommendation please"
                        ],
                        "responses": ["Here's a recipe recommendation for you:"]
                    },
                    {
                        "tag": "cuisine_inquiry",
                        "patterns": [
                            "What cuisines do you know?",
                            "What types of food can you recommend?",
                            "Tell me about cuisines",
                            "What food types are available?",
                            "What kind of food do you have?",
                            "Which cuisines?",
                            "What ethnicity of food?"
                        ],
                        "responses": ["I can recommend various cuisines like:"]
                    },
                    {
                        "tag": "ingredient_inquiry",
                        "patterns": [
                            "What ingredients are popular?",
                            "Tell me about ingredients",
                            "What ingredients should I use?",
                            "Common ingredients in recipes",
                            "What can I cook with?",
                            "What ingredients do you know?",
                            "Tell me ingredients"
                        ],
                        "responses": ["Some popular ingredients include:"]
                    }
                ]
            }
            
            with open(intents_file, 'w') as f:
                json.dump(intents, f, indent=4)
        
        # Create sample recipes
        if not os.path.exists(recipes_file):
            recipes = [
                {
                    "id": 10259,
                    "cuisine": "greek",
                    "ingredients": [
                        "romaine lettuce",
                        "black olives",
                        "grape tomatoes",
                        "garlic",
                        "pepper",
                        "purple onion",
                        "seasoning",
                        "garbanzo beans",
                        "feta cheese crumbles"
                    ]
                },
                {
                    "id": 10260,
                    "cuisine": "italian",
                    "ingredients": [
                        "pasta",
                        "tomato sauce",
                        "garlic",
                        "basil",
                        "parmesan cheese",
                        "olive oil"
                    ]
                },
                {
                    "id": 10261,
                    "cuisine": "mexican",
                    "ingredients": [
                        "tortillas",
                        "beans",
                        "cheese",
                        "avocado",
                        "salsa",
                        "cilantro",
                        "lime"
                    ]
                },
                {
                    "id": 10262,
                    "cuisine": "indian",
                    "ingredients": [
                        "rice",
                        "chicken",
                        "curry powder",
                        "onion",
                        "garlic",
                        "ginger",
                        "tomatoes",
                        "yogurt",
                        "coriander"
                    ]
                },
                {
                    "id": 10263,
                    "cuisine": "chinese",
                    "ingredients": [
                        "rice",
                        "soy sauce",
                        "sesame oil",
                        "chicken",
                        "green onions",
                        "ginger",
                        "garlic",
                        "vegetables"
                    ]
                }
            ]
            
            with open(recipes_file, 'w') as f:
                json.dump(recipes, f, indent=4)
    
    def train_conversation_model(self):
        """Train the intent classification model using scikit-learn"""
        # Process intents data
        training_sentences = []
        training_labels = []
        self.classes = []
        
        # Extract training data from intents
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                training_sentences.append(pattern)
                training_labels.append(intent['tag'])
            if intent['tag'] not in self.classes:
                self.classes.append(intent['tag'])
        
        # Create vectorizer
        self.vectorizer = CountVectorizer(
            tokenizer=self.tokenize_and_lemmatize,
            ngram_range=(1, 2)
        )
        
        # Fit vectorizer and transform training data
        X = self.vectorizer.fit_transform(training_sentences)
        y = training_labels
        
        # Train classifier
        self.classifier = MultinomialNB()
        self.classifier.fit(X, y)
    
    def tokenize_and_lemmatize(self, text):
        """Tokenize and lemmatize text"""
        tokens = word_tokenize(text.lower())
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def predict_intent(self, message):
        """Predict the intent of a user message"""
        # Transform the message using vectorizer
        X = self.vectorizer.transform([message])
        
        # Get predictions
        intent_id = self.classifier.predict(X)[0]
        
        # Get probabilities
        probs = self.classifier.predict_proba(X)[0]
        prob = max(probs)
        
        # Return intent and probability
        return {'intent': intent_id, 'probability': prob}
    
    def extract_ingredients(self, message):
        """Extract ingredients mentioned in a message"""
        words = self.tokenize_and_lemmatize(message)
        stop_words = set(stopwords.words('english'))
        potential_ingredients = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Check against known ingredients
        all_ingredients = set()
        for recipe in self.recipes:
            for ingredient in recipe['ingredients']:
                all_ingredients.add(ingredient.lower())
        
        found_ingredients = []
        for word in potential_ingredients:
            for ingredient in all_ingredients:
                if word in ingredient:
                    found_ingredients.append(ingredient)
                    break
        
        return list(set(found_ingredients))  # Remove duplicates
    
    def extract_cuisine(self, message):
        """Extract cuisine type from message"""
        words = self.tokenize_and_lemmatize(message)
        cuisines = set(recipe['cuisine'] for recipe in self.recipes)
        
        for word in words:
            if word in cuisines:
                return word
        
        return None
    
    def recommend_recipe(self):
        """Recommend a recipe based on current context"""
        candidate_recipes = []
        
        # First, filter by cuisine if specified
        if self.context["current_cuisine"]:
            candidate_recipes = self.cuisine_recipes.get(self.context["current_cuisine"], [])
        else:
            candidate_recipes = self.recipes
        
        # Score recipes based on liked and disliked ingredients
        scored_recipes = []
        for recipe in candidate_recipes:
            # Skip previously recommended recipes if we have alternatives
            if recipe in self.context["previous_recommendations"] and len(self.context["previous_recommendations"]) < len(candidate_recipes):
                continue
                
            score = 0
            for ingredient in recipe['ingredients']:
                if ingredient in self.context["liked_ingredients"]:
                    score += 2
                if ingredient in self.context["disliked_ingredients"]:
                    score -= 3
            
            scored_recipes.append((recipe, score))
        
        # Sort by score
        scored_recipes.sort(key=lambda x: x[1], reverse=True)
        
        # Return top recipe or random if no preferences
        if scored_recipes:
            recommended_recipe = scored_recipes[0][0]
            self.context["previous_recommendations"].append(recommended_recipe)
            return recommended_recipe
        elif candidate_recipes:
            recommended_recipe = random.choice(candidate_recipes)
            self.context["previous_recommendations"].append(recommended_recipe)
            return recommended_recipe
        else:
            return None
    
    def get_recipe_data(self, recipe):
        """Prepare recipe data for Gemini or basic formatting"""
        if not recipe:
            return None
        
        recipe_data = {
            "cuisine": recipe['cuisine'],
            "id": recipe['id'],
            "ingredients": recipe['ingredients']
        }
        
        return recipe_data
    
    async def generate_gemini_response(self, prompt):
        """Generate a response using Gemini API"""
        try:
            # Ensure consistent quality by setting temperature and topP
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 1024,
            }
            
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
            
            response = await self.gemini_model.generate_content_async(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings,
            )
            
            if hasattr(response, 'text'):
                return response.text
            # Handle different response formats
            elif hasattr(response, 'parts'):
                return ''.join(part.text for part in response.parts)
            else:
                # Fallback - try to convert response to string
                return str(response)
        except Exception as e:
            print(f"Error with Gemini API: {e}")
            return None
    
    def basic_format_recipe(self, recipe_data):
        """Format a recipe for display without using Gemini"""
        if not recipe_data:
            return "I'm sorry, I couldn't find a recipe matching your preferences."
        
        result = f"Here's a {recipe_data['cuisine']} recipe I think you'll like:\n\n"
        result += f"Recipe ID: {recipe_data['id']}\n"
        result += "Ingredients:\n"
        for ingredient in recipe_data['ingredients']:
            result += f"- {ingredient}\n"
        
        # Add a cooking suggestion
        result += "\nTo prepare this dish, you'll typically want to combine these ingredients "
        
        if recipe_data['cuisine'] == 'italian':
            result += "and simmer them with pasta for a delicious meal."
        elif recipe_data['cuisine'] == 'mexican':
            result += "in a flavorful combination perfect for tacos or burritos."
        elif recipe_data['cuisine'] == 'indian':
            result += "with aromatic spices and cook them slowly for a rich flavor."
        elif recipe_data['cuisine'] == 'chinese':
            result += "and stir-fry them quickly over high heat."
        elif recipe_data['cuisine'] == 'greek':
            result += "in a fresh salad or wrap for a Mediterranean treat."
        else:
            result += "according to your preference."
        
        return result
    
    async def format_recipe_with_gemini(self, recipe_data):
        """Format a recipe using Gemini for more natural language"""
        if not recipe_data:
            return "I'm sorry, I couldn't find a recipe matching your preferences."
        
        cuisine_context = ""
        if recipe_data['cuisine'] == 'italian':
            cuisine_context = "Italian cuisine is known for its simple yet flavorful dishes often using herbs like basil, garlic, olive oil, and tomatoes."
        elif recipe_data['cuisine'] == 'mexican':
            cuisine_context = "Mexican cuisine features vibrant flavors with ingredients like chili peppers, corn, beans, and fresh herbs like cilantro."
        elif recipe_data['cuisine'] == 'indian':
            cuisine_context = "Indian cuisine is aromatic and rich with diverse spices like cumin, coriander, turmeric, and garam masala."
        elif recipe_data['cuisine'] == 'chinese':
            cuisine_context = "Chinese cuisine emphasizes balance, featuring techniques like stir-frying and ingredients like soy sauce, ginger, and garlic."
        elif recipe_data['cuisine'] == 'greek':
            cuisine_context = "Greek cuisine celebrates Mediterranean flavors with olive oil, fresh vegetables, herbs, and ingredients like feta cheese."
        
        prompt = f"""
        You are a passionate cooking assistant helping a user discover a new recipe. Create an engaging, personalized response recommending the following recipe.
        
        Recipe details:
        - Cuisine: {recipe_data['cuisine']}
        - Recipe ID: {recipe_data['id']}
        - Ingredients: {', '.join(recipe_data['ingredients'])}
        
        User preferences:
        - Liked ingredients: {', '.join(self.context['liked_ingredients']) if self.context['liked_ingredients'] else 'None specified'}
        - Disliked ingredients: {', '.join(self.context['disliked_ingredients']) if self.context['disliked_ingredients'] else 'None specified'}
        
        Cuisine context:
        {cuisine_context}
        
        Format your response to include:
        1. A warm, personalized introduction mentioning the cuisine type
        2. A brief sentence acknowledging any user preferences for ingredients
        3. A clear list of ingredients (make it sound appetizing)
        4. A brief description of how to prepare the dish, highlighting key techniques for this cuisine
        5. A friendly closing line encouraging them to try it
        
        Keep your response conversational, enthusiastic about food, and concise (around 150 words). Make the reader excited to try this recipe!
        """
        
        response = await self.generate_gemini_response(prompt)
        if response:
            return response
        else:
            # Fall back to basic formatting if Gemini fails
            return self.basic_format_recipe(recipe_data)
    
    async def enhance_basic_response(self, basic_response, intent_tag, user_message):
        """Use Gemini to enhance any basic response from the chatbot"""
        # Skip enhancement if Gemini is not available
        if not self.gemini_available:
            return basic_response
            
        prompt = f"""
        You are a friendly cooking assistant. Rewrite the following basic response to make it more natural, conversational, and engaging.
        
        Original basic response:
        "{basic_response}"
        
        Context:
        - User's message: "{user_message}"
        - Intent type: {intent_tag}
        
        Guidelines for your enhanced response:
        1. Keep the same information but make it sound more natural and personalized
        2. Add a touch of enthusiasm about cooking and food
        3. Keep it concise but warm (around 2-4 sentences)
        4. Maintain a conversational tone as if speaking directly to the user
        5. If appropriate, ask a gentle follow-up question to encourage further conversation
        
        Important: Do not make up new information that wasn't in the original response.
        """
        
        enhanced_response = await self.generate_gemini_response(prompt)
        if enhanced_response:
            return enhanced_response
        else:
            return basic_response
    
    async def generate_response(self, intent, message):
        """Generate a response based on intent and message content"""
        tag = intent['intent']
        
        # Update conversation history
        self.context["conversation_history"].append((message, ""))  # Placeholder for bot response
        
        # Extract context from message
        cuisine = self.extract_cuisine(message)
        if cuisine:
            self.context["current_cuisine"] = cuisine
        
        ingredients = self.extract_ingredients(message)
        if "like" in message.lower() or "love" in message.lower():
            for ingredient in ingredients:
                if ingredient not in self.context["liked_ingredients"]:
                    self.context["liked_ingredients"].append(ingredient)
        
        if "dislike" in message.lower() or "hate" in message.lower() or "don't like" in message.lower():
            for ingredient in ingredients:
                if ingredient not in self.context["disliked_ingredients"]:
                    self.context["disliked_ingredients"].append(ingredient)
        
        # Generate base response
        if tag == 'recommend_recipe':
            recipe = self.recommend_recipe()
            recipe_data = self.get_recipe_data(recipe)
            
            if self.gemini_available:
                response = await self.format_recipe_with_gemini(recipe_data)
            else:
                response = self.basic_format_recipe(recipe_data)
        elif tag == 'cuisine_inquiry':
            cuisines = list(self.cuisine_recipes.keys())
            base_response = f"I can recommend recipes from these cuisines: {', '.join(cuisines)}. Which one would you like to try?"
            
            if self.gemini_available:
                response = await self.enhance_basic_response(base_response, tag, message)
            else:
                response = base_response
        elif tag == 'ingredient_inquiry':
            # Get the most common ingredients across all recipes
            all_ingredients = []
            for recipe in self.recipes:
                all_ingredients.extend(recipe['ingredients'])
            
            # Count occurrences
            ingredient_counts = {}
            for ingredient in all_ingredients:
                if ingredient in ingredient_counts:
                    ingredient_counts[ingredient] += 1
                else:
                    ingredient_counts[ingredient] = 1
            
            # Get top ingredients
            top_ingredients = sorted(ingredient_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            top_ingredient_names = [item[0] for item in top_ingredients]
            
            base_response = f"Some popular ingredients in my recipes are: {', '.join(top_ingredient_names)}. Do you have any preferences?"
            
            if self.gemini_available:
                response = await self.enhance_basic_response(base_response, tag, message)
            else:
                response = base_response
        else:
            # Find the matching intent and return a response
            for intent_data in self.intents['intents']:
                if intent_data['tag'] == tag:
                    base_response = random.choice(intent_data['responses'])
                    
                    if self.gemini_available:
                        response = await self.enhance_basic_response(base_response, tag, message)
                    else:
                        response = base_response
                    break
            else:
                default_response = "I'm not sure I understand. Would you like me to recommend a recipe?"
                
                if self.gemini_available:
                    response = await self.enhance_basic_response(default_response, "unknown", message)
                else:
                    response = default_response
        
        # Update conversation history with the actual response
        self.context["conversation_history"][-1] = (message, response)
        
        return response
    
    async def chat(self, message):
        """Process a message and return a response"""
        try:
            # Predict intent
            intent = self.predict_intent(message)
            
            # Generate response based on intent
            response = await self.generate_response(intent, message)
            
            # Always enhance the final response with Gemini if available
            if self.gemini_available and "Here's a recipe" not in response and "Recipe ID:" not in response:
                # This ensures we don't double-enhance recipe recommendations
                enhanced_response = await self.enhance_basic_response(response, intent['intent'], message)
                return enhanced_response
            else:
                return response
        except Exception as e:
            # Error handling
            print(f"Error processing message: {e}")
            error_msg = "I'm having trouble understanding that. Would you like a recipe recommendation instead?"
            
            if self.gemini_available:
                try:
                    return await self.enhance_basic_response(error_msg, "error", message)
                except:
                    return error_msg
            else:
                return error_msg

import time
def slow_print(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # New line after printing

# Main function to run the chatbot
async def main():
    try:
        # Try to load API key from environment variables or .env file
        dotenv.load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            print("Warning: No Gemini API key found. Using basic response generation.")
            print("To use Gemini, set GEMINI_API_KEY in your environment or .env file.")
            print("For testing, you can enter an API key now:")
            manual_key = input("Enter Gemini API key (leave blank to skip): ")
            if manual_key.strip():
                api_key = manual_key
        
        chatbot = RecipeChatBot(api_key=api_key)
        
        print("Recipe Chatbot: Hello! I'm your recipe assistant. How can I help you today? (type 'quit' to exit)")
        
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                print("Recipe Chatbot: Goodbye! Enjoy your cooking!")
                break
            elif user_input.lower() == 'clear':
                # Clear the console based on OS
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Recipe Chatbot: Hello! I'm your recipe assistant. How can I help you today? (type 'quit' to exit)")
                continue
            
            response = await chatbot.chat(user_input)
            slow_print(response)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please make sure you have the required libraries installed: nltk, numpy, scikit-learn, google-generativeai, python-dotenv")

if __name__ == "__main__":
    asyncio.run(main())