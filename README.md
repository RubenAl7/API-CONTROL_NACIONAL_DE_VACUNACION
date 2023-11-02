
# NATIONAL VACCINATION CARD API

This is an API designed to manage personal and dependent vaccine records, optimized for deployment on AWS using the Serverless Framework. The API allows users to securely store and retrieve vaccination data for themselves and their dependents.



## Installation and Deployment

Install serverless framework with npm

```bash
  npm install -g serverless
```

Install dependencies with npm (you must be inside any mic_serv... folder)

```bash
  npm install
```

Add your AWS credentials to your environment if you haven't done it before
 
```bash
  serverless config credentials --provider aws --key XXXXXX --secret XXXXXXXXXXXXXXXXXX
```

Deploy the project to AWS (you must be inside any mic_serv... folder)

```bash
  serverless deploy --stage {dev|qa|stg}
```
    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`MONGO_URI=XXXXXXXXXXXXXXXXXXXXXXXX`

`TWILIO_ID = 'XXXXXXXXXXXXXXXXXXXXXXXX'`

`TWILIO_AUTH_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXX'`

`JWT_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXX'`

## Serverless-Framework Documentation

[Documentation](https://www.serverless.com/framework/docs/tutorial)

