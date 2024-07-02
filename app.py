from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from google.cloud import storage
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure your bucket name and project ID
BUCKET_NAME = 'xmpl-bkt'
PROJECT_ID = 'enduring-broker-426815-b2'

# Initialize Google Cloud Storage client
storage_client = storage.Client(project=PROJECT_ID)
bucket = storage_client.bucket(BUCKET_NAME)

@app.route('/')
def index():
    blobs = bucket.list_blobs()
    images = [blob.name for blob in blobs if blob.name.endswith('.png')]
    return render_template('index.html', images=images, bucket_name=BUCKET_NAME)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.png'):
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        return redirect(url_for('index'))

@app.route('/view/<filename>')
def view_file(filename):
    # Generate public URL for the image file
    url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"
    return render_template('view.html', filename=filename, url=url)

@app.route('/download/<filename>')
def download_file(filename):
    # Serve the file directly from the bucket
    return redirect(f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
