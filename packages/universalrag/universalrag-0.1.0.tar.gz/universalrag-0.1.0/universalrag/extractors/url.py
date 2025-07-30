import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()

        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines()]
        cleaned_text = "\n".join([line for line in lines if line])

        if not cleaned_text.strip():
            print("⚠️ No meaningful text extracted from URL.")
        else:
            print(f"✅ Extracted {len(cleaned_text.split())} words from URL.")

        return cleaned_text

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch URL content: {e}")
        return ""
