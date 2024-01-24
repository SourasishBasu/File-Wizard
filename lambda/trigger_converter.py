import requests

def lambda_handler(event, context):
    
    # Parsing event records for bucket name and new file entry
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    filename = (event['Records'][0]['s3']['object']['key']).split(".")[0]

    print("File received in bucket: ", bucket)

    print("New submitted file name: ", filename)
    
    # Sending POST request to public EC2 IPv4 address to exposed Flask webapp port
    url = "http://{Replace with EC2 Instance's Public IPv4 Address}:5000/" + filename
    response = requests.post(url)

    # Check the response
    if response.status_code == 200:
        print('POST request successful!')
    else:
        print(f'Error: {response.status_code}')

    # Logs
    return response.text
