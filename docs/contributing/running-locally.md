# Running locally

## Local FastAPI

We set up a FastAPI option for local testing and development purposes - particularly for testing out the UI.

* First, install all dependencies

```bash
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
```

* Then run the API using Uvicorn, a WSGI server.

```bash
# Run the API locally. You can access the docs at localhost:8080/docs
make run
```

## Invoking Lambdas locally

### Option 1: Leverage PyInvoke command

Alternatively, you can just run the [PyInvoke](http://www.pyinvoke.org/) commands that will run all of the above:

```bash
# list available PyInvoke commands
invoke -l
invoke integration.sam-invoke
```

### Option 2: Run individual commands

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


