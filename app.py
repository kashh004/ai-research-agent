from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime
from config import settings
from agents.orchestrator import Orchestrator

app = Flask(__name__)
CORS(app)

# Initialize orchestrator
orch = Orchestrator(settings.chroma_dir, settings.embedding_model)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_papers():
    try:
        data = request.get_json()
        query = data.get('query', '')
        max_results = data.get('max_results', 10)
        since = data.get('since', None)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Run the orchestrator
        results = orch.run(query, max_results, since)
        
        # Format results for web display
        formatted_results = []
        for r in results:
            if 'error' in r:
                formatted_results.append({
                    'title': r['title'],
                    'error': r['error'],
                    'has_error': True
                })
            else:
                formatted_results.append({
                    'title': r['title'],
                    'authors': r['authors'],
                    'published': r['published'],
                    'summary': r['summary'],
                    'review': r['review'],
                    'ideas': r['ideas'],
                    'pdf_path': r['pdf_path'],
                    'gemini_enhanced': r.get('gemini_enhanced', False),
                    'has_error': False
                })
        
        return jsonify({
            'results': formatted_results,
            'query': query,
            'total_papers': len(formatted_results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<path:filename>')
def download_pdf(filename):
    """Serve PDF files from the data/pdfs directory"""
    try:
        return send_from_directory(settings.pdf_dir, filename)
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('reports', exist_ok=True)
    os.makedirs(settings.pdf_dir, exist_ok=True)
    os.makedirs(settings.chroma_dir, exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=8080)
