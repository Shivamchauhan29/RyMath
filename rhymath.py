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

def detect_intent(user_input):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(user_input.lower())
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # Define intents based on keywords
    if any(word in filtered_tokens for word in ["solve", "simplify", "differentiate", "integrate", "derivative"]):
        return "math"
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

def calculate_math(expression):
    print('expression:', expression)
    try:
        print('Math function triggered!')

        # Define symbols
        x, y = sp.symbols('x y')

        # Clean the expression
        clean_expr = (expression
                      .replace("differentiate", "")
                      .replace("derivative", "")
                      .replace("integrate", "")
                      .replace("simplify", "")
                      .replace("solve", "")
                      .replace("limit", "")
                      .replace("matrix", "")
                      .strip())

        steps = []  # Store steps for LaTeX rendering

        # **Solving Equations with Steps**
        if "solve" in expression:
            lhs, rhs = clean_expr.split("=")
            eq = sp.Eq(sp.sympify(lhs, locals={'x': x, 'y': y}),
                       sp.sympify(rhs, locals={'x': x, 'y': y}))
            solution = sp.solve(eq, x)

            steps.append(f"\\text{{Given Equation: }} {sp.latex(eq)}")
            if isinstance(solution, list):
                for idx, sol in enumerate(solution, 1):
                    steps.append(f"\\text{{Solution {idx}: }} {sp.latex(sol)}")
            else:
                steps.append(f"\\text{{Solution: }} {sp.latex(solution)}")

            # Combine steps and wrap in aligned
            steps_str = " \\\\ ".join(steps)
            latex_output = rf"""\begin{{aligned}}
{steps_str}
\end{{aligned}}"""
            return latex_output

        # **Simplification with Steps**
        elif "simplify" in expression:
            expr = sp.sympify(clean_expr, locals={'x': x, 'y': y})
            simplified_expr = sp.simplify(expr)

            steps.append(f"\\text{{Original Expression: }} {sp.latex(expr)}")
            steps.append(f"\\text{{Simplified Expression: }} {sp.latex(simplified_expr)}")

            steps_str = " \\\\ ".join(steps)
            latex_output = rf"""\begin{{aligned}}
{steps_str}
\end{{aligned}}"""
            return latex_output

        # **Differentiation with Steps**
        elif "differentiate" in expression or "derivative" in expression:
            expr = sp.sympify(clean_expr, locals={'x': x, 'y': y})
            derivative = sp.diff(expr, x)

            steps.append(f"\\text{{Function: }} {sp.latex(expr)}")
            steps.append(f"\\text{{Derivative: }} {sp.latex(derivative)}")

            steps_str = " \\\\ ".join(steps)
            latex_output = rf"""\begin{{aligned}}
{steps_str}
\end{{aligned}}"""
            return latex_output

        # **Integration with Steps**
        elif "integrate" in expression:
            expr = sp.sympify(clean_expr, locals={'x': x, 'y': y})
            integral = sp.integrate(expr, x)

            steps.append(f"\\text{{Function: }} {sp.latex(expr)}")
            steps.append(f"\\text{{Integral: }} {sp.latex(integral)}")

            steps_str = " \\\\ ".join(steps)
            latex_output = rf"""\begin{{aligned}}
{steps_str}
\end{{aligned}}"""
            return latex_output

        # **Limits**
        elif "limit" in expression:
            limit_expr, point = clean_expr.split(" at ")
            limit_result = sp.limit(sp.sympify(limit_expr, locals={'x': x}), x, float(point))

            steps.append(f"\\text{{Limit Expression: }} {sp.latex(sp.sympify(limit_expr, locals={'x': x}))}")
            steps.append(f"\\text{{Limit Result: }} {sp.latex(limit_result)}")

            steps_str = " \\\\ ".join(steps)
            latex_output = rf"""\begin{{aligned}}
{steps_str}
\end{{aligned}}"""
            return latex_output

        # **General Math Evaluation**
        else:
            result = sp.sympify(expression, locals={'x': x, 'y': y})
            steps.append(f"\\text{{Expression: }} {sp.latex(result)}")

            steps_str = " \\\\ ".join(steps)
            latex_output = rf"""\begin{{aligned}}
{steps_str}
\end{{aligned}}"""
            return latex_output

    except (sp.SympifyError, TypeError, ValueError, IndexError, ZeroDivisionError) as e:
        return f"❌ Oops! I couldn't understand the math expression. Error: {str(e)}"

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

