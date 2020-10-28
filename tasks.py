#!/usr/bin/env python
import sys
import logging
from invoke import task, Collection, UnexpectedExit, Failure
logger = logging.getLogger(__name__)

# Create the necessary collections (namespaces)
ns = Collection()

test = Collection('test')
ns.add_collection(test)

unit = Collection('unit')
ns.add_collection(unit)

integration = Collection('integration')
ns.add_collection(integration)

@task
def security_scan(c):
    """Runs `bandit` and `safety check`"""
    try:
        c.run('bandit -r lambdas/')
        # c.run('safety check')
    except UnexpectedExit as u_e:
        logger.critical(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit(1)
    except Failure as f_e:
        logger.critical(f"FAIL: Failure: {f_e}")
        sys.exit(1)


# TEST - format
@task
def format(c):
    """Auto format code with Python `black`"""
    try:
        c.run("black lambdas/")
    except UnexpectedExit as u_e:
        logger.critical(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit(1)
    except Failure as f_e:
        logger.critical(f"FAIL: Failure: {f_e}")
        sys.exit(1)


# TEST - LINT
@task
def run_linter(c):
    """Linting with `pylint`"""
    try:
        c.run('pylint lambdas/', warn=False)
    except UnexpectedExit as u_e:
        logger.critical(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit(1)
    except Failure as f_e:
        logger.critical(f"FAIL: Failure: {f_e}")
        sys.exit(1)


# UNIT TESTING
@task
def run_nosetests(c):
    """Unit testing: Runs unit tests using `nosetests`"""
    c.run('echo "Running Unit tests"')
    try:
        c.run('nosetests -v  --logging-level=CRITICAL')
    except UnexpectedExit as u_e:
        logger.critical(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit(1)
    except Failure as f_e:
        logger.critical(f"FAIL: Failure: {f_e}")
        sys.exit(1)


@task
def run_pytest(c):
    """Unit testing: Runs unit tests using `pytest`"""
    c.run('echo "Running Unit tests"')
    try:
        c.run('python -m coverage run -m pytest -v')
        c.run('python -m coverage report -m')
    except UnexpectedExit as u_e:
        logger.critical(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit(1)
    except Failure as f_e:
        logger.critical(f"FAIL: Failure: {f_e}")
        sys.exit(1)

# INTEGRATION TESTS - make sure sls invoke works locally
@task
def run_serverless_invoke(c):
    """Integration testing: validate sls invoke"""
    c.run('echo "Running Serverless Integration tests"')
    try:
        c.run('sls invoke local -f scan_policy --path events/scan-policy-mock.json')
        c.run('sls invoke local -f write_policy --path events/write-policy-mock.json')
        c.run('sls invoke local -f query_actions --path events/query-actions-mock.json')
        c.run('sls invoke local -f query_resources --path events/query-resources-mock.json')
        c.run('sls invoke local -f query_conditions --path events/query-conditions-mock.json')
    except UnexpectedExit as u_e:
        logger.critical(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit(1)
    except Failure as f_e:
        logger.critical(f"FAIL: Failure: {f_e}")
        sys.exit(1)


unit.add_task(run_nosetests, 'nose')
unit.add_task(run_pytest, 'pytest')

test.add_task(format, 'format')
test.add_task(run_linter, 'lint')
test.add_task(security_scan, 'security')

integration.add_task(run_serverless_invoke, 'serverless-invoke')
