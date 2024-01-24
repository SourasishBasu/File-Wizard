// NodeJS 18.x
// This function is triggered during file upload process when the GET request
// is made to the HTTP API to return a Presigned S3 bucket URL to upload the .docx file

'use strict'

const AWS = require('aws-sdk')
AWS.config.update({ region: process.env.AWS_REGION })
const s3 = new AWS.S3()

// Change this value to adjust the signed URL's expiration
const URL_EXPIRATION_SECONDS = 300

// Main Lambda entry point
exports.handler = async (event) => {
  return await getUploadURL(event)
}

// Generate the PresignedURL to be sent to static site during file upload
const getUploadURL = async function(event) {

  // Create a random number based file name for uploading to prevent file overwrite or conflicts
  const randomID = parseInt(Math.random() * 10000000)
  const Key = `${randomID}.docx`

  // Get signed URL from S3
  const s3Params = {
    Bucket: process.env.UploadBucket,
    Key,
    Expires: URL_EXPIRATION_SECONDS,
    ContentType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',

    // This ACL makes the uploaded object publicly readable. 
    ACL: 'public-read'
  }

  // Generate the Presigned URL with the provided S3 object parameters
  console.log('Params: ', s3Params)
  const uploadURL = await s3.getSignedUrlPromise('putObject', s3Params)

  // Send upload URL and file name as Key in the API response body
  const response = {
        "statusCode": 200,
        "headers": {
            "Key": Key
        },
        "body": JSON.stringify({uploadURL: uploadURL, Key: Key}),
        "isBase64Encoded": false
    };
  
  console.log(response.body)

  return response;
 
}
