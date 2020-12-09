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
        c.run('sam validate')
    except UnexpectedExit as u_e:
        logger.critical(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit(1)
    except Failure as f_e:
        logger.critical(f"FAIL: Failure: {f_e}")
        sys.exit(1)

@task
def run_sam_validate(c):
    """Validate SAM template"""
    c.run('echo "Validating SAML template"')
    try:
        c.run('python -m coverage run -m pytest -v')
        c.run('python -m coverage report -m')
    except UnexpectedExit as u_e:
        logger.critical(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit(1)
    except Failure as f_e:
        logger.critical(f"FAIL: Failure: {f_e}")
        sys.exit(1)


# INTEGRATION TESTS - make sure sam invoke works locally
@task
def run_sam_invoke(c):
    """Integration testing: validate sam invoke"""
    c.run('echo "Running SAM Integration tests"')
    try:
        c.run('sam build --use-container')
        c.run('sam local invoke WritePolicyFunction --event events/write-policy-mock.json')
        c.run('sam local invoke ScanPolicyFunction --event events/scan-policy-mock.json')
        c.run('sam local invoke QueryActionsFunction --event events/query-actions-mock.json')
        c.run('sam local invoke QueryResourcesFunction --event events/query-resources-mock.json')
        c.run('sam local invoke QueryConditionsFunction --event events/query-conditions-mock.json')
    except UnexpectedExit as u_e:
        logger.critical(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit(1)
    except Failure as f_e:
        logger.critical(f"FAIL: Failure: {f_e}")
        sys.exit(1)


# INTEGRATION TESTS - Run the lambdas directly to make sure that the __main__ works properly
@task
def run_lambdas_directly(c):
    """Integration testing: Running the Lambdas directly to validate that the __main__ works properly with
    its dummy values"""
    c.run('echo "Integration testing: Running the Lambdas directly to validate that the __main__ works properly with '
          'its dummy values"')
    try:
        c.run('python3 lambdas/scan_policy/app.py')
        c.run('python3 lambdas/write_policy/app.py')
        c.run('python3 lambdas/query_actions/app.py')
        c.run('python3 lambdas/query_resources/app.py')
        c.run('python3 lambdas/query_conditions/app.py')
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

integration.add_task(run_sam_invoke, 'sam-invoke')
integration.add_task(run_sam_validate, 'sam-validate')
integration.add_task(run_lambdas_directly, 'run-lambdas-directly')
