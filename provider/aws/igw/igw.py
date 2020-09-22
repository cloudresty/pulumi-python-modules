import  pulumi, yaml

from    sys             import path
from    os              import getenv
from    pulumi_aws      import ec2      as igw

path.append(getenv('IAC__PROJECT_MODULES_CONFIG'))

from    parse.yaml      import YAMLParse
from    vpc.vpc         import ExecuteVPCConf       as aws_vpc

# General variables
resource_type       = "igw"
resource_project    = getenv('IAC__PROJECT_ID')

class ExecuteIGWConf:

    def __init__(self):

        resource_specs  = YAMLParse(resource_type).getSpecs()
        aws_vpc_id      = aws_vpc.getVpc()

        for igw_name, igw_configuration in resource_specs.items():

            # AWS Internet Gateway Variables
            resource_name           = igw_name
            resource_namespace      = igw_configuration["namespace"]
            resource_environment    = igw_configuration["environment"]
            resource_vpc            = igw_configuration["vpc"]

            this_vpc                = aws_vpc_id[str(resource_vpc)]

            resource_id             = resource_project + "/" + resource_namespace + "/" + resource_environment + "/" + resource_type + "/" + resource_name

            aws_igw     = igw.InternetGateway(

                resource_name,
                vpc_id  = this_vpc,
                tags    = {

                    "Name"              : resource_name,
                    "ManagedBy"         : "Ascential",
                    "ManagedWith"       : "Pulumi",
                    "PulumiResourceId"  : resource_id,
                    "PulumiProject"     : pulumi.get_project(),
                    "PulumiStack"       : pulumi.get_stack()

                }

            )

            # Export the name of each Internet Gateway
            pulumi.export(resource_id, aws_igw.id)