from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import glob, os, time
from time import strftime
import subprocess
from tempfile import NamedTemporaryFile
import shutil

t = strftime("%H:%M:%S %m-%d", time.localtime())
load_dotenv()
embeddings = OpenAIEmbeddings()
index_folder = "./index/"
pdf_folder = "./pdf/"

def load_sds():    
    folders = glob.glob(f"{index_folder}*")
    #remove ./index/ from begin
    folders = [folder[len(index_folder):] for folder in folders]    
    option = st.selectbox(f"Select SDS ({len(folders)})", folders, key="123")

    if option!= None and st.button('Open SDS file'):
        subprocess.Popen([f"{pdf_folder}{option}"],shell=True)

    return index_folder,option

def ask_sds(knowledge_base, index_question):
    if len(index_question) != 0:
          
        # chat_history = []
        docs = knowledge_base.similarity_search(index_question)
        llm = OpenAI()
        #please use the format to answer question: {"question": question, "answer": answer}
        # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        # chain = load_qa_chain(llm, chain_type="stuff", memory=memory)
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
          response = chain.run(input_documents=docs, question=index_question)
          # print("cb", cb)

        st.write(response)
        print("response:", response)

def upload_sds_n_save(pdfs):
    # print(len(pdfs))
    for pdf in pdfs:
      print("pdf.name:", pdf.name)
      pdf_reader = PdfReader(pdf)
      temp_pdf = ''
      with NamedTemporaryFile(dir='.', suffix='.pdf', delete=False) as f:
          f.write(pdf.getbuffer())
          temp_pdf = f.name
      shutil.move(temp_pdf, pdf_folder + pdf.name)

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
      knowledge_base.save_local(f'{index_folder}{filename}')
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
    if(option != None):
      knowledge_base = FAISS.load_local(f"{index_folder}{option}", embeddings)
      filename = os.path.basename(option)

      index_question = st.text_input(f"Ask a question about {filename}")
      print("index_question:", index_question)

      # ask sds
      ask_sds(knowledge_base, index_question)
      
    # upload sds
    with st.form("my-form", clear_on_submit=True):
        pdf = st.file_uploader("Upload your SDS", type="pdf", accept_multiple_files=True)
        submitted = st.form_submit_button("Upload")
        # print(submitted, pdf)
        if submitted and pdf is not None:
            upload_sds_n_save(pdf)  
            
if __name__ == '__main__':    
    if not os.path.exists(index_folder):
      os.makedirs(index_folder)

    if not os.path.exists(pdf_folder):
      os.makedirs(pdf_folder)

    main()
