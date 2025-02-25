from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rymath import calculate_math, chatbot_trainer  
import re

app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest(BaseModel):
    user_input: str

@app.post("/chat")
def chat(request: ChatRequest):
    user_input = request.user_input.strip()
    
    # First, check if input contains any math characters/operators.
    if not re.search(r'[0-9+\-*/^=()]+', user_input):
        # Process as a normal chatbot request if no math symbols are found.
        response = chatbot_trainer.generate_response(user_input)
        print("Chatbot Response:", response)
        return {"response": response}
    
    # Define mapping of keywords to operations.
    keyword_mapping = {
        "differentiate": "differentiate",
        "derivative": "differentiate",
        "solve": "solve",
        "simplify": "simplify",
        "integrate": "integrate",
        "limit": "limit",
        "roots": "solve",
        "find roots": "solve",
        "zeroes": "solve",
        "roots of": "solve"
    }
    
    detected_operation = None
    for keyword in keyword_mapping:
        if keyword in user_input.lower():
            detected_operation = keyword_mapping[keyword]
            break

    if detected_operation:
        try:
            # Updated regex: after the keyword, optionally remove "of" before capturing the math expression.
            pattern = rf"(?:{'|'.join(re.escape(k) for k in keyword_mapping.keys())})\s+(?:of\s+)?([0-9a-zA-Z+\-*/^=()., ]+)"
            match = re.search(pattern, user_input, re.IGNORECASE)
            math_expression = match.group(1).strip() if match else user_input
            math_result = calculate_math(math_expression, detected_operation)
            print("Math Result:", math_result)
            
            return {"response": math_result}

        except Exception as e:
            print(f"Math function error: {e}")
            return {"response": "❌ Error processing mathematical request."}

    # If no math keyword is detected, process it through chatbot
    response = chatbot_trainer.generate_response(user_input)
    print("Chatbot Response:", response)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
