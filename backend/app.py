"""
REPORT-GEN Backend Application
Flask server for automated report generation
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import pandas as pd
from dotenv import load_dotenv
from utils import (
    parse_uploaded_file,
    detect_template,
    generate_report,
    export_to_pdf,
    export_to_txt,
    calculate_statistics
)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object('config.Config')

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)

# ========== ROUTES ==========

@app.route('/', methods=['GET'])
def index():
    """Serve the main application"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use CSV or Excel'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse file
        data, error = parse_uploaded_file(filepath)
        
        if error:
            return jsonify({'error': error}), 400
        
        # Get file info
        file_size = os.path.getsize(filepath) / 1024  # KB
        row_count = len(data)
        col_count = len(data[0].keys()) if data else 0
        columns = list(data[0].keys()) if data else []
        
        return jsonify({
            'success': True,
            'filename': filename,
            'size': f"{file_size:.2f} KB",
            'rows': row_count,
            'columns': col_count,
            'column_names': columns,
            'data': data[:10]  # Return first 10 rows for preview
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/detect-template', methods=['POST'])
def detect_template_route():
    """Detect appropriate template for data"""
    try:
        data = request.json
        columns = data.get('columns', [])
        report_type = data.get('report_type', '')
        
        template = detect_template(columns, report_type)
        
        return jsonify({
            'success': True,
            'template': template['name'],
            'confidence': template['confidence'],
            'all_templates': template['all_matches']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-report', methods=['POST'])
def generate_report_route():
    """Generate professional report"""
    try:
        data = request.json
        filename = data.get('filename')
        report_title = data.get('report_title')
        report_type = data.get('report_type')
        template = data.get('template')
        
        # Load data from uploaded file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_data, error = parse_uploaded_file(filepath)
        
        if error:
            return jsonify({'error': error}), 400
        
        # Generate report
        report_content = generate_report(
            report_title=report_title,
            report_type=report_type,
            template=template,
            data=file_data
        )
        
        return jsonify({
            'success': True,
            'report': report_content
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-pdf', methods=['POST'])
def export_pdf_route():
    """Export report as PDF"""
    try:
        data = request.json
        report_content = data.get('report')
        filename = data.get('filename', 'Report')
        
        # Generate PDF
        pdf_path = export_to_pdf(report_content, filename)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"{filename}.pdf"
        ), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-txt', methods=['POST'])
def export_txt_route():
    """Export report as TXT"""
    try:
        data = request.json
        report_content = data.get('report')
        filename = data.get('filename', 'Report')
        
        # Generate TXT
        txt_path = export_to_txt(report_content, filename)
        
        return send_file(
            txt_path,
            as_attachment=True,
            download_name=f"{filename}.txt"
        ), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0'
    }), 200

# ========== HELPER FUNCTIONS ==========

def allowed_file(filename):
    """Check if file type is allowed"""
    allowed_extensions = app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

# ========== MAIN ==========

if __name__ == '__main__':
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )