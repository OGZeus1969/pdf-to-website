# PDF to Website Converter

A Flask web application that converts PDF designs into responsive websites.

## Features
- PDF file upload and analysis
- Automatic website generation
- Responsive design using Bootstrap
- Modern UI with animations
- Support for multiple pages

## Setup
1. Install Python 3.13 or later
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

## Deployment
This application is configured for deployment on Render.com:

1. Create a new account on Render.com
2. Connect your GitHub repository
3. Create a new Web Service
4. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

## Project Structure
- `app.py`: Main Flask application
- `pdf_analyzer.py`: PDF content analyzer
- `templates/`: HTML templates
- `uploads/`: PDF storage directory
