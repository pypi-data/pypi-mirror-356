from universalrag.pipeline import RAGPipeline

# 🔧 Example input: PDF file, image, audio, video, docx, or URL                                 GROQ    
#input_path =r"C:\Users\KIIT\Desktop\minirag\examples\CV - Vigyat Singh (8) 2 - Copy (2).pdf"                # 📄 Local PDF
#input_path = r"C:\Users\KIIT\Desktop\minirag\examples\video1.mp4"            # 🎥 Local Video   working
#input_path = r"https://www.sjsu.edu/writingcenter/docs/handouts/Introduction%20of%20Research%20Papers.pdf"    # 🌐 URL                     notworking
#input_path = r"C:\Users\KIIT\Desktop\minirag\examples\WhatsApp Image 2025-06-20 at 2.29.12 AM.jpeg"#working   # 🖼️ Image
input_path = r"C:\Users\KIIT\Desktop\minirag\examples\audio_lyI1GLHZntI.wav"            # 🎧 Audio working
# input_path = "notes.docx"             # 📃 Word doc                                            #working

# 🔍 Model options: "flan" (default), "openai", "groq", "huggingface"
# ❓ Ask a question
rag = RAGPipeline(input_path, model_name="huggingface")

# ❓ Ask a question
question = "summarize the content"

answer = rag.ask(question)

print("\n🤖 Answer:")
print(answer)