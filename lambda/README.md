## Presigned URL Generator Function

This `Lambda` function will handle file upload requests to the input bucket and utilize `API Gateway` which will provide an endpoint which will call the function to generate a presigned url for the S3 bucket to upload the files with.

### Features
- `HTTP` API with endpoint to trigger the `Lambda` function
- `Lambda` function which queries `S3` bucket to return unique Presigned URL.
- Presigned URL is generated on the basis of object parameters such as `URL Expiration time`, `File Content type` etc. 
- Frontend site sends a `GET` request to the API endpoint using the `await axios` operation during file upload.

The response body includes the presigned upload URL which accepts content type of `application/vnd.openxmlformats-officedocument.wordprocessingml.document` for .docx files, and the `Object Key` name with which it will be uploaded to the bucket

### Endpoints
The resource for this API looks like [https://abcdefghij.execute-api.us-east-1.amazonaws.com/](https://abcefghij.execute-api.us-east-1.amazonaws.com/dev/register) with the following path `/getPresignedURL` and is used to upload `.docx` files

The following script shows that [presignedURL.js](./presignedURL.mjs) only has a GET method route with params mentioned in `s3Params`

```javascript
// Get signed URL from S3
const s3Params = {
  Bucket: process.env.UploadBucket,
  Key,
  Expires: URL_EXPIRATION_SECONDS,
  ContentType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',

  // This ACL makes the uploaded object publicly readable. 
  ACL: 'public-read'
}

const uploadURL = await getSignedUrl(s3Client, new PutObjectCommand(s3Params), {expiresIn: 300});

const response = {
      statusCode: 200,
      headers: {
        'Key': Key
      },
      body: JSON.stringify({ uploadURL: uploadURL, Key: Key }),
      isBase64Encoded: false
};
```

### Error Codes 5XX & 4XX
* 5XX (Internal Server Error): The server failed to fulfill an apparently valid request
* 4XX (Client Error): The request contains bad syntax or cannot be fulfilled

### Example Requests

The `curl` command is used to test the function locally using the following command or using POSTMAN

```bash
curl API_Resource_URL/API_ENDPOINT 
```

The output to the above command should be:
```bash
{"uploadURL":"https://bucket-name.s3.amazonaws.com/fileID.docx?AWSAccessKeyId=AccessKey&Content-Type=application%2Fvnd.openxmlformats-officedocument.wordprocessingml.document&Expires=1706262011&Signature=[unique_signature_string]","Key":"fileID.docx"}
```

## Setup

- Go to AWS Console > Lambda from Services
- Create a Lambda function with Node.js 20.x and configure it as follows:

  ![image](https://github.com/SourasishBasu/File-Wizard/assets/89185962/59106a88-b39f-41db-b548-f8cd20ca11fe)

- Under Triggers select API Gateway and create a new API

  ![image](https://github.com/SourasishBasu/File-Wizard/assets/89185962/8b8336fa-582e-452a-be5e-9f06859bfa80)

- Paste the [presignedURL.mjs](./presignedURL.mjs) within Code Source Panel.
- Under Configuration > Triggers, save the `API Endpoint URL` which will be used by the frontend to query the Lambda function to retreive the presigned URL
- Under Configuration > Permission, go to Role. Go to Permission Policies and select Add Permissions > Create Inline Policy.
- Switch to JSON within Policy Editor and paste the below policy.

```json
{
  "Version": "2012-10-17",
  "Statement":
  [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action":[
        "s3:PutObject",
        "s3:GetObject",
        "s3:PutObjectAcl"],
      "Resource": "arn:aws:s3:::upload-bucket/*"
    }
  ]
}
```

This policy gives the `presignedURL Lambda function` access to the `uploads-bucket` on S3 which provides permissions to it to generate a presigned URL for uploading a file object to that bucket.

- Click Next. Name the policy `uploads-policy` and select Create Policy.

### S3 Upload-Bucket configuration

- Go to input bucket's Permissions and under CORS copy the below policy into it:
  
  ```
  <CORSConfiguration>
    <CORSRule>
      <AllowedOrigin>http://your-website-domain.com/</AllowedOrigin>
      <AllowedMethod>PUT</AllowedMethod>
      <AllowedMethod>POST</AllowedMethod>
      <AllowedMethod>DELETE</AllowedMethod>
      <MaxAgeSeconds>3000</MaxAgeSeconds>
      <AllowedHeader>*</AllowedHeader>
    </CORSRule>
  </CORSConfiguration>
  ```

- Paste the below policy under Bucket Policy:

  ```json
  {
    "Version": "2012-10-17",
    "Statement":
    [
      {
        "Sid": "PublicRead",
        "Effect": "Allow",
        "Principal":"*",
        "Action":[
          "s3:PutObject",
          "s3:GetObject",
          "s3:PutObjectAcl"],
        "Resource": "arn:aws:s3:::upload-bucket/*"
      }
    ]
  }
  ```

- Ensure Object ACL is enabled and `Block Public Access` is turned off under input bucket's Permissions.

## Converter Trigger Function

This `Lambda` function will listen for new file upload events on `uploads-bucket` on S3 and trigger the Python based file converter application running within an `EC2 instance` by sending a `POST` request with the `file name` to the application listening for requests on a port exposed on its public IPv4 address.

### Features
- Listens for `Object Created` Events on `uploads-bucket` on `S3`.
- `Lambda` function parses event record to retrieve file name and bucket name.
- Sends a `POST` request to instance IP address with file name.

The response body includes the server message: 

```bash
"File downloaded, converted and uploaded successfully"
```

### Setup

- Go to AWS Console > Lambda from Services
- Create a Lambda function and configure it as follows:

![image](https://github.com/SourasishBasu/File-Wizard/assets/89185962/2ee1634e-97e0-4687-9ca7-59600a145d18)

- Under Triggers select S3 and create a new API

![s3trigger](https://github.com/SourasishBasu/File-Wizard/assets/89185962/31d68ba3-7bb9-461b-a9a1-c792a56d4da7)
