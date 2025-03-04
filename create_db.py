"""
The purpose of this script is to create a vector database.
Once the JSON file containing the various chunks is generated, these chunks are first converted
into embeddings using the 'efederici/sentence-bert-base' model, which supports Italian.
Finally, the embeddings are stored in a persistent database called 'vector-database'
using Chroma DB.

Author:
Roberto Parodo, email: r.parodo2@studenti.unica.it
"""
from langchain_core.documents.base import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import json

embeddings = HuggingFaceEmbeddings(model_name="efederici/sentence-bert-base")


class CreateDB(object):
    def __init__(self, file_json: str, name_directory: str):
        self.file_json, self.name_directory = file_json, name_directory
        self.dataset = self.load()
        self.create_database()

    def load(self):
        with open(self.file_json, 'r') as f:
            dataset = json.load(f)
        final_dataset = {}
        for key, item in dataset.items():
            aus = []
            for chunk in item:
                page = Document("")
                page.page_content = chunk[0]
                page.metadata = chunk[1]
                aus.append(page)
            final_dataset[key] = aus
        data = []
        for pdf_name, docs in final_dataset.items():
            data.extend(docs)
        return data

    def create_database(self):
        db = Chroma.from_documents(self.dataset, embeddings, persist_directory=self.name_directory)
        db.persist()


if __name__ == '__main__':
    datab = CreateDB('dataset.json', 'vec_database')