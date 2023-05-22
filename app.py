import os
from io import BytesIO
import streamlit as st
import openai
from apikey import api_key
from apikey import file_name
from pdf_reader import parse_pdf, text_to_docs, docs_to_index
from utils import Chat

#Function to build index of a pdf file
file_path = file_name
@st.cache_data
def get_index_for_pdf(file_name, openai_api_key):
    with open(file_path, 'rb') as file:
        file_bytes = file.read()
    pdf_file = BytesIO(file_bytes)
    text = parse_pdf(pdf_file)  # Extract text from the pdf
    documents = text_to_docs(text)  # Divide the text up into chunks
    index = docs_to_index(documents, openai_api_key)

    return index

os.environ['OPEAI_AI_KEY'] = api_key
openai.api_key = os.environ['OPEAI_AI_KEY']

# This is where we set the personality and style of our chatbot
prompt_template = """You are an assistant that draw knowledge across some given text 
        and all the other things you already know.

        The provided text is the following:
        {document_data}
    """

# Create a search index (using OpenAI embeddings) for the PDF file
index = get_index_for_pdf(file_name, openai.api_key)

#Start StreamLit
st.title("Chatbot with India 2023-2024 budget speech")
form = st.form("Input box", clear_on_submit=True)
question = form.text_input("Send message", placeholder="What was NIRMALA SITHARAMAN talking about?")
submit_button = form.form_submit_button("Send")

#Get convo history
prompt = st.session_state.get("prompt", None)
if prompt is None:
    # This is the format OpenAI expects
    prompt = [{"role": "system", "content": prompt_template}]

chat = Chat(prompt)

if question:  # Someone have asked a question
    # Search the PDF for relevant text and take the top result
    docs = index.similarity_search(question)
    doc = docs[0].page_content

    # Insert the text into the instructions
    prompt_template = prompt_template.format(document_data=doc)
    prompt[0] = {"role": "system", "content": prompt_template}

     # Add the question the user question
    prompt.append({"role": "user", "content": question})

    # Display the question in the app
    chat.update_question(question)
    response = []
    result = ""

    # Ask the question and stream the response
    for chunk in openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=prompt, stream=True
    ):
        text = chunk.choices[0].get("delta", {}).get("content")
        if text is not None:
            response.append(text)
            result = "".join(response).strip()
            chat.update_answer(result)

    # When we get an answer back we add that to the message history
    prompt.append({"role": "assistant", "content": result})

    # Finally, we store it in the session state
    st.session_state["prompt"] = prompt
