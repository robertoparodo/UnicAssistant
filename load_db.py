"""
Script to load the entire database.

Author:
Roberto Parodo, email: r.parodo2@studenti.unica.it
"""
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="efederici/sentence-bert-base")


class VectorizedDb(object):
    def __init__(self):
        self.db = Chroma(persist_directory="vec_database", embedding_function=embeddings)

    def get_db(self):
        return self.db
