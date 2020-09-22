import  pulumi, yaml

from    sys         import path
from    os          import getenv
from    pulumi_aws  import ec2      as net

path.append(getenv('IAC__PROJECT_MODULES_CONFIG'))

from    parse.yaml  import YAMLParse

# General variables
resource_type       = "vpc"
resource_project    = getenv('IAC__PROJECT_ID')
vpcs_dict           = {}

class ExecuteVPCConf:

    def __init__(self):

        self.resource_specs = YAMLParse(resource_type).getSpecs()


    def createVpc(self):

        for vpc_name, vpc_conf in self.resource_specs.items():

            # AWS VPC Dynamic Variables
            resource_name           = vpc_name
            resource_environment    = vpc_conf['namespace']
            resource_region         = vpc_conf['region']
            resource_cidr           = vpc_conf['cidr']
            resource_dns_resolution = vpc_conf['dns-resolution']
            resource_dns_hostnames  = vpc_conf['dns-hostnames']
            resource_id             = resource_project + "/" + resource_environment + "/" + resource_type + "/" + resource_name

            # Create VPCs
            vpc = net.Vpc(

                resource_name,
                cidr_block              = resource_cidr,
                enable_dns_support      = resource_dns_resolution,
                enable_dns_hostnames    = resource_dns_hostnames,
                tags                    = {

                    "Environment"       : resource_environment,
                    "Name"              : resource_name,
                    "ManagedBy"         : "Ascential",
                    "ManagedWith"       : "Pulumi",
                    "PulumiResourceId"  : resource_id,
                    "PulumiProject"     : pulumi.get_project(),
                    "PulumiStack"       : pulumi.get_stack()

                }

            )

            vpcs_dict.update({vpc._name: vpc.id})

            # Export the name of each VPC
            pulumi.export(resource_id, vpc.id)


    @classmethod
    def getVpc(cls):

        # # DEBUG CODE
        # for each_vpc_name, each_vpc_id in vpcs_dict.items():
        #     print("DEBUG | AWS VPC - Sent > Key:", each_vpc_name, "/ Value:", each_vpc_id)

        return vpcs_dict