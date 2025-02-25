import sympy as sp
from transformers import pipeline
import language_tool_python
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random
from dataset import ChatbotTrainer
from fastapi import FastAPI
from pydantic import BaseModel
import re
from math_scraper import get_wikipedia_summary
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    user_message = request.message
    return {"response": f"You said: {user_message}"}



# Initialize chatbot trainer
chatbot_trainer = ChatbotTrainer()

# Ensure necessary NLTK data is available
# Ensure necessary NLTK data is available
try:
    nltk.download('punkt')
    nltk.download('stopwords')
    from nltk.corpus import stopwords  # Ensure stopwords is imported after downloading
except Exception as e:
    print(f"Error downloading NLTK resources: {str(e)}")
    print("Please ensure you have an active internet connection.")


# Initialize LanguageTool for Grammar correction
try:
    tool = language_tool_python.LanguageTool('en-US')
except Exception:
    print("Downloading LanguageTool... This may take a few minutes.")
    tool = language_tool_python.LanguageTool('en-US', remote_server='https://api.languagetool.org')

# Conversation history to maintain context
conversation_history = []

# Friendly responses for casual conversation
FRIENDLY_RESPONSES = [
    "That sounds amazing! Tell me more about that.",
    "Wow, you're really into that! What happened next?",
    "That's super cool! How did that make you feel?",
    "Yay, that's awesome! What else is on your mind?",
    "I love hearing your stories! Keep going!",
    "Sounds interesting! Keep me posted with more details.",
    "I'm all ears! What else do you have to share?",
    "That sounds like fun! What's next on your mind?"
]
# def fetch_math_info(query):
#     print(f"Fetching math info for: {query}")  # Debugging statement
#     try:
#         result = get_wikipedia_summary(query)
#         print(f"Scraper returned: {result[:200]}...")  # Print first 200 characters to check output
#         return result
#     except Exception as e:
#         print(f"Error in fetch_math_info: {str(e)}")  # Debugging error
#         return f"Could not fetch data: {str(e)}"


def detect_intent(user_input):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(user_input.lower())
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # Define intents based on keywords
    if any(word in filtered_tokens for word in ["solve", "simplify", "differentiate", "integrate", "derivative"]):
        return "math"
    elif "math info" in user_input.lower():
        return "math_info"
    elif "poem" in filtered_tokens or "paragraph" in filtered_tokens:
        return "poem"
    elif "grammar" in filtered_tokens:
        return "grammar"
    elif "train" in filtered_tokens:
        return "train"
    elif any(word in filtered_tokens for word in ['hi', 'hello', 'hey']):
        return "greeting"
    elif any(word in filtered_tokens for word in ['bye', 'exit', 'quit']):
        return "exit"
    else:
        return "chat"

def handle_invalid_input(user_input):
    intent = detect_intent(user_input)
    if intent == "unknown":
        return "Hmm, I didn't quite get that. Could you clarify what you're asking?"
    return None

def calculate_math(expression, operation):
    print('Expression:', expression)
    print('Operation:', operation)
    
    try:
        x, y = sp.symbols('x y')

        # Ensure proper formatting
        expression = expression.replace("^", "**")
        expression = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)

        expr = sp.sympify(expression, locals={'x': x, 'y': y})
        steps = [f"\\text{{Given Expression: }} {sp.latex(expr)}"]

        if operation in ["differentiate", "derivative"]:
            result = sp.diff(expr, x)
            steps.append(f"\\text{{Derivative: }} {sp.latex(result)}")

        elif operation == "integrate":
            result = sp.integrate(expr, x)
            steps.append(f"\\text{{Integral: }} {sp.latex(result)}")

        elif operation == "solve":
            if "=" in expression:
                lhs, rhs = expression.split("=")
                eq = sp.Eq(sp.sympify(lhs, locals={'x': x, 'y': y}), sp.sympify(rhs, locals={'x': x, 'y': y}))
            else:
                eq = sp.Eq(expr, 0)
            
            result = sp.solve(eq, x)
            steps.append(f"\\text{{Solution: }} {sp.latex(result)}")

        elif operation == "simplify":
            result = sp.simplify(expr)
            steps.append(f"\\text{{Simplified Expression: }} {sp.latex(result)}")

        elif operation == "limit":
            try:
                limit_expr, point = expression.split(" at ")
                result = sp.limit(sp.sympify(limit_expr, locals={'x': x}), x, float(point))
                steps.append(f"\\text{{Limit Computation: }} {sp.latex(result)}")
            except ValueError:
                return "❌ \\text{Invalid limit syntax. Use format: } \\text{limit(expr at point)}"

        else:
            return "❌ \\text{Unknown operation.}"

        # Format as LaTeX output
        steps_str = " \\\\ ".join(steps)
        return rf"""\begin{{aligned}}
{steps_str}
\end{{aligned}}"""

    except (sp.SympifyError, TypeError, ValueError, IndexError, ZeroDivisionError) as e:
        return f"❌ \\text{{Error: }} {str(e)}"

def generate_poem(prompt):
    try:
        # Use the local GPT-2 model for poem generation
        return chatbot_trainer.generate_response(f"Write a poem about {prompt}")
    except Exception as e:
        print(f"Poem Generation Error: {str(e)}")
        return "Sorry, I couldn't generate a poem right now. Let's try something else!"

def check_grammar(text):
    try:
        if not text.strip():
            return "Please provide a sentence for grammar checking."
        
        matches = tool.check(text)
        if matches:
            corrected_text = language_tool_python.utils.correct(text, matches)
            return f"✅ Here's your corrected text: {corrected_text}\n\nFound {len(matches)} grammar issues."
        else:
            return "Your text looks great! No grammar issues found. 🎉"
    except Exception as e:
        return f"❌ Sorry, something went wrong while checking the grammar. Error: {str(e)}"

def generate_friendly_response():
    return random.choice(FRIENDLY_RESPONSES)

def get_user_name():
    name = input("Hey there! What's your name? 😊 ")
    print(f"Nice to meet you, {name}!")
    return name

def chatbot():
    name = get_user_name()
    
    print(f"Hey {name}! I’m your friendly chatbot. 😊")
    print("I can help you with:")
    print("- Solving math problems (e.g., '2 + 2 * 3')")
    print("- Writing poems (e.g., 'write a poem about nature')")
    print("- Checking grammar (e.g., 'check grammar: This is a test')")
    print("- Training my conversation skills (type 'train me')")
    print("- Or we can just chat! 💬")
    print("Just type 'exit', 'quit', or 'bye' if you want to leave.")
    
    while True:
        user_input = input(f"\n{name}: ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print(f"Goodbye, {name}! It was wonderful talking to you. Take care! 👋")
            break
        
        invalid_input_response = handle_invalid_input(user_input)
        if invalid_input_response:
            print(invalid_input_response)
            continue
        
        intent = detect_intent(user_input)
        if intent == "math":
            print(calculate_math(user_input))
        elif intent == "poem":
            prompt = user_input.replace("poem", "").replace("paragraph", "").strip()
            print(generate_poem(prompt))
        elif intent == "grammar":
            text_to_check = user_input.lower().replace("grammar", "").strip()
            if text_to_check:
                print(check_grammar(text_to_check))
            else:
                print("Please provide a sentence or phrase to check grammar for.")
        elif intent == "train":
            print("Starting training... This may take a few minutes.")
            chatbot_trainer.train()
            print("Training complete! I'm ready to chat better now!")
        elif intent == "greeting":
            print(f"Hi {name}! How can I brighten your day today?")
        # elif intent == "math_info":
        #     query = user_input.replace("math info", "").strip()
        #     print(fetch_math_info(query))
        elif intent == "chat":
            response = chatbot_trainer.generate_response(user_input)
            print(response)
            
            # Save the conversation data for further training
            chatbot_trainer.add_conversation(user_input, response)
            
        else:
            print("I’m here to chat! What’s on your mind today?")

        conversation_history.append((user_input, intent))
        
        print("\nWhat else can I help you with? Feel free to ask about math, poetry, grammar, or just chat!")

if __name__ == "__main__":
    chatbot()

