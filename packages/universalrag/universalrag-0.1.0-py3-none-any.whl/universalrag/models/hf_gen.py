import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL_NAME", "HuggingFaceH4/zephyr-7b-beta")

# ✅ Setup client with Featherless provider
client = InferenceClient(
    model=HF_MODEL,
    api_key=HF_TOKEN,
    provider="featherless-ai",
)

def generate_answer(question, chunks):
    context = "\n".join(chunks[:3])  # limit context to avoid token overflow
    prompt = f"Answer the following question based on the context:\n\n{context}\n\nQ: {question}"

    try:
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=256,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Featherless API call failed: {e}"
