import PyPDF2
import json
import os

def analyze_pdf(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        reader = PyPDF2.PdfReader(file)
        
        # Get number of pages
        num_pages = len(reader.pages)
        
        # Extract text and analyze structure
        content = []
        for i in range(num_pages):
            page = reader.pages[i]
            # Convert Decimal to float for JSON serialization
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            
            content.append({
                'page': i + 1,
                'text': page.extract_text(),
                'size': {'width': width, 'height': height}
            })
        
        return {
            'num_pages': num_pages,
            'content': content,
            'filename': os.path.basename(pdf_path)
        }

if __name__ == '__main__':
    # Use the most recently uploaded PDF
    uploads_dir = 'uploads'
    pdf_files = [(f, os.path.getmtime(os.path.join(uploads_dir, f))) 
                 for f in os.listdir(uploads_dir) if f.endswith('.pdf')]
    latest_pdf = max(pdf_files, key=lambda x: x[1])[0]
    pdf_path = os.path.join(uploads_dir, latest_pdf)
    
    print(f"Analyzing {latest_pdf}...")
    result = analyze_pdf(pdf_path)
    
    # Save analysis to a JSON file
    with open('analysis.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    
    print(f"Analyzed {result['num_pages']} pages from {result['filename']}")
    print("Analysis saved to analysis.json")
