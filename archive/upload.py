import tkinter as tk #import model A as alias B
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os, sys, time
start_time = time.time()

load_dotenv()
file= sys.argv[1]
# C:/Users/Alan/AppData/Local/Programs/Python/Python311/python.exe "d:/Github_Repo/streamlit-langchain-ask-pdf/upload.py" "D:\Github Repo\streamlit-langchain-ask-pdf\pdf\Adhesive, 3M Spray Adhesive 90 SDS.pdf"
def upload_file():
    # contents = ''
    # with open('C:\path_setting\\vector_path.txt') as f:
    #     contents = f.readlines()
    # f.close()
    # vector_folder = contents[0]

    vector_folder = os.getenv('VECTOR_PATH')

    label = tk.Label(text = file)    
    label.pack()

    pdf_reader = PdfReader(file)
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

    filename = os.path.basename(file)
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    knowledge_base.save_local(f'{vector_folder}\{filename}')
    print("--- %s seconds ---" % (time.time() - start_time))

upload_file()

# root = tk.Tk()
# root.title('Inteplast SDS Tool')
# root.resizable(False, False)
# root.geometry('600x300')

# tk.Button(
#     root,
#     text = "Ask",
#     command= lambda: upload_file()                
# ).pack(pady= 10)

# root.mainloop()