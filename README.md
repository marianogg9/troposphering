## Troposphering

This repo contains a brief introduction to [Troposphere](https://github.com/cloudtools/troposphere), a Python library to create and manage CloudFormation descriptors (templates).

For more info, please check out the [blog article]() I wrote.

# Requirements

As a suggestion, use a [virtualenv]() to avoid messing around local Python installations/dependencies.

- troposphere
  ```bash
  pip install troposphere
  ```

# Quick start

Modify template `subnets_input` file and add your current AWS account values:
- VPC ID.
- Subnet(s) ID.
- Subnet(s) name(s).
- Region.
- (optional) Common tags to add.

Once done, change its name to be `subnets_input.json`.

Now it's ready to be run.

```bash
python3 subnets.py
```

It will create a template (YAML) file called `subnets_template.yaml` where you can check all resources being defined.

This template then can be used as file input for a CloudFormation stack creation, as so:
```bash
aws cloudformation create-stack --stack-name AddingSubnetsWithTroposphere --template-body file://subnets_template.yaml
```

# Next steps
- Automate CFN stack creation.