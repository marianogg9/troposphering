# This script creates a CloudFormation template (YAML) defining a (set of) security groups and instances in a given input VPC, dependant on 'subnets' CFN stack.
# It expects a json file as input (instances_input.json) with initial values.
# This script was created by me as an example Troposphere implementation.
# More examples: https://github.com/cloudtools/troposphere/tree/main/examples.

import json

from troposphere.ec2 import SecurityGroup, SecurityGroupRule, Instance
from troposphere import ImportValue, Template, Ref, Output, GetAtt

t = Template()                                                                  # Define output template.

with open('instances_input.json','r') as i:                                     # Read input value file.
    data = json.load(i)

## Security Group(s)
for sg in data['security_groups']:
    security_group = SecurityGroup(
        sg['name'],
        GroupDescription=sg['description'],
        VpcId=data['vpc_id'],
        SecurityGroupIngress=[ 
            SecurityGroupRule(
                IpProtocol='tcp',
                FromPort=rule['ports']['from'],
                ToPort=rule['ports']['to'],
                CidrIp=rule['cidr']
            ) for rule in sg['rules']['ingress']
        ],
        SecurityGroupEgress=[
            SecurityGroupRule(
                IpProtocol='tcp',
                FromPort=rule['ports']['from'],
                ToPort=rule['ports']['to'],
                CidrIp=rule['cidr']
            ) for rule in sg['rules']['egress']
        ],
        Tags=[
            {
                "Key": "Name",
                "Value": sg['name']
            }
        ] + [tag for tag in data['common_tags']]    
    )
    t.add_resource(security_group)

## Instance(s)
for i in data['instances']:                                                     # Loop over the instances values definition.
    instance = Instance(                                                        # Define each instance.
        i['name'],
        ImageId=data['ami_id'],
        InstanceType=data['instance_type'],
        SubnetId=ImportValue(
            data['subnets_stack'] + '-' + (data['region']).replace('-','') + i['availability-zone']
        ),
        SecurityGroupIds=[Ref(security_group)],
        KeyName=data['ec2keypair'],
        Tags=[                                                                  # Let's combine "local" specific tags
            {
                "Key": "Name",
                "Value": i['name']
            }
        ] + [tag for tag in data['common_tags']]                                # with global ones.
    )
    t.add_resource(instance)
    
    t.add_output(                                                               # Add some output values.
        [
            Output(
                i['name']+'InstanceID',
                Value=Ref(instance)
            ),
            Output(
                i['name']+'PrivateIP',
                Value=GetAtt(i['name'],'PrivateIp')
            )
        ]
    )

## Write out the YAML template
with open('instances_template.yaml', 'w') as f:                                 # Lastly, create the output template file.
    f.write(t.to_yaml())