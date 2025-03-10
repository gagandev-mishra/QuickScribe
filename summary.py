import assemblyai as aai
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st
import chat_with_model as chat
import all_in_one as overall
import os


load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

transcriber = aai.Transcriber()
model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        temperature=0,
        max_tokens=None,
        timeout=None)

st.sidebar.title("QuickScribe 📄")

selected_option = st.sidebar.selectbox("What you want to do?", ['All in One', 'Transcript', 'Summary', 'Chat with me!'])

# Initialize session state for saved_transcript
if "saved_transcript" not in st.session_state:
    st.session_state.saved_transcript = ""
    st.session_state.saved_summary = ""

if selected_option == "All in One":
    st.header(selected_option + "✅")
    overall_feture = overall.all_in_one(model=model, transcriber=transcriber)

elif selected_option == 'Transcript':
    st.header(selected_option + "📜")
    st.write(st.session_state.saved_transcript)

elif selected_option == 'Summary':
    st.header(selected_option + "ℹ️")
    st.write(st.session_state.saved_summary)

elif selected_option == 'Chat with me!':
    st.title("Want to speak with me 😀?")
    chat_feature = chat.chat_features(model=model)




