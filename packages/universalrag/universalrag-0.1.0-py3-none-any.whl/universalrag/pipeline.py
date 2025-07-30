import os
from universalrag.embedder import Embedder
from universalrag.retriever import Retriever
from universalrag.extractors.pdf import extract_text_from_pdf
from universalrag.extractors.docx import extract_text_from_docx
from universalrag.extractors.image import extract_text_from_image
from universalrag.extractors.audio import extract_text_from_audio
from universalrag.extractors.video import extract_text_from_video
from universalrag.extractors.url import extract_text_from_url
from universalrag.utility.summarizer import safe_summarize_large_text, summarize_with_api


class RAGPipeline:
    SUPPORTED_MODELS = ["openai", "groq", "huggingface"]

    def __init__(self, file_path_or_url, model_name=None):
        self.raw_input = file_path_or_url
        self.model_name = (model_name or "openai").lower()

        if self.model_name not in self.SUPPORTED_MODELS:
            raise ValueError(f"❌ Unsupported model: {self.model_name}. Choose from: {self.SUPPORTED_MODELS}")

        print(f"🚀 [UniversalRAG] Using model: {self.model_name}")
        print(f"📂 Loading from: {self.raw_input}")

        self.text = self._extract_text(self.raw_input)
        self.chunks = self._chunk_text(self.text)

        self.embedder = Embedder()
        self.vectors = self.embedder.embed_chunks(self.chunks)

        if self.vectors is None or getattr(self.vectors, "shape", [0])[0] == 0:
            raise ValueError("❌ No vectors found — cannot initialize Retriever.")

        self.retriever = Retriever(self.vectors, self.chunks)
        self.generate_answer = self._load_model(self.model_name)

    def _extract_text(self, path):
        if path.startswith("http"):
            return extract_text_from_url(path)
        elif path.endswith(".pdf"):
            return extract_text_from_pdf(path)
        elif path.endswith(".docx"):
            return extract_text_from_docx(path)
        elif path.endswith((".jpg", ".jpeg", ".png")):
            return extract_text_from_image(path)
        elif path.endswith((".mp4", ".mov")):
            return extract_text_from_video(path)
        elif path.endswith((".mp3", ".wav")):
            return extract_text_from_audio(path)
        else:
            raise ValueError("❌ Unsupported file or URL format.")

    def _chunk_text(self, text, chunk_size=500, overlap=50):
        words = text.split()
        return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size - overlap)]

    def _load_model(self, model_name):
        if model_name == "openai":
            from universalrag.models.openai_gen import generate_answer
        elif model_name == "groq":
            from universalrag.models.groq_gen import generate_answer
        elif model_name == "huggingface":
            from universalrag.models.hf_gen import generate_answer
        return generate_answer

    def _get_model_id(self):
        if self.model_name == "groq":
            return "llama-3.1-8b-instant"
        elif self.model_name == "openai":
            return "gpt-3.5-turbo"
        return ""

    def _get_api_key(self):
        if self.model_name == "groq":
            return os.getenv("GROQ_API_KEY")
        elif self.model_name == "openai":
            return os.getenv("OPENAI_API_KEY")
        return None

    def _get_api_url(self):
        if self.model_name == "groq":
            return "https://api.groq.com/openai/v1/chat/completions"
        elif self.model_name == "openai":
            return "https://api.openai.com/v1/chat/completions"
        return None

    def ask(self, question):
        query_vector = self.embedder.embed_query(question)
        top_chunks = self.retriever.get_top_chunks(query_vector, k=5)
        full_text = "\n".join(top_chunks)

        if len(full_text.split()) > 3000 and self.model_name in ["openai", "groq"]:
            return safe_summarize_large_text(
                lambda prompt: summarize_with_api(
                    prompt,
                    self._get_model_id(),
                    self._get_api_key(),
                    self._get_api_url()
                ),
                full_text,
                question=question
            )

        return self.generate_answer(question, top_chunks)
