# universalrag/utils/summarizer.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def split_into_chunks(text, max_words=800):
    """Splits a long text into smaller chunks of given max_words."""
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]


def summarize_with_api(prompt, model, api_key, api_url):
    """
    Generic summarization function for Groq, OpenAI, or any compatible chat model API.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        response_data = response.json()

        if "choices" not in response_data or not response_data["choices"]:
            raise ValueError("API returned no choices")

        return response_data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ Failed to summarize with API: {e}"


def safe_summarize_large_text(
    summarizer_func,
    text,
    question=None,
    chunk_words=800
):
    """
    Safely summarizes long text in parts, then combines into a final answer or summary.
    Useful to avoid token limits and 413 errors.
    """
    chunks = split_into_chunks(text, max_words=chunk_words)
    partial_summaries = []

    for i, chunk in enumerate(chunks):
        try:
            print(f"📄 Summarizing chunk {i + 1}/{len(chunks)}...")
            summary = summarizer_func(chunk)
            partial_summaries.append(summary)
        except Exception as e:
            partial_summaries.append(f"❌ Failed to summarize chunk {i + 1}: {e}")

    combined_summary = "\n".join(partial_summaries)

    if question:
        return summarizer_func(f"{combined_summary}\n\nNow answer this question based on the above: {question}")
    else:
        return summarizer_func(
            f"Summarize the following partial summaries into a final comprehensive summary:\n\n{combined_summary}"
        )
