#!/usr/bin/env bash
set -x

# Run this from the main directory
sls invoke -f scan_policy --path events/scan-policy-mock.json
sls invoke -f write_policy --path events/write-policy-mock.json

sls invoke -f query_actions --path events/query-actions-mock.json
sls invoke -f query_resources --path events/query-resources-mock.json
sls invoke -f query_conditions --path events/query-conditions-mock.json
