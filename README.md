# RyMath: AI Chatbot with Memory, Poem Generation, and Math Solver

## 🚀 Overview
RyMath is designed to maintain conversation history and provide intelligent responses using a fine-tuned GPT-2 model. Additionally, it features an integrated **math solver** using SymPy to handle calculations, differentiation, integration, equations, limits, and matrix operations. It can also generate **poems** based on user input, making it a creative AI assistant.

## 💂️ Project Structure
```
│── dataset.py         # Handles data processing and chatbot training
│── rymath.py         # Main script to run RyMath
│── api.py             # Backend API for UI integration
│── requirements.txt   # Dependencies for the project
│── README.md          # Project documentation
│── conversation_data.json # Stores conversation history
│── chatbot_model/     # Model storage directory
│── rymath-ui/        # React-based frontend UI
```  

## 🛠️ Setup Instructions  
### 1️⃣ Install Backend Dependencies  
Ensure Python 3.8+ is installed, then install the required dependencies:  
```sh
pip install -r requirements.txt
```  

### 2️⃣ Install Frontend Dependencies  
Navigate to the frontend folder and install dependencies:  
```sh
cd rymath-ui  
npm install  
```  

### 3️⃣ Download & Initialize the Model  
Before running the backend, initialize the model:  
```python
from dataset import ChatbotTrainer  
chatbot_trainer = ChatbotTrainer()  
chatbot_trainer.initialize_model()  
```  

---

## 🚀 Running the Project  
### Start Backend Server  
Run the backend service:  
```sh
python3 api.py  
```
Or using Uvicorn:
```sh
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```  

### Start Frontend UI  
In a separate terminal, start the React frontend:  
```sh
cd rymath-ui  
npm start  
```  

The application will be available at `http://localhost:3000`. 🎯

## 🧠 Features
✅ **Memory-Based Conversations** – Maintains a short-term conversation history (last 5 interactions).  
✅ **GPT-2 Response Generation** – Generates human-like responses using GPT-2.  
✅ **Poem Generation** – Creates original poetry based on user prompts.  
✅ **Math Solver** – Handles complex mathematical expressions using SymPy.  
✅ **Equation Solving** – Solves algebraic equations like `solve x^2 + 5*x + 6 = 0`.  
✅ **Differentiation & Integration** – Computes derivatives and integrals, e.g., `differentiate x^3 + 6*x`.  
✅ **Trigonometry & Logarithms** – Supports functions like `sin(x)`, `log(x)`, etc.  
✅ **Matrix Operations** – Computes determinants, inverses, and matrix multiplications.  

## 🎯 Usage Examples
```sh
User: Write a poem about the ocean
RyMath: 🌊 The ocean whispers, deep and wide,
        Its waves embrace the changing tide...

User: solve x^2 + 5*x + 6 = 0
RyMath: ✅ Solution: x = -2, x = -3

User: differentiate x^3 + 6*x
RyMath: ✅ Derivative: 3*x^2 + 6

User: integrate sin(x) + x^2
RyMath: ✅ Integral: -cos(x) + x^3/3 + C

User: matrix [[1, 2], [3, 4]] determinant
RyMath: ✅ Determinant: -2
       ✅ Inverse:
       [[-2  1]
        [ 1 -0.5]]
```

## 🤝 Contribution
Feel free to contribute! Fork the repository, create a branch, make improvements, and submit a pull request.

<!--## 🌜 License
This project is open-source under the MIT License.
-->
## 🔗 Connect
📧 **Email**: chauhanshivam2310@gmail.com , yashpundeer0@gmail.com
<!-- 🌐 **Website**: your-website.com -->
🚀 **#LetsGrowTogether**

