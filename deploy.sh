#!/usr/bin/env bash
set -e

die() {
    echo "$@"
    exit
}

# Must export these variables beforehand. These usually live in a file titled "samconfig.toml", but we don't want to store the deployment details in this Git Repo.
declare -a vars=(S3_BUCKET S3_PREFIX STACK_NAME CAPABILITIES AWS_REGION SUBDOMAIN DOMAIN_NAME)

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

echo "Will deploy to ${SUBDOMAIN}.${DOMAIN_NAME}"

sam deploy \
  --parameter-overrides HostedZoneId=${hostedZoneId} DomainName=${DOMAIN_NAME} Subdomain=${SUBDOMAIN} \
  --stack-name ${STACK_NAME} \
  --s3-bucket ${S3_BUCKET} \
  --s3-prefix ${S3_PREFIX} \
  --capabilities ${CAPABILITIES} \
  --region ${AWS_REGION}

echo "Copying the UI files to the S3 bucket"
aws s3 sync ./static/ s3://${SUBDOMAIN}.${DOMAIN_NAME} --delete

# Uncomment this when we have the Route53 stuff worked out.
echo "View the website here: http://${SUBDOMAIN}.${DOMAIN_NAME}.s3-website.${AWS_REGION}.amazonaws.com/"

#echo "View the updates at: https://${subdomain}.${domain_name}"