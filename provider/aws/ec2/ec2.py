import  pulumi, yaml

from    sys         import path
from    os          import getenv
from    pulumi_aws  import ec2

path.append(getenv('IAC__PROJECT_MODULES_CONFIG'))

from    parse.yaml                  import YAMLParse
from    subnet.subnet               import ExecuteSubnetConf        as aws_subnet
from    securitygroup.securitygroup import ExecuteSecurityGroupConf as aws_sg
from    keypair.keypair             import ExecuteKeyPairConf       as aws_keypair

# General variables
resource_type       = "ec2"
resource_project    = getenv('IAC__PROJECT_ID')
ec2s_dict           = {}

class ExecuteEC2Conf:

    def __init__(self):

        resource_specs  = YAMLParse(resource_type).getSpecs()
        aws_subnet_id   = aws_subnet.getSubnet()
        aws_sg_id       = aws_sg.getSecurityGroup()
        aws_keypair_id  = aws_keypair.getKeyPair()

        for ec2_instance_name, ec2_instance_configuration in resource_specs.items():

            # AWS EC2 Dynamic Variables
            resource_name                   = ec2_instance_name
            resource_number_of_instances    = ec2_instance_configuration["number_of_instances"]
            resource_namespace              = ec2_instance_configuration["namespace"]
            resource_environment            = ec2_instance_configuration["environment"]
            resource_ami                    = ec2_instance_configuration["ami"]
            resource_instance_type          = ec2_instance_configuration["instance_type"]
            resource_subnet                 = ec2_instance_configuration["subnet"]
            resource_security_groups        = ec2_instance_configuration["security_groups"]
            resource_public_ipv4_address    = ec2_instance_configuration["public_ipv4_address"]
            resource_keypair                = ec2_instance_configuration["ssh_key"]
            resource_user_data              = ec2_instance_configuration["user_data"]

            this_subnet                     = aws_subnet_id[str(resource_subnet)]
            this_keypair                    = aws_keypair_id[str(resource_keypair)]

            security_groups_list            = []

            for each_security_group_found in resource_security_groups:

                this_security_group = aws_sg_id[str(each_security_group_found)]
                security_groups_list.append(this_security_group)

            for number_of_instances in range (1, int(resource_number_of_instances)+1):

                if resource_number_of_instances > 1:
                    resource_final_name = (resource_name+str("-" + str(number_of_instances)).zfill(4))
                else:
                    resource_final_name = resource_name

                resource_id                     = resource_project + "/" + resource_namespace + "/" + resource_environment + "/" + resource_type + "/" + resource_final_name

                # Create EC2
                ec2_instance                    = ec2.Instance(

                    resource_final_name,
                    ami                         = resource_ami,
                    instance_type               = resource_instance_type,
                    associate_public_ip_address = resource_public_ipv4_address,
                    subnet_id                   = this_subnet,
                    # vpc_security_group_ids      = [this_security_group],
                    vpc_security_group_ids      = security_groups_list,

                    # FIXME:
                    # Need to look into this just in case we'd like
                    # to use manual internal IP address allocation
                    # instead of DHCP.
                    # private_ip                  = ec2_instance_configuration["private_ipv4_address"],

                    key_name                    = this_keypair,
                    root_block_device           = {
                        "volume_type" : "gp2",
                        "volume_size" : "20"
                    },
                    user_data                   = resource_user_data,
                    tags                        = {

                        "Environment"       : resource_environment,
                        "Name"              : resource_final_name,
                        "ManagedBy"         : "Ascential",
                        "ManagedWith"       : "Pulumi",
                        "PulumiResourceId"  : resource_id,
                        "PulumiProject"     : pulumi.get_project(),
                        "PulumiStack"       : pulumi.get_stack()

                    }

                )

                ec2s_dict.update({ec2_instance._name: ec2_instance.id})

                # Export the name of each EC2 Instance
                pulumi.export(resource_id, ec2_instance.id)

    @classmethod
    def getEc2(cls):

        return ec2s_dict