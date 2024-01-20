from spire.doc import *
from spire.doc.common import *
import boto3
import os
from flask import Flask

# Create Flask app
app = Flask(__name__)


def convert_word_to_pdf(word_file_path, output_dir):
    # Create a Document object
    document = Document()

    # Load a Word DOCX file
    document.LoadFromFile(f"{word_file_path}")

    # Save the file to a PDF file
    pdf_output_path = os.path.join(output_dir, "WordToPdf.pdf")
    document.SaveToFile(pdf_output_path, FileFormat.PDF)
    document.Close()

    return pdf_output_path


def upload_to_s3(file_path, bucket_name, object_key):

    s3 = boto3.client('s3')

    # Upload the file
    with open(file_path, 'rb') as file:
        s3.upload_fileobj(file, bucket_name, object_key)


@app.route('/<string:filename>', methods=['POST'])
def download_to_s3(filename):
    s3 = boto3.client('s3')

    bucket_name = "basu-doc-uploads"
    filename = filename + ".docx"

    file_path = f"C:/Users/KIIT/PycharmProjects/pythonProject/inputs/{filename}"
    # Download the file
    s3.download_file(bucket_name, filename, file_path)
    lambda_handler(filename)


def lambda_handler(name):
    download_path = f"C:/Users/KIIT/PycharmProjects/pythonProject/inputs/{name}"
    output_dir = f"C:/Users/KIIT/PycharmProjects/pythonProject/outputs"

    # Convert Word to PDF and get the PDF file path
    pdf_output_path = convert_word_to_pdf(download_path, output_dir)

    # S3 configuration
    bucket_name = 'basu-pdf-output'
    object_key = name.replace("docx", "pdf")  # Adjust the object key as needed

    # Upload the PDF file to S3
    upload_to_s3(pdf_output_path, bucket_name, object_key)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
