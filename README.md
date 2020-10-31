# policy-sentry-ui

Here, we will store code for the following:

* REST API for Policy Sentry
  * Will be deployed to AWS as Lambdas, exposed as an API gateway
  * Uses Serverless Framework
* User interface POC for Policy Sentry
  * Plain HTML and JS for right now
  * It will point to the API Gateway mentioned above

## Commands

### Serverless framework

* Setup:

```bash
# Install the serverless CLI
npm install -g serverless
# Install the dependencies
npm install
```

* Try invoking the function locally before we deploy it to the cloud provider

```bash
sls invoke local -f scan_policy --path events/scan-policy-mock.json
sls invoke local -f write_policy --path events/write-policy-mock.json

sls invoke local -f query_actions --path events/query-actions-mock.json
sls invoke local -f query_resources --path events/query-resources-mock.json
sls invoke local -f query_conditions --path events/query-conditions-mock.json
```

* Authenticate to AWS over command line

* To deploy the Lambda function using the Serverless framework, run:

```bash
# Deploy
sls deploy
```

* Invoke the Lambda function using mock data and return the output:

```bash
sls invoke -f write_policy --path events/write-policy-mock.json
sls invoke -f scan_policy --path events/scan-policy-mock.json

sls invoke -f query_actions --path events/query-actions-mock.json
sls invoke -f query_resources --path events/query-resources-mock.json
sls invoke -f query_conditions --path events/query-conditions-mock.json
```

### Local Flask API

We set up a Flask API option for local testing and development purposes - particularly for testing out the UI.

* First, install Dev dependencies so we can use Flask

```bash
pip3 install -r requirements-dev.txt
```

* Then run the Flask API locally

```bash
python3 local_run.py
```
