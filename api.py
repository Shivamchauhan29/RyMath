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
    
    math_keywords = ["differentiate", "derivative", "solve", "simplify", "integrate", "limit"]
    detected_keyword = None
    
    for keyword in math_keywords:
        if keyword in user_input.lower():
            detected_keyword = keyword
            break
    
    if detected_keyword:
        try:
            match = re.search(rf"{detected_keyword}\s+([0-9a-zA-Z+\-*/^=()., ]+)", user_input, re.IGNORECASE)
            math_expression = match.group(1) if match else user_input
            math_result = calculate_math(math_expression, detected_keyword)
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
