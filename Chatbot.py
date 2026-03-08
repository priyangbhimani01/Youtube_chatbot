from Chatbot_Project.Project import *
import streamlit as st
from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="YouTube Chatbot", page_icon="🎥", layout="wide")



if "page" not in st.session_state:
    st.session_state.page = "home"

if "messages" not in st.session_state:
    st.session_state.messages = None

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "docs" not in st.session_state:
    st.session_state.docs = None

if "check_url_home" not in st.session_state:
    st.session_state.check_url_home = None   

if "check_url_chat" not in st.session_state:
    st.session_state.check_url_chat = None     

def process_video(url):

    loader = YoutubeLoader.from_youtube_url(url)
    docs = loader.load()
    return docs

    

def midprocess_video(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    split_docs = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(split_docs, embeddings)

    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 3, "lambda_mult":0.5})

    return retriever


if st.session_state.page == "home":

    st.title("🎥 YouTube Video Chatbot")

    if "video_url" not in st.session_state:
        st.session_state.video_url = ""

    url = st.text_input("Enter YouTube URL", value=st.session_state.video_url)
    st.session_state.video_url = url

    if url:
        st.subheader("Video Preview")

        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.video(url)

    col1, col2, col3 = st.columns([2,1,2])

    with col2:
        if st.button("Proceed ➜"):

            if url:

                with st.spinner("Processing video transcript..."):
                    if st.session_state.check_url_home != st.session_state.video_url:
                        st.session_state.docs = process_video(url)
                        st.session_state.check_url_home=st.session_state.video_url
                        st.session_state.messages = [ {"role": "assistant", "content": "Hello! I am your AI assistant."} ]


                    else:
                        pass    
                st.session_state.page = "chat"
                st.rerun()

            else:
                st.warning("Please enter a YouTube URL")



if st.session_state.page == "chat":

    st.title("💬 Chat with the Video")

    col1, col2 = st.columns([3,1])

    if st.session_state.check_url_chat != st.session_state.video_url:
        st.session_state.retriever=midprocess_video(st.session_state.docs)
        st.session_state.check_url_chat=st.session_state.video_url

    else:
        pass    


    with col2:
        if st.button("Go Back", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    st.divider()

    user_input = st.chat_input("Ask a question about the video")

    if user_input:

        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )


        docs = st.session_state.retriever.invoke(user_input)

        context = "\n".join([doc.page_content for doc in docs])

        llm= ChatGroq(model="llama-3.1-8b-instant",temperature=0.7)

        prompt = f"""
        You are helpful AI assistant, Answer the question based only on the following context.

        Context:
        {context}

        Question:
        {user_input}
        """

        response = llm.invoke(prompt)

        ai_response = response.content

        st.session_state.messages.append(
            {"role": "assistant", "content": ai_response}
        )

    
    for msg in st.session_state.messages:

        if msg["role"] == "assistant":
            col1, col2,clo3 = st.columns([3,1,1])
            with col1:
                st.write(msg["content"])

        else:
            col1, col2, col3 = st.columns([3,1,2.3])
            with col3:
                st.write(msg["content"])