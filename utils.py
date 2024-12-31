import os
import PyPDF2
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess(pdf_directory):
    documents = []
    filenames = []
    
    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            with open(os.path.join(pdf_directory, filename), 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text()
                documents.append(text)
                filenames.append(filename)
    
    return documents, filenames

def search_query(query, pdf_directory):
    documents, filenames = preprocess(pdf_directory)
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(documents)
    
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, vectors).flatten()
    
    results = sorted(
        zip(filenames, similarities),
        key=lambda x: x[1],
        reverse=True
    )
    
    return [result for result in results if result[1] > 0]  # Return non-zero matches
def extract_relevant_text(query, file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    sentences = text.split('.')
    relevant_sentences = [sentence for sentence in sentences if query.lower() in sentence.lower()]
    return ' '.join(relevant_sentences[:3])  # Mengambil hingga 3 kalimat pertama yang relevan
