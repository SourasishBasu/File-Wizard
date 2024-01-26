## Presigned URL Generator Function

This `Lambda` function will handle file upload requests to the input bucket and utilize `API Gateway` which will provide an endpoint which will call the function to generate a presigned url for the S3 bucket to upload the files with.

### Features
- `HTTP` API with endpoint to trigger the `Lambda` function
- `Lambda` function which queries `S3` bucket to return unique Presigned URL.
- Presigned URL is generated on the basis of object parameters such as `URL Expiration time`, `File Content type` etc. 
- Frontend site sends a `GET` request to the API endpoint using the `await axios` operation during file upload.

The response body includes the presigned upload URL which accepts content type of `application/vnd.openxmlformats-officedocument.wordprocessingml.document` for .docx files, and the `Object Key` name with which it will be uploaded to the bucket

### Endpoints
The resource for this API looks like [https://abcdefghij.execute-api.us-east-1.amazonaws.com/](https://abcefghij.execute-api.us-east-1.amazonaws.com/dev/register) with the following path `/getPresignedURL`

The following script shows that [presignedURL.js](./presignedURL.js) only has a GET method route with params mentioned in `s3Params`

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

const uploadURL = await s3.getSignedUrlPromise('putObject', s3Params)

const response = {
      "statusCode": 200,
      "body": JSON.stringify({uploadURL: uploadURL, Key: Key}),
      "isBase64Encoded": false
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

## Converter Function
