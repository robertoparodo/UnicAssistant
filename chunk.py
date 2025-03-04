"""
The purpose of this script is to divide the regulations contained in the PDFs into chunks
and perform pre-processing, specifically removing summaries that could interfere with
finding relevant chunks.
The script segments the text so that each chunk begins with a new article.
If the chunks are too long, they are further divided using the RecursiveChunkSplitter.
After these operations are completed, all chunks are saved in a JSON file.

Author:
Roberto Parodo, email: r.parodo2@studenti.unica.it
"""
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents.base import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import re
import json


def find_pdfs(base_dir):
    pdf_files = []
    for root, dirs, files in os.walk(base_dir):
        for pdf_file in files:
            if pdf_file.endswith('.pdf'):
                full_path = os.path.join(root, pdf_file)
                pdf_files.append(full_path.replace("\\", "/"))
    return pdf_files


def load_pdf(paths: list) -> dict:
    dataset = {}
    for path in paths:
        pages_document = []
        loader = PyPDFLoader(path)
        pages_document.extend(loader.load())
        dataset[path] = pages_document
    return dataset


def extract_text_from_pdf_with_pages(pdf_list: list) -> str:
    total_text = ""
    for text in pdf_list:
        total_text += text.page_content
    return total_text


def split_articles(text) -> list:
    regex = r'(Art\.\s*\d+\s+.*?\n)(?=\s*Art\.|\Z)'
    matches = re.findall(regex, text, re.DOTALL)
    return matches


def delete_summary(pages: list, key_word: str) -> list:
    pattern = re.compile(r'\b' + re.escape(key_word) + r'\s*\.?\s*1\b', re.IGNORECASE)
    occurrence = 0
    for index, page in enumerate(pages):
        if pattern.search(page):
            occurrence += 1
            if occurrence == 2:
                return pages[index:]
    return delete_summary2(pages, key_word)


def delete_summary2(pages: list, key_word: str) -> list:
    pattern = re.compile(r'\b' + re.escape(key_word) + r'\s*\.?\s*2\b', re.IGNORECASE)
    occurrence = 0
    for index, page in enumerate(pages):
        if pattern.search(page):
            occurrence += 1
            if occurrence == 2:
                return pages[index:]
    return pages


def create_chunks(arts, source) -> list:
    chunks = []
    for art in arts:
        portion_pdf = Document("")
        portion_pdf.page_content = art
        portion_pdf.metadata['source'] = source
        portion_pdf.metadata['page'] = re.findall(r'\d+', art)[0]
        chunks.append(portion_pdf)
    return chunks


def save_json(documents):
    aus = {}
    for term, content_pdf in documents.items():
        content = []
        for portion in content_pdf:
            content.append([portion.page_content, portion.metadata])
        aus[term] = content
    with open('dataset.json', 'w') as f:
        json.dump(aus, f, indent=4)


if __name__ == '__main__':

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    path_pdf = find_pdfs('dataset')
    all_rules = load_pdf(path_pdf)
    all_pdf = {}
    for metadata, file in all_rules.items():
        all_text = extract_text_from_pdf_with_pages(file)
        articles = split_articles(all_text)
        articles = delete_summary(articles, "art")
        final_chunks = create_chunks(articles, metadata)
        final_chunks = text_splitter.split_documents(final_chunks)
        all_pdf[metadata] = final_chunks
    for key, pdf in all_pdf.items():
        for chunk in pdf:
            chunk.page_content = chunk.page_content.replace("\n", "")
    save_json(all_pdf)
