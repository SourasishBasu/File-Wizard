import img2pdf
import boto3
import os
from flask import Flask, jsonify

# Create Flask app
app = Flask(__name__)

# Use pandoc package with pypandoc to convert from .docx to .pdf
def convert_png_to_pdf(png_file_path, output_dir):

    a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
	layout_fun = img2pdf.get_layout_fun(a4inpt)

	with open(output_dir,"wb") as f:
		f.write(img2pdf.convert(png_file_path, layout_fun=layout_fun))

  print("File converted to PDF")

# Upload to S3
def upload_to_s3(file_path, bucket_name, object_key):
    try:
        s3 = boto3.client('s3')

        # Upload the file
        s3.upload_file(file_path, bucket_name, object_key)

    except Exception as e:
        # Return an error message
        return jsonify({'error': f'Error: {str(e)}'}), 500


# Exposing as API to receive POST request containing newly uploaded file name
@app.route('/<string:filename>', methods=['POST'])
def download_to_s3(filename):

    try:
        s3 = boto3.client('s3')

        bucket_name = "basu-doc-uploads"
        filename = filename + ".png"

        file_path = f"./inputs/{filename}"

        # Download the file
        s3.download_file(bucket_name, filename, file_path)

        # Call the lambda_handler function
        lambda_handler(filename)

        # Return a success message
        return jsonify({'message': 'File downloaded, converted and uploaded successfully'})

    except Exception as e:
        # Return an error message
        return jsonify({'error': f'Error: {str(e)}'}), 500  # HTTP status code 500 for internal server error

# Handles the converted file and calls the upload function to the output bucket
def lambda_handler(name):
    object_key = name.replace("png", "pdf")  # The object key is same as the original file name
    
    download_path = f"./inputs/{name}"
    output_dir = f"./outputs/{object_key}"
    
    # Convert Word to PDF
    convert_png_to_pdf(download_path, output_dir)

    # S3 bucket details
    bucket_name = 'basu-pdf-output'
    
    # Upload the PDF file to S3
    upload_to_s3(output_dir, bucket_name, object_key)


# App runs on localhost, listens for requests on port 5000
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
