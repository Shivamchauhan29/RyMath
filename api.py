from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rhymath import calculate_math, chatbot_trainer  

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
    math_keywords = ["solve", "simplify", "differentiate", "integrate", "derivative"]

    # Check if the input contains any math-related keyword
    if any(keyword in user_input.lower() for keyword in math_keywords):
        try:
            math_result = calculate_math(user_input)
            print("Math Result:", math_result)  # Debugging output
            
            # Ensure numeric results are returned properly
            if isinstance(math_result, (int, float)) or (isinstance(math_result, str) and math_result.replace(".", "").isdigit()):
                return {"response": str(math_result)}
            
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
