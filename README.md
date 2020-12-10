# policy-sentry-ui

Here, we will store code for the following:

* REST API for Policy Sentry
  * Will be deployed to AWS as Lambdas, exposed as an API gateway
  * Uses [AWS Serverless Application Model (SAM)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
* User interface POC for Policy Sentry

## Prerequisites

* AWS CLI

```bash
brew install awscli
```

* AWS SAM CLI

```bash
brew tap aws/tap
brew install aws-sam-cli
```
* Docker: should be installed and running locally
* Authenticate to your AWS account via CLI
* There should be a Route53 Public Hosted Zone in the account.

# Instructions

## Deployment

We have some automation that bootstraps the deployment.

* First, set some environment variables that describe your deployment. We have a bash script that supplies some default settings; feel free to alter them according to your needs.

```bash
source ./deploy_settings.sh
```

Note: In the future, we will just set those environment variables via GitHub environment variables and run this deployment in GitHub actions.

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

## Testing and Development

* Create virtual environment and activate it

```bash
python3 -m venv ./venv && source venv/bin/activate
```

* Install dependencies

```bash
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
```

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

## Local Flask API

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