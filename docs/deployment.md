# Deployment

## Step 0: Install Prerequisites

* AWS CLI

```bash
brew install awscli
```

* AWS SAM CLI

```bash
brew tap aws/tap
brew install aws-sam-cli
```
* Docker: should be installed and running locally. See installation instructions [here](https://docs.docker.com/get-docker/)
* Authenticate to your AWS account via CLI

## Step 1: Purchase a domain name via Route53

You will need to purchase a domain name via Route53. You can follow the documentation [here](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/registrar.html).

## Step 2: Create a Route53 Public Hosted Zone

You will need to create a Route53 Public Hosted Zone that matches the domain name that you purchased in the previous step.

* After you register the domain name, you can create the hosted zone via the AWS Console or via the command line using the [create-hosted-zone](https://docs.aws.amazon.com/cli/latest/reference/route53/create-hosted-zone.html) command:

```bash
export DOMAIN_NAME="example.com"
aws route53 create-hosted-zone --name $DOMAIN_NAME 
```

## Step 3: Create an S3 bucket to hold the SAM CLI artifacts

The Severless Application Model (SAM) packages applications by creating a `.zip` file of your code and dependencies and uploading the file to an S3 bucket so it can be consumed by CloudFormation.

While we could use the `sam deploy --guided` command in development (because the guided mode automatically creates the S3 bucket, whereas the non-guided mode does not), that can be error prone for a tutorial, and is not conducive to CI/CD pipelines.

* Run this command to create a deployment bucket that will host your SAM CLI artifacts:

```bash
export DEPLOYMENT_BUCKET="samcli-deployment-bucket-myapplication"
aws s3api create-bucket --bucket $DEPLOYMENT_BUCKET --region us-east-1
```

## Step 4: Ensure your IAM user has the minimum required permissions

The following IAM policy represents the minimum permissions needed to create the serverless infrastructure.

<details>
<summary>Required permissions for Serverless deployment</summary>
<br>
<pre>
<code>
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "SkipResourceConstraints",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:ListBucket",
                "s3:GetObject",
                "lambda:GetFunction",
                "lambda:ListTags",
                "lambda:UntagResource",
                "lambda:TagResource",
                "lambda:UpdateFunctionCode",
                "lambda:GetFunctionConfiguration"
            ],
            "Resource": "*"
        },
        {
            "Sid": "MultMultNone",
            "Effect": "Allow",
            "Action": [
                "acm:l*",
                "cloudformation:describea*",
                "cloudformation:describestackd*",
                "cloudformation:describet*",
                "cloudformation:es*",
                "cloudformation:liste*",
                "cloudformation:listi*",
                "cloudformation:liststacks",
                "cloudformation:listt*",
                "cloudformation:v*",
                "cloudfront:getca*",
                "cloudfront:getf*",
                "cloudfront:geto*",
                "cloudfront:getp*",
                "cloudfront:listc*",
                "cloudfront:listd*",
                "cloudfront:listf*",
                "cloudfront:listo*",
                "cloudfront:listp*",
                "cloudfront:lists*",
                "iam:generatec*",
                "iam:generates*",
                "iam:getacco*",
                "iam:getcontextkeysforc*",
                "iam:getcr*",
                "iam:getor*",
                "iam:getservicela*",
                "iam:listacco*",
                "iam:listgroups",
                "iam:listo*",
                "iam:listpolici*",
                "iam:listroles",
                "iam:listsa*",
                "iam:listserve*",
                "iam:listusers",
                "iam:listv*",
                "iam:pa*",
                "iam:simulatec*",
                "lambda:getac*",
                "lambda:liste*",
                "lambda:listfunctions",
                "lambda:listl*",
                "route53:geta*",
                "route53:getche*",
                "route53:getg*",
                "route53:gethealthcheckc*",
                "route53:gethostedzonec*",
                "route53:gettrafficpolicyinstancec*",
                "route53:listg*",
                "route53:listh*",
                "route53:listreu*",
                "route53:listtrafficpolici*",
                "route53:listtrafficpolicyinstances",
                "route53:t*",
                "s3:getaccesspoint",
                "s3:getacco*",
                "s3:lista*",
                "s3:listj*"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Sid": "CloudformationMultStackcloudsplaining",
            "Effect": "Allow",
            "Action": [
                "cloudformation:describec*",
                "cloudformation:describestacke*",
                "cloudformation:describestackr*",
                "cloudformation:detectstackd*",
                "cloudformation:detectstackr*",
                "cloudformation:g*",
                "cloudformation:ca*",
                "cloudformation:co*",
                "cloudformation:createc*",
                "cloudformation:createstack",
                "cloudformation:deletec*",
                "cloudformation:deletestack",
                "cloudformation:ex*",
                "cloudformation:si*",
                "cloudformation:updatestack",
                "cloudformation:updatet*",
                "cloudformation:describestacks",
                "cloudformation:listc*",
                "cloudformation:liststackr*",
                "cloudformation:t*",
                "cloudformation:un*",
                "cloudformation:sets*"
            ],
            "Resource": [
                "arn:aws:cloudformation:us-east-1:*:stack/policyguru*/*",
                "arn:aws:cloudformation:us-east-1:*:stack/policyguru*/*",
                "arn:aws:cloudformation:us-east-1:aws:transform/Serverless-2016-10-31"
            ]
        },
        {
            "Sid": "AcmMultCertificate",
            "Effect": "Allow",
            "Action": [
                "acm:des*",
                "acm:e*",
                "acm:g*",
                "acm:del*",
                "acm:i*",
                "acm:ren*",
                "acm:res*",
                "acm:u*",
                "acm:a*",
                "acm:rem*"
            ],
            "Resource": [
                "arn:aws:acm:us-east-1:*:certificate/*"
            ]
        },
        {
            "Sid": "LambdaMultFunctionscanpolicyfunction",
            "Effect": "Allow",
            "Action": [
                "lambda:getal*",
                "lambda:getf*",
                "lambda:getpo*",
                "lambda:listt*",
                "lambda:getpr*",
                "lambda:getpr*",
                "lambda:createa*",
                "lambda:createf*",
                "lambda:deletea*",
                "lambda:deletef*",
                "lambda:i*",
                "lambda:publishv*",
                "lambda:putf*",
                "lambda:updatea*",
                "lambda:updatef*",
                "lambda:deletep*",
                "lambda:putp*",
                "lambda:deletep*",
                "lambda:putp*",
                "lambda:lista*",
                "lambda:listfunctione*",
                "lambda:listp*",
                "lambda:listv*",
                "lambda:t*",
                "lambda:un*",
                "lambda:addp*",
                "lambda:di*",
                "lambda:e*",
                "lambda:removep*"
            ],
            "Resource": [
                "arn:aws:lambda:us-east-1:*:function:ScanPolicyFunction",
                "arn:aws:lambda:us-east-1:*:function:ScanPolicyFunction/*",
                "arn:aws:lambda:us-east-1:*:function:WritePolicyFunction",
                "arn:aws:lambda:us-east-1:*:function:WritePolicyFunction/*",
                "arn:aws:lambda:us-east-1:*:function:Query*",
                "arn:aws:lambda:us-east-1:*:function:Query*/*"
            ]
        },
        {
            "Sid": "CloudformationMultStacksetcloudsplaining",
            "Effect": "Allow",
            "Action": [
                "cloudformation:describestacki*",
                "cloudformation:describestackse*",
                "cloudformation:detectstacks*",
                "cloudformation:gettemplates*",
                "cloudformation:createstacki*",
                "cloudformation:deletestacki*",
                "cloudformation:deletestacks*",
                "cloudformation:st*",
                "cloudformation:updatestacki*",
                "cloudformation:updatestacks*",
                "cloudformation:liststacki*",
                "cloudformation:liststackse*",
                "cloudformation:t*",
                "cloudformation:un*"
            ],
            "Resource": [
                "arn:aws:cloudformation:us-east-1:*:stackset/policyguru*/*:*",
                "arn:aws:cloudformation:us-east-1:*:stackset/policyguru/*:*"
            ]
        },
        {
            "Sid": "S3MultCloudsplaining",
            "Effect": "Allow",
            "Action": [
                "s3:geto*",
                "s3:a*",
                "s3:deleteobject",
                "s3:deleteobjectversion",
                "s3:putobject",
                "s3:putobjectl*",
                "s3:putobjectr*",
                "s3:replicated*",
                "s3:replicateo*",
                "s3:res*",
                "s3:listm*",
                "s3:deleteobjectt*",
                "s3:deleteobjectversiont*",
                "s3:putobjectt*",
                "s3:putobjectversiont*",
                "s3:replicatet*",
                "s3:b*",
                "s3:o*",
                "s3:putobjecta*",
                "s3:putobjectversiona*"
            ],
            "Resource": [
                "arn:aws:s3:::*policyguru*/*",
                "arn:aws:s3:::policyguru*/*"
            ]
        },
        {
            "Sid": "S3MultCloudsplainingnone",
            "Effect": "Allow",
            "Action": [
                "s3:getaccel*",
                "s3:getan*",
                "s3:getb*",
                "s3:gete*",
                "s3:geti*",
                "s3:getl*",
                "s3:getm*",
                "s3:getr*",
                "s3:createb*",
                "s3:deletebucket",
                "s3:deletebucketo*",
                "s3:deletebucketw*",
                "s3:putaccel*",
                "s3:putan*",
                "s3:putbucketc*",
                "s3:putbucketl*",
                "s3:putbucketn*",
                "s3:putbucketo*",
                "s3:putbucketr*",
                "s3:putbucketv*",
                "s3:putbucketw*",
                "s3:pute*",
                "s3:puti*",
                "s3:putl*",
                "s3:putm*",
                "s3:putr*",
                "s3:listb*",
                "s3:putbuckett*",
                "s3:deletebucketp*",
                "s3:putbucketa*",
                "s3:putbucketp*"
            ],
            "Resource": [
                "arn:aws:s3:::policyguru*",
                "arn:aws:s3:::*policyguru*"
            ]
        },
        {
            "Sid": "IamMultRolecloudsplaining",
            "Effect": "Allow",
            "Action": [
                "iam:getcontextkeysforp*",
                "iam:getr*",
                "iam:getserviceli*",
                "iam:simulatep*",
                "iam:listattachedr*",
                "iam:listinstanceprofilesf*",
                "iam:listrolep*",
                "iam:listrolet*",
                "iam:tagr*",
                "iam:untagr*",
                "iam:attachr*",
                "iam:creater*",
                "iam:createservicel*",
                "iam:deleter*",
                "iam:deleteservicel*",
                "iam:detachr*",
                "iam:pa*",
                "iam:putr*",
                "iam:updateas*",
                "iam:updater*"
            ],
            "Resource": [
                "arn:aws:iam::*:role/policyguru*"
            ]
        },
        {
            "Sid": "ExecuteapiWriteExecuteapigeneral",
            "Effect": "Allow",
            "Action": [
                "execute-api:i*",
                "execute-api:m*"
            ],
            "Resource": [
                "arn:aws:execute-api:us-east-1:*:*/*/*/*"
            ]
        }
    ]
}
</code>
</pre>
</details>

## Step 5: Deployment Settings

We will go over two options for deployment.
* Option 1: Manual deployment (i.e., from the command line)
* Option 2: From GitHub Actions

### Step 5 (Option 1): Set Deployment settings as environment variables

We have some automation that bootstraps the deployment in `scripts/deploy.sh`. However, that deployment script expects several environment variables.

* Create a file titled `deploy_private_settings.sh`

```bash
touch deploy_private_settings.sh
chmod +x ./deploy_private_settings.sh
```

* Specifically, you will need to set the values for the environment variables listed below. Insert those into the `deploy_private_settings.sh` file:

```bash
#!/usr/bin/env bash

export DEPLOYMENT_BUCKET="" # name of the S3 bucket you created before 
export DOMAIN_NAME="" # name of the Route53 hosted zone you created previously
export WEBSITE_BUCKET=""  # this will be the name of the S3 bucket that is tied to your CloudFront. It's not public, and the name does not matter.
export S3_PREFIX="policyguru"
export STACK_NAME="policyguru"
export CAPABILITIES="CAPABILITY_IAM"
export AWS_REGION="us-east-1"
```

_Note: Just fill in the values for the environment variables `DEPLOYMENT_BUCKET`, `DOMAIN_NAME`, AND `WEBSITE_BUCKET`. You can leave the non-empty values as-is._

* Now source the file so the environment variables are present in your shell session:

```bash
source ./deploy_settings.sh
```

### Step 5 (Option 2): Set Deployment settings via GitHub actions

* After creating the IAM user, download the CSV file containing the AWS Access Keys and set up the access keys as Secrets in your GitHub repository. The official documentation for setting GitHub secrets is [here](https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository).

* Go to your GitHub repository under _Settings_ > _Secrets_ > _New Repository Secret_

* You will enter two secrets - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, respectively.

* Copy the values from their respective columns in the CSV file and add the secrets.

* Add two more secrets
  * `DEPLOYMENT_BUCKET`: This should be the name of the S3 bucket that you created in **Step 3**
  * `WEBSITE_BUCKET`: Whatever you want to call the bucket that holds your static website files that call the REST API.
    * It doesn't matter what this is called, as long as it has a unique name in the S3 global namespace. The website bucket does not leverage the [Static Website](https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html) S3 functionality
    * Instead, it [uses CloudFront to serve the static website hosted on S3](https://docs.aws.amazon.com/AmazonS3/latest/dev/website-hosting-cloudfront-walkthrough.html).
  * `AWS_REGION`: Set this to the AWS Region that you want to deploy this infrastructure to.
  * `DOMAIN_NAME`: Set this to the domain name that you created in Step 2.

## Step 6: Deployment

We will go over two options for deployment in this section
* Option 1: Manual deployment (i.e., from the command line)
* Option 2: From GitHub Actions

### Step 6 (Option 1): Build Serverless artifacts and Run the deployment script

First you will need to build the serverless application using the `sam build --use-container`. This command gathers the build artifacts of your application's dependencies and places them in the proper format and location for next steps, such as locally testing, packaging, and deploying.

* Run the build command:

```bash
sam build --use-container
```

* Then run the deployment script:

```bash
./scripts/deploy.sh
```

This will create the following resources that are defined in the [./template.yaml](../template.yaml) file:
* **Lambda functions** for:
  * Policy Sentry's write-policy function
  * Cloudsplaining's scan-policy function
  * Policy Sentry's functions to query the Actions, Resources, and Condition key tables
* **API Gateway** (HTTP API type). The execute-api endpoint is disabled in favor of Route53.
* **S3 bucket** corresponding to the subdomain and domain name specified in the `deploy_settings.sh` values
* **S3 bucket policy** to allow for static website usage.
* **ACM Certificate**

It will also upload the static website artifacts to the S3 bucket mentioned above.

### Step 6 (Option 2): Run the GitHub Action

With those secrets enabled, once you push to the `main` or `master` branches, your GitHub action should automatically deploy to the domain you provided.

## Step 7: Validating the API

* If we deployed the API to https://api.example.com, you can do a test query with the following:

```bash
export DOMAIN_NAME="example.com"
curl "https://api.${DOMAIN_NAME}/query/actions?service=s3&name=getobject"
```

That will return:

```json
{"s3": [{"action": "s3:GetObject", "description": "Grants permission to retrieve objects from Amazon S3", "access_level": "Read", "resource_arn_format": "arn:${Partition}:s3:::${BucketName}/${ObjectName}", "condition_keys": [], "dependent_actions": []}, {"action": "s3:GetObject", "description": "Grants permission to retrieve objects from Amazon S3", "access_level": "Read", "resource_arn_format": "*", "condition_keys": [], "dependent_actions": []}]}
```
