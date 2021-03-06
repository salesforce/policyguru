#!/usr/bin/env bash
set -e

die() {
    echo "$@"
    exit
}

sam build --use-container

DEPLOYMENT_BUCKET="${1:-samcli-deployment-bucket-policyguru.io}"
WEBSITE_BUCKET="${1:-website.policyguru.io}"
S3_PREFIX="${1:-policyguru}"
STACK_NAME="${1:-policyguru}"
CAPABILITIES="${1:-CAPABILITY_IAM}"
AWS_REGION="${1:-us-east-1}"
DOMAIN_NAME="${1:-policyguru.io}"

# Must export these variables beforehand. These usually live in a file titled "samconfig.toml", but we don't want to store the deployment details in this Git Repo.
declare -a vars=(DEPLOYMENT_BUCKET S3_PREFIX STACK_NAME CAPABILITIES AWS_REGION DOMAIN_NAME WEBSITE_BUCKET)

# Check required environment variables
for var_name in "${vars[@]}"
do
  if [ -z "$(eval "echo \$$var_name")" ]; then
    echo "Missing environment variable $var_name"
    exit 1
  fi
done

# Given the registered domain name, grab the Hosted Zone ID and supply it to the sam deploy parameter
hostedZone=$(aws route53 list-hosted-zones-by-name | jq --arg name "${DOMAIN_NAME}." -r '.HostedZones | .[] | select(.Name=="\($name)") | .Id')
prefix="/hostedzone/"
hostedZoneId=`echo "$hostedZone" | cut -c 13-`
echo "Will deploy to ${DOMAIN_NAME}"

# Check if the AWS credentials profile is set
if [ -z "$(eval "echo ${AWS_PROFILE}")" ]; then
  profile_cmd=""
else
  echo "AWS_PROFILE environment variable exists. Using --profile flag."
  profile_cmd="--profile ${AWS_PROFILE}"
fi

sam deploy \
  --parameter-overrides HostedZoneId=${hostedZoneId} DomainName=${DOMAIN_NAME} WebsiteBucketName=${WEBSITE_BUCKET} \
  --stack-name ${STACK_NAME} \
  --s3-bucket ${DEPLOYMENT_BUCKET} \
  --s3-prefix ${S3_PREFIX} \
  ${profile_cmd} \
  --capabilities ${CAPABILITIES} \
  --region ${AWS_REGION} \
  --no-fail-on-empty-changeset \
  --debug

echo "Copying the UI files to the S3 bucket"
aws s3 sync ./static/ s3://${WEBSITE_BUCKET} --delete

echo "View the updates at: https://${DOMAIN_NAME}"