from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import glob, os, time
from time import strftime

t = strftime("%H:%M:%S %m-%d", time.localtime())
load_dotenv()
embeddings = OpenAIEmbeddings()

def load_sds():
    index_folder = "./index/"
    folders = glob.glob(f"{index_folder}*")
    #remove ./index/ from begin
    folders = [folder[len(index_folder):] for folder in folders]    
    option = st.selectbox(f"Select SDS ({len(folders)})", folders, key="123")
    return index_folder,option

def ask_sds(knowledge_base, index_question):
    if len(index_question) != 0:
          docs = knowledge_base.similarity_search(index_question)
          llm = OpenAI()
          chain = load_qa_chain(llm, chain_type="stuff")
          with get_openai_callback() as cb:
            response = chain.run(input_documents=docs, question=index_question)
            # print("cb", cb)

          st.write(response)
          print("response:", response)

def upload_sds_n_save(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
      text += page.extract_text()

    # split into chunks
    text_splitter = CharacterTextSplitter(
      separator="\n",
      chunk_size=1000,
      chunk_overlap=200,
      length_function=len
    )
    chunks = text_splitter.split_text(text)
          
    filename = pdf.name
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    knowledge_base.save_local(f'./index/{filename}')
    st.write(f'File {filename} upload successed!')
    # refresh page
    st.experimental_rerun()

def main():
    print(f"--------------------{t}-----------------------------")    
    st.set_page_config(page_title="Inteplast SDS System")
    st.header("Ask your SDS")
    
    # load sds
    index_folder,option = load_sds()

    # load .faiss & .pkl
    knowledge_base = FAISS.load_local(f"{index_folder}{option}", embeddings)
    filename = os.path.basename(option)

    index_question = st.text_input(f"Ask a question about {filename}")
    print("index_question:", index_question)

    # ask sds
    ask_sds(knowledge_base, index_question)

    # upload sds

    with st.form("my-form", clear_on_submit=True):
        pdf = st.file_uploader("Upload your SDS", type="pdf")
        submitted = st.form_submit_button("Upload")
        # print(submitted, pdf)
        if submitted and pdf is not None:
            upload_sds_n_save(pdf)  
            
if __name__ == '__main__':
    main()
