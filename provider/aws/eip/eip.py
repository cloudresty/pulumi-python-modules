import  pulumi, yaml

from    sys             import path
from    os              import getenv
from    pulumi_aws      import ec2      as net

path.append(getenv('IAC__PROJECT_MODULES_CONFIG'))

from    parse.yaml      import YAMLParse

# General variables
resource_type       = "eip"
resource_project    = getenv('IAC__PROJECT_ID')
eips_dict           = {}

class ExecuteElasticIPConf:

    def __init__(self):

        resource_specs  = YAMLParse(resource_type).getSpecs()

        for eip_name, eip_configuration in resource_specs.items():

            # AWS Elastic IP Dynamic Variables
            resource_name   = eip_name

            eip             = net.Eip(

                resource_name,
                tags = {
                    "Name": resource_name
                }

            )

            eips_dict.update({eip._name: eip.id})

            # Exporting each Elasticache Subnet Group created for future reference
            pulumi.export(resource_name, eip.id)

    @classmethod
    def getEIP(cls):

        return eips_dict