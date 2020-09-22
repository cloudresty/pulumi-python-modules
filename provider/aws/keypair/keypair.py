import  pulumi, yaml

from    sys         import path
from    os          import getenv
from    pulumi_aws  import ec2              as am

path.append(getenv('IAC__PROJECT_MODULES_CONFIG'))

from    parse.yaml  import YAMLParse

# General variables
resource_type       = "keypair"
resource_project    = getenv('IAC__PROJECT_ID')
keypairs_dict       = {}

class ExecuteKeyPairConf:

    def __init__(self):

        resource_specs  = YAMLParse(resource_type).getSpecs()

        for keypair_name, keypair_configuration in resource_specs.items():

            # AWS KeyPair Dynamic Variables
            resource_name               = keypair_name
            # resource_namespace          = subnet_configuration['namespace']
            # resource_az                 = subnet_configuration['az']
            resource_public_key         = keypair_configuration['public_key']

            # resource_id = resource_project + "/" + resource_namespace + "/" + resource_type + "/" + resource_name
            keypair                     = am.KeyPair(

                resource_name,
                public_key              = resource_public_key,
                tags                    = {

                    # "Environment"       : resource_namespace,
                    "Name"              : resource_name,
                    "ManagedBy"         : "Ascential",
                    "ManagedWith"       : "Pulumi",
                    # "PulumiResourceId"  : resource_id,
                    "PulumiProject"     : pulumi.get_project(),
                    "PulumiStack"       : pulumi.get_stack()

                },

                # opts = pulumi.ResourceOptions(depends_on=[this_vpc], parent=this_vpc)
                # opts = pulumi.ResourceOptions(parent=aws_vpc)

            )

            keypairs_dict.update({keypair._name: keypair.id})

            # Exporting each KeyPair created for future reference
            # pulumi.export(resource_id, keypair.id)

    @classmethod
    def getKeyPair(cls):

        return keypairs_dict