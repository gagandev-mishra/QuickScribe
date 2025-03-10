from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import streamlit as st

def chat_features(model):

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input        
    if prompt := st.chat_input("Ask anything about the recording"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):  
            # Chat Template
            chat_template = ChatPromptTemplate([
                ('system', 'You are a verfy helpful in explaining concepts'),
                MessagesPlaceholder(variable_name='chat_history'),
                ('human', '{query}')
            ])

            # Load Transcript
            chat_history = []
            with open("transcript.txt") as file:
                chat_history.extend(file.readlines())

            # Create Prompt
            prompt = chat_template.invoke({'chat_history': chat_history, 'query': prompt})
            send_message = model.invoke(prompt)
            st.session_state.messages.append({'role': 'assistant', "content": send_message.content})
            st.markdown(send_message.content)

