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

def ask_pdf(val, knowledge_base):
    question = val  
    if len(question) != 0:        
        docs = knowledge_base.similarity_search(question)
        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
            res = chain.run(input_documents=docs, question=question)
            # print(f"Total Tokens: {cb.total_tokens}")
            # print(f"Prompt Tokens: {cb.prompt_tokens}")
            # print(f"Completion Tokens: {cb.completion_tokens}")
            # print(f"Total Cost (USD): ${cb.total_cost}")

        res = res.replace('.', ".\n\n")
        return res