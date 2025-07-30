import os
from dotenv import load_dotenv
import requests
from universalrag.utility.summarizer import safe_summarize_large_text, summarize_with_api

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def summarize_func(prompt):
    return summarize_with_api(
        prompt,
        model="llama-3.1-8b-instant",
        api_key=GROQ_API_KEY,
        api_url="https://api.groq.com/openai/v1/chat/completions"
    )

def generate_answer(question, chunks):
    full_text = "\n".join(chunks)
    
    if len(full_text.split()) > 3000:
        return safe_summarize_large_text(summarize_func, full_text, question=question)
    else:
        return summarize_func(full_text + f"\n\nNow answer this: {question}")
