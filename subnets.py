# This script creates a CloudFormation template (YAML) defining a set of subnets in a given input VPC.
# It expects a json file as input (subnets_input.json) with initial values.
# This script was created by me as an example Troposphere implementation.

import json

from troposphere import ec2
from troposphere import Ref, Sub, Export
from troposphere import Template, Output

t = Template()                                                  # Define output template.

with open('subnets_input.json','r') as s:                       # Read input value file.
    data = json.load(s)

for s in data['subnets']:                                       # Loop over the subnets values definition.
    region = data['region']
    availabilityZone = s['availability-zone']
    name = 'Subnet'+region+availabilityZone
    subnet = ec2.Subnet(                                        # Define each subnet.
        name.replace('-',''),
        AvailabilityZone=s['availability-zone'],
        CidrBlock=s['cidr'],
        VpcId=data['vpcid'],
        Tags=[                                                  # Let's combine "local" specific tags
            {
                "Key": "Name", 
                "Value": 'subnet-'+data['region']+s['availability-zone']
            }
        ] + [tag for tag in data['common_tags']]                # with global ones.
    )
    t.add_resource(subnet)

    output = Output(                                            # Add outputs
        name.replace('-',''),
        Value=Ref(subnet),
        Export=Export(Sub("${AWS::StackName}-" + subnet.title)) # and export values.
    )
    
    t.add_output(output)

with open('subnets_template.yaml', 'w') as f:                   # Lastly, create the output template file.
    f.write(t.to_yaml())