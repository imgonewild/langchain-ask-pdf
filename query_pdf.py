from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import json, time

load_dotenv()
embeddings = OpenAIEmbeddings()
load_faiss = FAISS.load_local('./index/CLEANER, BLEACH CLOROX BLEACH SDS.pdf', embeddings)

# arr_question = []
cnt = 1
output = ''

for line in open('./prompt_db.jsonl', 'r'):
    # arr_question.append(json.loads(line))
    question = json.loads(line)
    query = question['prompt']
    print(f"{cnt} Question: {query}")    
    cnt += 1
    output += f"Question: {query}\n"

    ask_start_time = time.time()
    # answer = query_engine.query(f"You are a safety expert and {query}")
    docs = load_faiss.similarity_search(query)
    llm = OpenAI()
    chain = load_qa_chain(llm, chain_type="stuff")
    
    with get_openai_callback() as cb:
        response = chain.run(input_documents=docs, question=query)
        output += response

    # print("response", response)
    # print("\n--- %s seconds to query:---" % round(time.time() - ask_start_time, 2))
    print(f"Answer({round(time.time() - ask_start_time, 2)}s): {response}")
    print("----------------------------------------------------------")

    output+= f"Answer({round(time.time() - ask_start_time, 2)}s): {response}\n"
    output+= "----------------------------------------------------------\n" 

with open(f'./output/CLEANER, BLEACH CLOROX BLEACH SDS.txt', 'w') as f:
  f.write(output)