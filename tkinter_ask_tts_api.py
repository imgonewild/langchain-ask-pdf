from tkinter import *
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv
from googletrans import Translator

def ask_pdf(val, knowledge_base, language):
    print(language)
    question =  val + f' and please reply as {language}.'

    if len(question) != 0:        
        docs = knowledge_base.similarity_search(question)
        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
            res = chain.run(input_documents=docs, question=question)
        res = res.replace('.', ".\n")

    return res
    # return translate(res, language)

def translate(text, language):
    translator = Translator()
    translation = translator.translate(text, src='en', dest=language)
    print(language, translation.text)
    return translation.text