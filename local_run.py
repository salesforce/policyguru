#!/usr/bin/env python

from lambdas.local_app import app

app.run(host="localhost", port=5000, debug=True)
