import tkinter as tk #import model A as alias B
from tkinter import *
from tkinter import ttk
from tkinter.commondialog import Dialog
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv
import os, sys

try:
    file = sys.argv[1]
except:
    # file = "Adhesive, 3M Spray Adhesive 90 SDS.pdf"
    file = "BioRem-2000-Surface-Cleaner MSDS.pdf"
root = tk.Tk()
root.resizable(True, True)
root.title(file)

ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
w = 367/1600*ws # width for the Tk root

h = hs # height for the Tk root
x = ws-w #(ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

load_dotenv()
vector_folder = os.getenv('VECTOR_PATH')
embeddings = OpenAIEmbeddings()
knowledge_base = FAISS.load_local(f"{vector_folder}\{file}", embeddings)

def ask(val):
    question = val  
    if len(question) != 0:        
        docs = knowledge_base.similarity_search(question)
        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
            res = chain.run(input_documents=docs, question=question)
            # response = chain.predict(input=question)
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")

        res = res.replace('.', ".\n\n")
        txt_ans.delete("1.0",END)   
        txt_ans.insert(tk.END, res)

def show_hand_cursor(a):
    txt_ans.config(cursor="watch")

txt_question = Text(root, height=4, font= ('Aerial 17'))
txt_question.insert(tk.END, "What is the waste procedure?")
txt_question.pack(padx=10, pady=10)
txt_question.bind('<Return>', lambda event: ask(txt_question.get("1.0",END)))

ttk.Button(
    root,
    text = "Ask", 
    command = lambda: ask(txt_question.get("1.0",END))                        
).pack(pady= 10)

txt_ans = Text(root, height=hs, font= ('Aerial 17'))
txt_ans.pack(padx=10, pady=10, fill='both')

root.mainloop()