import streamlit as st
import time
import yt_dlp
import tempfile
import os
import pdf_summarizer

def all_in_one(model, transcriber):

    st.text("Provide the file to get transcript and Audio summary of your lecture")

    uploaded_file = st.file_uploader("Choose a video/audio file")
    st.markdown("""<h3 style="text-align: center;">OR</h3>""", 
                unsafe_allow_html=True)
    
    st_uploaded_link = st.text_input("Paste the video/audio link")
    
    transcribe_now = st.button("Start Transcribing...")

    if transcribe_now:
        if uploaded_file:
            transribe(uploaded_file, model=model, transcriber=transcriber)
        else:
            try:
                download_audio(st_uploaded_link)
                transribe("audio.mp3", model=model, transcriber=transcriber)
            except yt_dlp.utils.DownloadError:
                    st.info("ℹ️ Please provide a valid link or check the video availability.")

    st.markdown("""<h3 style="text-align: center;">OR</h3>""", 
                unsafe_allow_html=True)

    # pdf summary
    uploaded_pdf_file = st.file_uploader("Choose a PDF file", type=['pdf'])

    if uploaded_pdf_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_pdf_file.getvalue())
            temp_filepath = os.path.abspath(temp_file.name)
        
        result = pdf_summarizer.summarize_pdf(model=model, file_name=temp_filepath)
        st.session_state.saved_summary = result.content
        st.title("Summary ℹ️")
        st.markdown(st.session_state.saved_summary)
                        
def transribe(data, model, transcriber):
    st.write("File Uploaded Successfully!")
    
    st.title("Transcript 📜")
    progress_text = "Your request is in progress. Please wait."

    my_bar = st.progress(10, text=progress_text)
    transcript = transcriber.transcribe(data)
    st.session_state.saved_transcript = transcript.text

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    
    my_bar.empty()
    
    st.write(st.session_state.saved_transcript)

    # Save transcript in the system
    with open("transcript.txt", 'w') as file:
        file.write(st.session_state.saved_transcript)

    result = model.invoke("Summarize the  topic" + st.session_state.saved_transcript)
    st.session_state.saved_summary = result.content

    with open("summary.txt", 'w') as summary_file:
        summary_file.write(st.session_state.saved_summary)

    st.title("Summary ℹ️")

    st.write(st.session_state.saved_summary)

def download_audio(uploaded_link, output_filename="audio"):
                ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_filename,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]}
                with st.spinner("Wait for file the to download...", show_time=True):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(uploaded_link, download=True)
                        return output_filename
                    