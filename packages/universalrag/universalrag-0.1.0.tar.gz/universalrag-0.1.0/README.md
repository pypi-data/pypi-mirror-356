# 📦 UniversalRAG

**UniversalRAG** is a plug-and-play, multimodal Retrieval-Augmented Generation (RAG) framework that lets you query data from ** PDFs, Videos, Images, Audio, Documents**, and more using powerful LLMs like **OpenAI**, **Groq**, **HuggingFace**.




## Why UniversalRAG?

UniversalRAG is designed to simplify the entire Retrieval-Augmented Generation (RAG) pipeline for developers.

- ❌ No need to write separate code for different document types
- ❌ No manual chunking, vectorizing, or retrieval code
- ❌ No need to understand the low-level details of embeddings or vector DBs

Just pass in:
- a PDF, YouTube video, audio file, or website URL
- ask your question
- get an accurate answer backed by retrieval

UniversalRAG saves developers hours of boilerplate work and enables them to focus on building real-world GenAI apps faster.

It’s your one-stop solution for multimodal RAG.

---

## 🚀 Features

- ✅ Supports 6+ input formats: PDF, DOCX, Image, Audio, Video
- ✅ Embedding-based retrieval system
- ✅ Built-in support for 3 types of models:
  - `groq` (LLaMA 3.1 8B Instant)
  - `huggingface` (HuggingFaceH4/zephyr-7b-beta)
  - `openai` (GPT-3.5 Turbo)
- ✅ Clean interface: Just import and ask!
- ✅ Easily extendable
- ✅ Supports `.env`-based API key management

---

## 📦 Installation

```bash
pip install universalrag


🔐 Setup API Keys

Create a .env file in your project root and add the keys as per the model(s) you’re using:
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token


⸻

🧪 Example Usage

⚠️NOTE:Load the any of the pdf,url,video,audio,doc,image at the place where you are running this input file
⚠️NOTE:copy the path of the specific (pdf,url,video,audio,doc,image) as well in the {input_path}
⚠️NOTE:The User gets to Choose which model he/she wants to communicate with.
⚠️NOTE:{groq,openai,huggingface,}-inputs for the variable {model_name}

#CODE:
🗂️ Input file (choose one)
from universalrag.pipeline import RAGPipeline
input_path = r"anything.pdf"         # PDF                   
# input_path = "lecture.mp4"         # 🎥 Video
# input_path = "https://example.com" # 🌐 URL
# input_path = "meeting.wav"         # 🎧 Audio
# input_path = "notes.docx"          # 📃 Word Doc
# input_path = "image.jpg"           # 🖼️ Image
# 🤖 Initialize pipeline with desired model
rag = RAGPipeline(input_path, model_name="groq")  
# ❓ Ask a question
question = "Summarize the content."
answer = rag.ask(question)
print("\n🤖 Answer:")
print(answer)


⚠️ Notes
	•	You must install model dependencies (e.g., openai, groq, transformers, langchain) as per your use case.
	•	You need API keys for Groq, OpenAI, or Hugging Face models.
	•	Some formats (e.g. audio/video) require ffmpeg to be installed.



📃 License

MIT License © 2025 Vigyat Singh

⸻

❤️ Contribute

Feel free to open issues, suggest improvements, or create pull requests!

⸻

🌐 Contact

For queries or collaborations, reach out to:
	•	GitHub: @vigyat13
	•	Email: vigyatsingh@2004.com