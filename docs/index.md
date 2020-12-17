PolicyGuru Documentation
========================

PolicyGuru is a read-only REST API for [Policy Sentry](https://github.com/salesforce/policy_sentry/), and [Cloudsplaining](https://github.com/salesforce/cloudsplaining).

This REST API also supports [the PolicyGuru Terraform provider](https://github.com/salesforce/terraform-provider-policyguru), which allows you to write least privilege AWS IAM Policies directly from Terraform.

## Why is this useful?

First of all, PolicyGuru's Terraform provider uses this REST API as its default endpoint. But it can be useful to you for two reasons:
1. If you want your own endpoint in case ours goes down (we don't see that happening, but some organizations want this level of assurance)
2. Perhaps you want to improve the WIP default website - we want to expose this website as open source so others can contribute.

## Disclaimer

While the REST API is production ready, the website (policyguru.io) is mostly a proof of concept. We would like to welcome contributions from anyone to improve the website.