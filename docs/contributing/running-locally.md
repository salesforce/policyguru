# Running the API locally

## Option 1: Local FastAPI

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

## Option 2: Docker

You can build a Docker container that hosts this locally. This is hosted on the **8002** local port.

* Build the docker container with docker-compose:

```bash
make run-docker
```

* You can access the docs at the **8002** port: http://localhost:8002/docs

