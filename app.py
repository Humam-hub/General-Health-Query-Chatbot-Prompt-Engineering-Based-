import streamlit as st
from groq import Groq
import re
from typing import List, Dict

# Safety keywords and phrases to flag potentially harmful queries
SAFETY_KEYWORDS = [
    'suicide', 'kill myself', 'end my life', 'self harm', 'cut myself',
    'overdose', 'drug abuse', 'eating disorder', 'anorexia', 'bulimia',
    'prescription drug', 'medication dosage', 'drug interaction',
    'emergency', 'chest pain', 'heart attack', 'stroke', 'severe bleeding',
    'unconscious', 'difficulty breathing', 'allergic reaction'
]

RESTRICTED_TOPICS = [
    'specific medication dosages', 'drug interactions', 'prescription advice',
    'diagnosis', 'treatment plans', 'surgery recommendations'
]

class HealthChatbot:
    def __init__(self):
        self.client = None
        
    def initialize_client(self):
        """Initialize Groq client using Streamlit secrets"""
        try:
            api_key = st.secrets["GROQ_API_KEY"]
            self.client = Groq(api_key=api_key)
            return True
        except KeyError:
            st.error("❌ **Configuration Error**: GROQ_API_KEY not found in secrets. Please add it to your .streamlit/secrets.toml file.")
            return False
        except Exception as e:
            st.error(f"❌ **Client Error**: {str(e)}")
            return False
    
    def check_safety(self, query: str) -> tuple[bool, str]:
        """Check if the query contains potentially harmful content"""
        query_lower = query.lower()
        
        # Check for emergency keywords
        emergency_keywords = ['emergency', 'chest pain', 'heart attack', 'stroke', 
                            'severe bleeding', 'unconscious', 'difficulty breathing', 
                            'allergic reaction', 'choking']
        
        for keyword in emergency_keywords:
            if keyword in query_lower:
                return False, "🚨 **EMERGENCY ALERT**: If you're experiencing a medical emergency, please call emergency services (911 in US, 999 in UK, 112 in EU) immediately or go to your nearest emergency room. This chatbot cannot provide emergency medical assistance."
        
        # Check for self-harm keywords
        self_harm_keywords = ['suicide', 'kill myself', 'end my life', 'self harm', 'cut myself']
        for keyword in self_harm_keywords:
            if keyword in query_lower:
                return False, "🆘 **CRISIS SUPPORT**: If you're having thoughts of self-harm, please reach out for help immediately:\n\n• **National Suicide Prevention Lifeline**: 988 (US)\n• **Crisis Text Line**: Text HOME to 741741\n• **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/\n\nYou're not alone, and help is available."
        
        # Check for medication/prescription queries
        medication_keywords = ['prescription', 'dosage', 'medication', 'drug interaction', 'pills']
        for keyword in medication_keywords:
            if keyword in query_lower:
                return False, "⚠️ **MEDICATION SAFETY**: I cannot provide advice about prescription medications, dosages, or drug interactions. Please consult with:\n\n• Your doctor or pharmacist\n• A licensed healthcare provider\n• Your local pharmacy\n\nMedication decisions should always be made with professional medical guidance."
        
        return True, ""
    
    def get_system_prompt(self) -> str:
        return """You are a helpful health information chatbot. Your role is to provide general health and wellness information only. Follow these critical guidelines:

SAFETY RULES:
1. NEVER provide medical diagnoses or attempt to diagnose conditions
2. NEVER recommend specific treatments, medications, or dosages
3. NEVER provide emergency medical advice
4. ALWAYS encourage users to consult healthcare professionals for medical concerns
5. Provide only general health education and wellness information

RESPONSE STYLE:
- Be friendly, empathetic, and supportive
- Keep responses concise but informative
- Use simple, easy-to-understand language
- Include appropriate disclaimers about seeking professional medical advice

TOPICS YOU CAN DISCUSS:
- General health and wellness tips
- Lifestyle factors (diet, exercise, sleep)
- Basic anatomy and physiology education
- General information about common health conditions
- Mental health awareness and coping strategies
- Preventive care importance

ALWAYS END RESPONSES WITH:
"💡 Remember: This information is for educational purposes only. For medical concerns, please consult with a qualified healthcare provider."

Be helpful while prioritizing user safety above all else."""

    def generate_response(self, query: str, conversation_history: List[Dict]) -> str:
        """Generate response using Groq client"""
        if not self.client:
            return "⚠️ Please check your API key configuration in secrets.toml"
        
        # Check safety first
        is_safe, safety_message = self.check_safety(query)
        if not is_safe:
            return safety_message
        
        # Prepare conversation for API
        messages = [{"role": "system", "content": self.get_system_prompt()}]
        
        # Add conversation history
        for msg in conversation_history[-5:]:  # Keep last 5 exchanges for context
            messages.append(msg)
        
        # Add current query
        messages.append({"role": "user", "content": query})
        
        try:
            completion = self.client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=messages,
                temperature=0.7,
                max_completion_tokens=1500,
                top_p=0.95,
                stream=False,
                stop=None,
            )
            
            ai_response = completion.choices[0].message.content
            
            return ai_response
            
        except Exception as e:
            error_msg = str(e)
            if "api_key" in error_msg.lower():
                return "❌ **API Key Error**: Please check your Groq API key in the sidebar."
            elif "rate_limit" in error_msg.lower():
                return "❌ **Rate Limit**: Too many requests. Please wait a moment and try again."
            elif "model" in error_msg.lower():
                return "❌ **Model Error**: The model may not be available. Please try again later."
            else:
                return f"❌ **Error**: {error_msg}"

def main():
    st.set_page_config(
        page_title="Health Assistant Chatbot",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize chatbot and client
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = HealthChatbot()
        st.session_state.chatbot.initialize_client()
    
    # Initialize conversation history
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚠️ Important Safety Information")
        st.markdown("""
        **This chatbot is for educational purposes only and should NOT be used for:**
        - Medical emergencies
        - Specific medical diagnoses
        - Medication advice
        - Treatment recommendations
        
        **For emergencies, call:**
        - 🚨 Emergency Services: 911 (US)
        - 🆘 Crisis Hotline: 988 (US)
        """)
        
        st.markdown("---")
        
        if st.button("Clear Conversation"):
            st.session_state.conversation_history = []
            st.rerun()
    
    # Main chat interface
    st.title("🏥 Health Assistant Chatbot")
    st.markdown("*Your friendly health information companion*")
    
    # Display safety disclaimer
    st.info("⚠️ **Disclaimer**: This chatbot provides general health information only. Always consult healthcare professionals for medical advice, diagnosis, or treatment.")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display conversation history
        for i, msg in enumerate(st.session_state.conversation_history):
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about general health topics..."):
        # Add user message to conversation
        st.session_state.conversation_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.generate_response(
                    prompt, 
                    st.session_state.conversation_history[:-1]  # Exclude the current user message
                )
            
            st.write(response)
            
            # Add assistant response to conversation
            st.session_state.conversation_history.append({"role": "assistant", "content": response})
    
    # Example queries
    if not st.session_state.conversation_history:
        st.markdown("### 💭 Example Questions You Can Ask:")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            - "What are some tips for better sleep?"
            - "How can I boost my immune system?"
            - "What are the benefits of regular exercise?"
            """)
        
        with col2:
            st.markdown("""
            - "How much water should I drink daily?"
            - "What foods are good for heart health?"
            - "How can I manage stress better?"
            """)

if __name__ == "__main__":
    main()