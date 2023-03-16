## Troposphering

This repo contains a brief introduction to [Troposphere](https://github.com/cloudtools/troposphere), a Python library to create and manage CloudFormation descriptors (templates).

For more info, please check out the [blog article]() I wrote.

# Requirements

As a suggestion, use a [virtualenv](https://docs.python.org/3/library/venv.html) to avoid messing around local Python installations/dependencies.

- troposphere
  ```bash
  pip install troposphere
  ```

# Quick start

There are two different scripts (in their folders):
- `subnets/subnets.py`
  This will create a template `subnets_template.yaml` defining a (set of) subnets defined in an input `subnets_input.json`.

- `instances/instances.py`
  This one creates a template `instances_template.yaml` defining an (set of) instance and security group(s) defined in an input `instances_input.json`.
  
The second script (`instances`) is dependant on the first one, as it will use the subnets declared/created in the prior stack.

First, modify each `_input` file and add your current AWS account values, such as:
- VPC ID.
- Region.
- Resource name(s).
- (optional) Common tags to add.

Once done, change the name to be `<script_name>_input.json`.

Now you are ready to go.

```bash
cd subnets/
python3 subnets.py
```

It will create a template (YAML) file called `subnets_template.yaml` where you can check all resources being defined.

This template then can be used as file input for a CloudFormation stack creation, as so:
```bash
aws cloudformation create-stack --stack-name AddingSubnetsWithTroposphere --template-body file://subnets_template.yaml
```

Same within `instances/` to create the second stack.

**These scripts are guidelines with basic features that can be extended with both Python blessings and CloudFormation flexibility.**
E.g. one could define a map of regions vs availabilityZones or AMIs per region, etc, to be used later on when creating the instance(s).

# Next step(s)
- Automate CFN stack creation.