# RhyMath: AI Chatbot with Memory, Poem Generation, and Math Solver

## 🚀 Overview
RhyMath is designed to maintain conversation history and provide intelligent responses using a fine-tuned GPT-2 model. Additionally, it features an integrated **math solver** using SymPy to handle calculations, differentiation, integration, equations, limits, and matrix operations. It can also generate **poems** based on user input, making it a creative AI assistant.

## 📂 Project Structure
```
/ai-chatbot-project
│── dataset.py         # Handles data processing and chatbot training
│── rhymath.py         # Main script to run RhyMath
│── requirements.txt   # Dependencies for the project
│── README.md          # Project documentation
│── conversation_data.json # Stores conversation history
│── chatbot_model/     # Model storage directory
```

## 🛠️ Setup Instructions
### 1️⃣ Install Dependencies
Make sure you have Python 3.8+ installed, then install the required dependencies:
```sh
pip install -r requirements.txt
```

### 2️⃣ Download & Initialize the Model
RhyMath uses a **GPT-2** model. Before running it, initialize the model:
```python
from dataset import ChatbotTrainer
chatbot_trainer = ChatbotTrainer()
chatbot_trainer.initialize_model()
```

### 3️⃣ Run RhyMath
Start the chatbot interface with:
```sh
python rhymath.py
```

## 🧠 Features
✅ **Memory-Based Conversations** – Maintains a short-term conversation history (last 5 interactions).  
✅ **GPT-2 Response Generation** – Generates human-like responses using GPT-2.  
✅ **Poem Generation** – Creates original poetry based on user prompts.  
✅ **Math Solver** – Handles complex mathematical expressions using SymPy.  
✅ **Equation Solving** – Solves algebraic equations like `solve x**2 - 4*x + 4 = 0`.  
✅ **Differentiation & Integration** – Computes derivatives and integrals, e.g., `differentiate x**3 + 6x`.  
✅ **Trigonometry & Logarithms** – Supports functions like `sin(x)`, `log(x)`, etc.  
✅ **Matrix Operations** – Computes determinants and inverses of matrices.  

## 🎯 Usage Examples
```sh
User: solve x**2 - 4*x + 4 = 0
RhyMath: ✅ Solution: [2]

User: differentiate x**3 + 6*x
RhyMath: ✅ Derivative: 3*x**2 + 6

User: integrate sin(x) + x**2
RhyMath: ✅ Integral: -cos(x) + x**3/3

User: matrix [1 2; 3 4]
RhyMath: ✅ Determinant: -2
       ✅ Inverse:
       [-2  1]
       [1  -0.5]

User: Write a poem about the ocean
RhyMath: 🌊 The ocean whispers, deep and wide,
        Its waves embrace the changing tide...
```

## 🤝 Contribution
Feel free to contribute! Fork the repository, create a branch, make improvements, and submit a pull request.

## 📜 License
This project is open-source under the MIT License.

## 🔗 Connect
📧 **Email**: your-email@example.com  
🌐 **Website**: your-website.com  
🚀 **#LetsGrowTogether**

