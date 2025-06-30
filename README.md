# 🏥 HealthChatBot

A friendly, safety-first health information chatbot built with Streamlit and Groq LLM. This chatbot provides general health and wellness information, focusing on user safety and responsible AI use. **It does not provide medical advice, diagnosis, or emergency assistance.**

## Features
- Conversational health and wellness information
- Strict safety checks for emergencies, self-harm, and medication queries
- Friendly, empathetic, and supportive responses
- Example questions to guide users
- Sidebar with safety disclaimers and quick reset

## Getting Started

### Prerequisites
- Python 3.8+

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/HealthChatBot.git
   cd HealthChatBot
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Key:**
   - Create a file at `.streamlit/secrets.toml` with the following content:
     ```toml
     GROQ_API_KEY = "your_groq_api_key_here"
     ```
   - Replace `your_groq_api_key_here` with your actual [Groq API key](https://console.groq.com/).

### Running the App
```bash
streamlit run app.py
```

The app will open in your browser. You can now chat with the Health Assistant Chatbot about general health topics.

## Usage
- Type your health-related question in the chat input.
- The chatbot will respond with general information and always remind you to consult a healthcare professional for medical concerns.
- Use the sidebar to clear the conversation or review safety information.

## Safety & Limitations
- **No medical advice:** The chatbot does not provide medical diagnoses, treatment recommendations, or medication advice.
- **Emergencies:** For emergencies, always call your local emergency number (e.g., 911 in the US).
- **Privacy:** Do not share personal, sensitive, or identifying health information.

## Example Questions
- "What are some tips for better sleep?"
- "How can I boost my immune system?"
- "What foods are good for heart health?"
- "How can I manage stress better?"

## License
MIT License

## Acknowledgments
- [Streamlit](https://streamlit.io/)
- [Groq](https://groq.com/)

---

> 💡 **Disclaimer:** This chatbot is for educational purposes only. For medical concerns, always consult with a qualified healthcare provider. 
