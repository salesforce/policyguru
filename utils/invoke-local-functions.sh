#!/usr/bin/env bash
set -x
# Run this from the main directory
sls invoke local -f scan_policy --path events/scan-policy-mock.json
sls invoke local -f write_policy --path events/write-policy-mock.json

sls invoke local -f query_actions --path events/query-actions-mock.json
sls invoke local -f query_resources --path events/query-resources-mock.json
sls invoke local -f query_conditions --path events/query-conditions-mock.json


# Run the lambdas directly to make sure that the __main__ works properly

python3 lambdas/cloudsplaining_scan_policy/handler.py
python3 lambdas/write_policy/handler.py
python3 lambdas/query_actions/handler.py
python3 lambdas/query_resources/handler.py
python3 lambdas/query_conditions/handler.py
