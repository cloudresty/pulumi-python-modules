import  pulumi, yaml

from    sys         import path
from    os          import getenv
from    pulumi_aws  import ec2              as net

path.append(getenv('IAC__PROJECT_MODULES_CONFIG'))

from    parse.yaml  import YAMLParse
from    vpc.vpc     import ExecuteVPCConf   as aws_vpc

# General variables
resource_type       = "subnet"
resource_project    = getenv('IAC__PROJECT_ID')
subnets_dict        = {}

class ExecuteSubnetConf:

    def __init__(self):

        resource_specs  = YAMLParse(resource_type).getSpecs()
        aws_vpc_id      = aws_vpc.getVpc()

        # DEBUG CODE
        # for each_individual_vpc_key, each_individual_vpc_value in aws_vpc_id.items():
        #     print("DEBUG | AWS SUBNET - Received > Key:" , str(each_individual_vpc_key), "/ Value:", str(each_individual_vpc_value))

        for subnet_name, subnet_configuration in resource_specs.items():

            # AWS Subnet Dynamic Variables
            resource_name               = subnet_name
            resource_namespace          = subnet_configuration['namespace']
            resource_az                 = subnet_configuration['az']
            resource_cidr               = subnet_configuration['cidr']
            resource_assign_public_ipv4 = subnet_configuration['assign-public-ipv4']
            resource_vpc                = subnet_configuration['vpc']

            this_vpc    = aws_vpc_id[str(resource_vpc)]

            resource_id = resource_project + "/" + resource_namespace + "/" + resource_type + "/" + resource_name
            subnet      = net.Subnet(

                resource_name,
                vpc_id                      = this_vpc,
                cidr_block                  = resource_cidr,
                map_public_ip_on_launch     = resource_assign_public_ipv4,
                availability_zone           = resource_az,
                tags                        = {

                    "Environment"       : resource_namespace,
                    "Name"              : resource_name,
                    "ManagedBy"         : "Ascential",
                    "ManagedWith"       : "Pulumi",
                    "PulumiResourceId"  : resource_id,
                    "PulumiProject"     : pulumi.get_project(),
                    "PulumiStack"       : pulumi.get_stack()

                },

                # opts = pulumi.ResourceOptions(depends_on=[this_vpc], parent=this_vpc)
                # opts = pulumi.ResourceOptions(parent=aws_vpc)

            )

            subnets_dict.update({subnet._name: subnet.id})

            # Exporting each subnet created for future reference
            pulumi.export(resource_id, subnet.id)

    @classmethod
    def getSubnet(cls):

        return subnets_dict