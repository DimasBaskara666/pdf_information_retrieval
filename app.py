# app.py
from flask import Flask, request, render_template, send_file
from utils import preprocess, search_query, extract_relevant_text
import os

app = Flask(__name__)

# Directory where PDFs are stored
PDF_DIRECTORY = os.path.join(os.path.dirname(__file__), 'database')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = search_query(query, PDF_DIRECTORY)
    enhanced_results = [
        {
            "filename": filename,
            "similarity": similarity,
            "description": extract_relevant_text(query, os.path.join(PDF_DIRECTORY, filename))
        }
        for filename, similarity in results
    ]
    return render_template('results.html', query=query, results=enhanced_results)

@app.route('/view/<filename>')
def view_pdf(filename):
    file_path = os.path.join(PDF_DIRECTORY, filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return "File not found", 404

@app.route('/download/<filename>')
def download_pdf(filename):
    file_path = os.path.join(PDF_DIRECTORY, filename)
    if os.path.exists(file_path):
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
