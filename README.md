<a href="https://basu-doc-frontend.s3.us-east-1.amazonaws.com/index.html?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjELj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCmFwLXNvdXRoLTEiSDBGAiEA%2BM6HhnAAB1TdDLe5JRk4rq%2FpAHyUvOTxXLSlRLe%2FCB0CIQCPCmccrkLyilG0PPMqJeAh7IStFb0fOwpaUbv7Hd4%2FairkAghxEAAaDDA0ODgyMzM5MjU5NyIM1hbH6n97SJL8m768KsECy3JoxvK2uAQbTB46tS5%2FrcMw1z6xvDJBR1gUf9YZejMGKjh0Y6WUChWNbQ8Ha9dxMtkkalKUIooEpee2d6SA6chISH0BqsjWLAg2NfyFq%2BqBMySDq9p1fG9snthRkuqdOKB%2BF9cxGD%2B69sbtudQ6r2Bo%2Fs3zoEBL32BkbsFORn%2BV7CwrgK5Wyxdbmu77f1PFT4iD1utis2FcalfIvx4bajGrnOmsI%2BzlqMsrMkZj5IhvXduCO29u1pBHIZv%2Fp2cWfHIYHFaM4eLhwHCZZ9yVuDdUU7jtHc5BIEnU1aqyx0%2Ft5SAplmbBYPNB65sGh7JX31t9007kebE8OVXq4B61%2B5scKkL4I%2BNtbBT4OYC28qfcXwgLGUu%2FAijvZ5xHijWPnidgIpmgtuaVi0yZPYN%2FuL15wj7D4%2BiDaIY%2FKH8FOF5qMJX9wq0GOrICwd4g6yteGe0LEBHzigQbcdn4TP0tUZNACCZ9SGcrkxVEjhz5dBoKtVqbVvxbuikjBhEvNiEmqbUWcReCPHE3MlJGPFqCE6UHrhUiOct0N%2FBZUojKPGAgbXv0cAbLGsO9sDbucak64m8MxgWEmnb5WUaukjF8ZvUpY3%2FQsZ1cQFIqHlz3vRpCyH8enbAonqRRs5%2FwWUtVxMEqnVrbL2L7SJvVx%2BZKGLD7lO8dpLUetIg9zKGldlCrjWutxSLJVhszuxjGarsYoi%2F8qXexVyrDl6cUWKD0ocu%2FTEonQRlY%2Bf9E89Nq6KqNpMLcApYZa1ffolj9xkBGqvG6jYFGeXo0SZnBEwxLg3w4PbqqiFv%2F%2FjgBr1Tpk%2Fa8X%2BA1pFpFZ7mH%2B9gqKJM5dGBejHxKCX77T4Sl&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240124T150308Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQWXQZ3FK5WZQIT7D%2F20240124%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=dd27942c19d867d629c3199a78b934508cf0626ee81c6eca28cd4e85f9ac7a28">
  <img alt="Vue.js and Python" src="./assets/banner.png">
  <h1 align="center">File Wizard</h1>
</a>

<p align="center">
  An open-source file conversion webapp built with Vue.js, Python<br>
  and AWS for the HTTP API, Lambda functions and S3 object storage.<br>Converts .docx files to .pdf
</p>

<p align="center">
  <a href="#features"><strong>Features</strong></a> ·
  <a href="#running-locally"><strong>Running locally</strong></a> ·
  <a href="#overview"><strong>Overview</strong></a> ·
  <a href="#api-routing"><strong>API Routing</strong></a> ·
  <a href="#aws-configuration-for-sns"><strong>AWS Configuration</strong></a> ·
  <a href="#authors"><strong>Authors</strong></a>
</p>


## Features

- **Website**
  - [Vue.js](https://vuejs.org) App Router
  - [Amazon Web Services](https://docs.aws.amazon.com/) for backend functionality
  - Support for `HTTP API`, `S3` File Storage, and `Lambda` functions
  - Edge runtime-ready
  
- **AWS Infrastructure**
  - [Amazon S3](https://aws.amazon.com/s3) Allows for object storage and static site hosting
  - [API Gateway](https://aws.amazon.com/eventbridge) hosts the HTTP API 
  - [AWS Lambda](https://aws.amazon.com/lambda) for processing JSON and filtering required data
  - [Amazon EC2](https://aws.amazon.com/sns) for provisioning VM instances 

### Tech Stack
![Vue.js](https://img.shields.io/badge/Vue.js-43853D?style=for-the-badge&logo=vuedotjs&logoColor=white)
![Python](https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white)
![EC2](https://img.shields.io/badge/ec2-orange?style=for-the-badge&logo=amazon-ec2&logoColor=white)
![API Gateway](https://img.shields.io/badge/API%20Gateway-8A2BE2?style=for-the-badge&logo=amazon-api-gateway&logoColor=white)
![S3](https://img.shields.io/badge/S3-2d2dba?style=for-the-badge&logo=amazon-s3&logoColor=white)
![Lambda](https://img.shields.io/badge/Lambda-FF9900?style=for-the-badge&logo=aws-lambda&logoColor=white)


## Overview
<img alt="AWS Architecture" src="./assets/architecture-overview.png">

A static site is hosted on `S3` with a document upload form. We use `API Gateway` to create an API which makes a `GET` request to a `Lambda` function after the user clicks <kbd>Upload File</kbd> on the form.

The API sends a `presigned bucket URL` for the `uploads-bucket`. The site then automatically conducts a `PUT` request to the same bucket with the `.docx` file data.

Another `Lambda` function is configured to listen for `PUT Object events` in the S3 `uploads-bucket`. It parses the event record for file name and sends a `POST` request to the Python `Flask App` performing the document conversion.

An `EC2` instance is deployed with an Ubuntu OS image. A python script is setup to run as a background process.

The python `microservice` converts documents using `pandoc` package and is exposed as an API using `Flask` listening for `POST` requests on a specified port. It downloads and saves the specified file with its ID, uploads the converted file to the `output-bucket` on `S3` and performs cleanup for files saved during runtime.

The static site returns the download link for the converted file from the `output-bucket`.

## Running locally

First, run the development flask server on Ubuntu Linux:

### Installation
```bash
sudo apt update && apt upgrade
sudo apt install pandoc texlive
sudo apt install python3.10-venv
```

### Setup Python venv and script

```bash
python3 -m venv venv
source venv/bin/activate
mkdir inputs outputs
touch app.py
```

The Flask app should be able to handle requests at all times. It can be run as a background process using `nohup` command to ensure application uptime as long as VM is running even if we were to exit out of remote shell.

The `&` displays the process ID for the python process which may be recorded to perform `kill <PID>` in case the process it to be stopped.

The logs and stdout along with stderr is saved to `log.txt`.

```bash
sudo su
nohup python3 app.py > log.txt 2>&1 &
```

The flask app should now be running on:
[http://{ec2-instance-public-ipv4-address}:5000](http://{ec2-instance-public-ipv4-address}:5000/)

> [!WARNING]
> This command only starts the webapp. You will need to configure the instance Security Group to allow TCP connections to port 5000 of the EC2 instance from any external IPv4 address [0.0.0.0/0] on AWS to get the full functionality.

## API Routing

The `HTTP API` is hosted on AWS using  Lambda function which deploys a `Serverless Express.js app`. Source code for lambda function is in the [`amplify/backend/function/formfunction/src/app.js`](./amplify/backend/function/formfunction/src/app.js)
 

> [!NOTE]
> To learn more about the `Serverless Express.js app` and how to deploy it, visit the [`amplify/README.md`](./amplify/README.md) 

## AWS Configuration for S3


> [!NOTE]
> To learn more about the `S3` static site and how to deploy it, visit the [`lambda-sns/README.md`](./lambda-sns/README.md) 

## Authors

This project is created by [MLSA KIIT](https://mlsakiit.com) for Cloud Computing Domain's Project Wing:

- Sourasish Basu ([@SourasishBasu](https://github.com/SourasishBasu)) - [MLSA KIIT](https://mlsakiit.com)

## Version
| Version | Date          		| Comments        |
| ------- | ------------------- | --------------- |
| 1.0     | Jan 24th, 2024   | Initial release |

## Future Roadmap
**Website/API**
- [ ] HTTPS Validation
- [ ] File Validation and Sanitization on server side using SHA checksums
- [ ] Better pdf engine to improve formatting during conversion
- [ ] Better Error Handling
  
**AWS Infrastructure**
- [ ] Actual implementation in production
- [ ] Conversion feature between multiple file types
- [ ] Implementing image compression using methods such as Huffman Encoding

## Usage

<p align="center"> 
  <img src="https://github.com/MLSAKIIT/Registration-Validator-SMS/blob/f29507912629613b2ca8ac423484c0b7d6409029/assets/form.png" />
   <br><b>Upload Form template</b>
</p>
<br>
<p align="center"> 
  <img src="https://github.com/MLSAKIIT/Registration-Validator-SMS/blob/f29507912629613b2ca8ac423484c0b7d6409029/assets/registrations.png" />
   <br><b>S3 uploads-bucket for .docx files</b>
</p>
<br>
<p align="center"> 
  <img src="https://github.com/MLSAKIIT/Registration-Validator-SMS/blob/f29507912629613b2ca8ac423484c0b7d6409029/assets/ss.png" />
   <br><b>S3 output-bucket for .pdf files</b>
</p>

----
