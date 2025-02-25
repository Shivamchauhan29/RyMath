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
    
    math_keywords = keyword_mapping.keys()
    detected_operation = None
    for keyword in math_keywords:
        if keyword in user_input.lower():
            detected_operation = keyword_mapping[keyword]
            break

    if detected_operation:
        try:
            # Pattern to capture math expression following any keyword, optionally preceded by "of"
            pattern = rf"(?:{'|'.join(re.escape(k) for k in keyword_mapping.keys())})\s+(?:of\s+)?([0-9a-zA-Z+\-*/^=()., ]+)"
            match = re.search(pattern, user_input, re.IGNORECASE)
            math_expression = match.group(1).strip() if match else user_input
            
            # Remove trailing non-math words like "for", "me", "please" (using word boundary)
            math_expression = re.sub(r'\s+(for|me|please)\b[\s\?\!\.]*$', '', math_expression, flags=re.IGNORECASE)
            
            math_result = calculate_math(math_expression, detected_operation)
            print("Math Result:", math_result)  # Debugging output
            
            return {"response": math_result}

        except Exception as e:
            print(f"Math function error: {e}")
            return {"response": "❌ Error processing mathematical request."}

    # If no math keyword is detected, process it through chatbot
    response = chatbot_trainer.generate_response(user_input)
    print("Chatbot Response:", response)  # Debugging output

    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
