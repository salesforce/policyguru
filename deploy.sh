#!/usr/bin/env bash
set -e

die() {
    echo "$@"
    exit
}

subdomain=$1
domain_name=$2

[ -z "$subdomain" ] && die "Missing subdomain name.  Usage: $0 cloudsplaining sfdcspace.com";
[ -z "$domain_name" ] && die "Missing domain name.  Usage: $0 cloudsplaining sfdcspace.com";

# Given the registered domain name, grab the Hosted Zone ID and supply it to the sam deploy parameter
hostedZone=$(aws route53 list-hosted-zones-by-name | jq --arg name "${domain_name}." -r '.HostedZones | .[] | select(.Name=="\($name)") | .Id')
prefix="/hostedzone/"
hostedZoneId=`echo "$hostedZone" | cut -c 13-`

echo "Will deploy to ${subdomain}.${domain_name}"

sam deploy --parameter-overrides HostedZoneId=${hostedZoneId} DomainName=${domain_name} Subdomain=${subdomain}
