from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import json
from werkzeug.utils import secure_filename
import PyPDF2
import fitz  # PyMuPDF for image extraction
import glob

app = Flask(__name__, 
    static_url_path='',
    static_folder='static',
    template_folder='templates'
)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('static/extracted_images', exist_ok=True)

def extract_images_from_pdf(pdf_path, output_dir):
    doc = fitz.open(pdf_path)
    images = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Generate unique filename
            image_name = f'page{page_num + 1}_img{img_index + 1}.{image_ext}'
            image_path = os.path.join(output_dir, image_name)
            
            # Save image
            with open(image_path, 'wb') as img_file:
                img_file.write(image_bytes)
            images.append(f'/static/extracted_images/{image_name}')
    
    return images

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

def clear_uploads():
    files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
    for f in files:
        try:
            os.remove(f)
            print(f"Removed: {f}")
        except Exception as e:
            print(f"Error removing {f}: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return 'No file uploaded', 400
        
        file = request.files['file']
        
        # If user submits without selecting a file
        if file.filename == '':
            return 'No file selected', 400
        
        if file and allowed_file(file.filename):
            # Clear old files
            clear_uploads()
            
            # Save new file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract text from PDF
            with open(filepath, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
            
            # Extract images from PDF
            images = extract_images_from_pdf(filepath, 'static/extracted_images')
            
            # Save extracted text and image paths as JSON
            json_filename = filename.rsplit('.', 1)[0] + '.json'
            json_filepath = os.path.join(app.config['UPLOAD_FOLDER'], json_filename)
            with open(json_filepath, 'w') as json_file:
                json.dump({
                    'text': text,
                    'images': images
                }, json_file)
            
            return redirect(url_for('preview', filename=filename))
    
    return render_template('upload.html')

@app.route('/preview/<filename>')
def preview(filename):
    json_filename = filename.rsplit('.', 1)[0] + '.json'
    json_filepath = os.path.join(app.config['UPLOAD_FOLDER'], json_filename)
    
    with open(json_filepath, 'r') as json_file:
        data = json.load(json_file)
    
    return render_template('preview.html', filename=filename, text=data['text'], images=data['images'])

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
