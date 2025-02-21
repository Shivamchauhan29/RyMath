from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rhymath import RhyMath  # Import your chatbot

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load chatbot
chatbot = RhyMath()
chatbot.initialize_model()

# Request model
class ChatRequest(BaseModel):
    user_input: str

@app.post("/chat")
def chat(request: ChatRequest):
    response = chatbot.generate_response(request.user_input)
    return {"response": response}

@app.post("/math")
def math_solver(request: ChatRequest):
    response = chatbot.calculate_math(request.user_input)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
