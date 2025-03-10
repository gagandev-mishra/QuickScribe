from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def summarize_pdf(model, file_name):
    loader = PyPDFLoader(file_name)
    pages = [page.page_content for page in loader.load_and_split()]  
    chat_template = ChatPromptTemplate([
        ('system', "You're best in reading pdf file, "
                    "and making the key notes from the uploaded file"
                    "try to give response such a person don't feel overwhelm, also not go unsatisfied"
                    "Also don't ask user for further query"
                    "Just end the summary with proper close-up"),
        ('human', '{pages}')
    ])

    prompt = chat_template.invoke(pages)

    return model.invoke(prompt)
