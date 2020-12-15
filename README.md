# policy-sentry-ui

Here, we will store code for the following:

* REST API for Policy Sentry
  * Will be deployed to AWS as Lambdas, exposed as an API gateway
  * Uses [AWS Serverless Application Model (SAM)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
* User interface POC for Policy Sentry

<!--ts-->
   * [policy-sentry-ui](#policy-sentry-ui)
      * [Prerequisites](#prerequisites)
   * [Instructions](#instructions)
      * [Deployment](#deployment)
         * [Validating the API](#validating-the-api)
      * [Testing and Development](#testing-and-development)
      * [Running locally](#running-locally)
         * [Invoking Lambdas locally](#invoking-lambdas-locally)
            * [Option 1: Leverage PyInvoke command](#option-1-leverage-pyinvoke-command)
            * [Option 2: Run individual commands](#option-2-run-individual-commands)
      * [Local Flask API](#local-flask-api)
   * [Resources](#resources)

<!-- Added by: kmcquade, at: Mon Dec 14 12:19:18 EST 2020 -->

<!--te-->


## Prerequisites

### Requirement 1: Things to install

* AWS CLI

```bash
brew install awscli
```

* AWS SAM CLI

```bash
brew tap aws/tap
brew install aws-sam-cli
```
* Docker: should be installed and running locally. See installation instructions [here](https://docs.docker.com/get-docker/)
* Authenticate to your AWS account via CLI

### Requirement 2: Purchase a domain name via Route53

You will need to purchase a domain name via Route53. You can follow the documentation here: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/registrar.html.

### Requirement 3: Create a Route53 Public Hosted Zone

You will need to create a Route53 Public Hosted Zone that matches the domain name that you purchased in the previous step.

* After you register the domain name, you can create the hosted zone via the AWS Console or via the command line using the [create-hosted-zone](https://docs.aws.amazon.com/cli/latest/reference/route53/create-hosted-zone.html) command:

```bash
export DOMAIN_NAME="example.com"
aws route53 create-hosted-zone --name $DOMAIN_NAME 
```

### Requirement 4: Create an S3 bucket to hold the SAM CLI artifacts

The Severless Application Model (SAM) packages applications by creating a `.zip` file of your code and dependencies and uploading the file to an S3 bucket so it can be consumed by CloudFormation.

While we could use the `sam deploy --guided` command in development (because the guided mode automatically creates the S3 bucket, whereas the non-guided mode does not), that can be error prone for a tutorial, and is not conducive to CI/CD pipelines.

* Run this command to create a deployment bucket that will host your SAM CLI artifacts:

```bash
export DEPLOYMENT_BUCKET="samcli-deployment-bucket-myapplication"
aws s3api create-bucket --bucket $DEPLOYMENT_BUCKET --region us-east-1
```

# Instructions

## Deployment

### Step 1: Deployment settings

We have some automation that bootstraps the deployment in `deploy.sh`. However, that deployment script expects several environment variables.

* Create a file titled `deploy_private_settings.sh`

```bash
touch deploy_private_settings.sh
chmod +x ./deploy_private_settings.sh
```

* Specifically, you will need to set the values for the environment variables listed below. Insert those into the `deploy_private_settings.sh` file:

```bash
#!/usr/bin/env bash

export DEPLOYMENT_BUCKET="" # name of the S3 bucket you created before 
export DOMAIN_NAME="" # name of the Route53 hosted zone you created previously
export WEBSITE_BUCKET=""  # this will be the name of the S3 bucket that is tied to your CloudFront. It's not public, and the name does not matter.
export S3_PREFIX="policyguru"
export STACK_NAME="policyguru"
export CAPABILITIES="CAPABILITY_IAM"
export AWS_REGION="us-east-1"
```

_Note: Just fill in the values for the environment variables `DEPLOYMENT_BUCKET`, `DOMAIN_NAME`, AND `WEBSITE_BUCKET`. You can leave the non-empty values as-is._

* Now source the file so the environment variables are present in your shell session:

```bash
source ./deploy_settings.sh
```

_Note: In the future, we will just set those environment variables via GitHub environment variables and run this deployment in GitHub actions._

### Step 2: Run the deployment script

* Then run the deployment script:

```bash
./deploy.sh
```

This will create the following resources that are defined in the [./template.yaml](./template.yaml) file:
* **Lambda functions** for:
  * Policy Sentry's write-policy function
  * Cloudsplaining's scan-policy function
  * Policy Sentry's functions to query the Actions, Resources, and Condition key tables
* **API Gateway** (HTTP API type). The execute-api endpoint is disabled in favor of Route53.
* **S3 bucket** corresponding to the subdomain and domain name specified in the `deploy_settings.sh` values
* **S3 bucket policy** to allow for static website usage.
* **ACM Certificate**

It will also upload the static website artifacts to the S3 bucket mentioned above.

### Step 3: Validating the API

* If we deployed the API to https://api.example.com, you can do a test query with the following:

```bash
export DOMAIN_NAME="example.com"
curl "https://api.${DOMAIN_NAME}/query/actions?service=s3&name=getobject"
```

That will return:

```json
{"s3": [{"action": "s3:GetObject", "description": "Grants permission to retrieve objects from Amazon S3", "access_level": "Read", "resource_arn_format": "arn:${Partition}:s3:::${BucketName}/${ObjectName}", "condition_keys": [], "dependent_actions": []}, {"action": "s3:GetObject", "description": "Grants permission to retrieve objects from Amazon S3", "access_level": "Read", "resource_arn_format": "*", "condition_keys": [], "dependent_actions": []}]}
```

# Development

## Environment setup

* Create virtual environment and activate it

```bash
python3 -m venv ./venv && source venv/bin/activate
```

* Install dependencies

```bash
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
```

## Testing

* Run unit tests

```bash
# Option 1: Use PyInvoke that automates this
invoke test.pytest

# Option 2: Run Pytest directly
pytest -v
```

## Running locally

### Invoking Lambdas locally

#### Option 1: Leverage PyInvoke command

Alternatively, you can just run the PyInvoke commands that will run all of the above:

```bash
# list available PyInvoke commands
invoke -l
invoke integration.sam-invoke
```

#### Option 2: Run individual commands

First you will need to build the serverless application using the `sam build --use-container`. This command gathers the build artifacts of your application's dependencies and places them in the proper format and location for next steps, such as locally testing, packaging, and deploying.

* Run the build command:

```bash
sam build --use-container
```

* Run functions locally and invoke them with the `sam local invoke` command.

```bash
sam local invoke WritePolicyFunction --event events/write-policy-mock.json
sam local invoke ScanPolicyFunction --event events/scan-policy-mock.json
sam local invoke QueryActionsFunction --event events/query-actions-mock.json
sam local invoke QueryResourcesFunction --event events/query-resources-mock.json
sam local invoke QueryConditionsFunction --event events/query-conditions-mock.json
```

### Local Flask API

We set up a Flask API option for local testing and development purposes - particularly for testing out the UI.

* First, install Dev dependencies so we can use Flask

```bash
pip3 install -r requirements-dev.txt
```

* Then run the Flask API locally

```bash
# Option 1: Use the PyInvoke wrapper
invoke develop.flask

# Option 2: Run the flask app directly
python3 local_run.py
```


# Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.
