from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from google.cloud import storage
import os

# just in cas uploads folder is needed

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# make sure the upload folder exists

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# configured the bucket name: 'xmpl-bkt'
# project id can stay the same

BUCKET_NAME = 'xmpl-bkt'
PROJECT_ID = 'enduring-broker-426815-b2'

# initialize the storage client
# set the bucket to the storage client bucket

storage_client = storage.Client(project=PROJECT_ID)
bucket = storage_client.bucket(BUCKET_NAME)

# send the list of files to index.html
# make sure the file name ends with png
@app.route('/')
def index():

    blobs = bucket.list_blobs()
    images = [blob.name for blob in blobs if blob.name.endswith('.png')]
    return render_template('index.html', images=images, bucket_name=BUCKET_NAME)

@app.route('/upload', methods=['POST'])
def upload_file():

    # check if the file was in the request
    if 'file' not in request.files:

        return redirect(request.url)

    file = request.files['file']

    # check if the filename is empty
    if file.filename == '':

        return redirect(request.url)

    # in case of accepted file
    # upload the file
    # redirect back to index.html to see the updated files list
    
    if file and file.filename.endswith('.png'):

        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        return redirect(url_for('index'))

@app.route('/view/<filename>')
def view_file(filename):

    # generate public URL for the image file
    # can go to the bucket/filename
    # send to view.html

    url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"
    return render_template('view.html', filename=filename, url=url)

@app.route('/download/<filename>')
def download_file(filename):

    # file can be served directly from the bucket
    return redirect(f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}")

if __name__ == '__main__':

    # host the app on port 8080
    app.run(host='0.0.0.0', port=8080)
