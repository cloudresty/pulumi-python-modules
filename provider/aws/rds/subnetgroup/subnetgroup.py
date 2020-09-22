import  pulumi, yaml

from    sys             import path
from    os              import getenv
from    pulumi_aws      import rds          as rds

path.append(getenv('IAC__PROJECT_MODULES_CONFIG'))

from    parse.yaml      import YAMLParse
from    subnet.subnet   import ExecuteSubnetConf    as aws_subnet

# General variables
resource_type       = "rds"
resource_project    = getenv('IAC__PROJECT_ID')
subnetgroups_dict   = {}

class ExecuteRDSSubnetGroupConf:

    def __init__(self):

        resource_specs  = YAMLParse(resource_type).getSpecs()
        aws_subnet_id   = aws_subnet.getSubnet()

        for subnetgroup_name, subnetgroup_configuration in resource_specs["subnet-group"].items():

            # AWS Elasticache Subnet Group Dynamic Variables
            resource_name           = subnetgroup_name
            resource_description    = subnetgroup_configuration["description"]
            resource_subnet_ids     = subnetgroup_configuration["subnets"]
            resource_subnets_list   = []

            for each_subnet_found in resource_subnet_ids:
                resource_subnets_list.append(aws_subnet_id[str(each_subnet_found)])

            subnetgroup                 = rds.SubnetGroup(

                resource_name,
                description             = resource_description,
                subnet_ids              = resource_subnets_list

            )

            subnetgroups_dict.update({subnetgroup._name: subnetgroup.id})

            # Exporting each Elasticache Subnet Group created for future reference
            # pulumi.export(resource_id, subnetgroup.id)

    @classmethod
    def getSubnetGroup(cls):

        return subnetgroups_dict