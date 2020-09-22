import  pulumi, yaml

from    sys         import path
from    os          import getenv
from    pulumi_aws  import lb

path.append(getenv('IAC__PROJECT_MODULES_CONFIG'))

from    parse.yaml  import YAMLParse
from    vpc.vpc     import ExecuteVPCConf   as aws_vpc
from    ec2.ec2     import ExecuteEC2Conf   as aws_ec2

# General variables
resource_type       = "lb"
resource_project    = getenv('IAC__PROJECT_ID')
tgs_dict            = {}

class ExecuteTargetGroupConf:

    def __init__(self):

        resource_specs  = YAMLParse(resource_type).getSpecs()
        aws_vpc_id      = aws_vpc.getVpc()
        aws_ec2_id      = aws_ec2.getEc2()

        for target_group_name, target_group_configuration in resource_specs["targetgroup"].items():

            # AWS Target Group Dynamic Variables
            resource_name       = target_group_name
            resource_port       = target_group_configuration["port"]
            resource_protocol   = target_group_configuration["protocol"]
            resource_vpc        = target_group_configuration["vpc"]


            this_vpc                        = aws_vpc_id[str(resource_vpc)]

            # resource_id                     = resource_project + "/" + resource_namespace + "/" + resource_environment + "/" + resource_type + "/" + resource_name

            # Create Instance Target Group
            targe_group                    = lb.TargetGroup(

                resource_name,
                name        = resource_name,
                port        = resource_port,
                protocol    = resource_protocol,
                vpc_id      = this_vpc,
                tags        = {

                    # "Environment"       : resource_environment,
                    "Name"              : resource_name,
                    "ManagedBy"         : "Ascential",
                    "ManagedWith"       : "Pulumi",
                    # "PulumiResourceId"  : resource_id,
                    "PulumiProject"     : pulumi.get_project(),
                    "PulumiStack"       : pulumi.get_stack()

                }

            )

            tgs_dict.update({targe_group._name: targe_group.id})

            # Export the name of each Instance Target Group
            pulumi.export(resource_name, targe_group.id)

            tgat_index = 0
            for each_tg_instance in target_group_configuration["instances"]:

                tgat_index = tgat_index + 1

                this_ec2                = aws_ec2_id[str(each_tg_instance)]

                target_group_attachment = lb.TargetGroupAttachment(

                    (resource_name + "-at-" + str(tgat_index)),
                    target_group_arn    = targe_group.arn,
                    target_id           = this_ec2,
                    port                = 80

                )

    @classmethod
    def getTargetGroup(cls):

        return tgs_dict