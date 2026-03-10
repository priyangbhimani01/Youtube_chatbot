# 🎥 YouTube Video Chatbot

A **Streamlit-based AI chatbot** that lets you chat with the content of any **YouTube video**. It extracts the video transcript, processes it using **LangChain**, stores embeddings in a **FAISS vector database**, and uses an **LLM** to answer questions based on the video content.

---

## 🚀 Features

- 🎬 Enter any *YouTube video URL*
- 📺 Preview the video inside the app
- 🧠 Automatically extracts YouTube transcripts
- 🔍 Uses vector embeddings to understand video content
- 💬 Ask questions about the video
- ⚡ Built with **Streamlit + LangChain**
- 🤖 Supports multiple LLM providers:
  - Groq
  - HuggingFace

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Framework:** LangChain  
- **Embeddings:** HuggingFace Embeddings  
- **Vector Database:** FAISS  
- **LLMs:** Google Generative AI, Groq, HuggingFace  
- **Document Loader:** YoutubeLoader  

## ⚙️ Setup & Installation

git clone https://github.com/your-username/youtube-chatbot.git

pip install -r requirements.txt

GOOGLE_API_KEY=your_google_api_key

GROQ_API_KEY=your_groq_api_key
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token

streamlit run app.py

