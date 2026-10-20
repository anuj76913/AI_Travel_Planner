import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Initialize the Groq model
def get_groq_llm(model_name: str = "openai/gpt-oss-120b", temperature: float = 0.0):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set. Please set it in .env file.")
        
    return ChatGroq(
        groq_api_key=api_key,
        model_name=model_name,
        temperature=temperature
    )

from langchain_google_genai import ChatGoogleGenerativeAI

def get_gemini_llm(model_name: str = None, temperature: float = 0.0):
    """Initialize the Gemini model for the Review Agent."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY environment variable not set. Please set it in .env file.")
        
    if model_name is None:
        model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-3.5-flash-lite")

    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=temperature
    )
