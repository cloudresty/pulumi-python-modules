import  pulumi, yaml

from    sys         import path
from    os          import getenv
from    pulumi_aws  import lb

path.append(getenv('IAC__PROJECT_MODULES_CONFIG'))

from    parse.yaml                          import YAMLParse
from    subnet.subnet                       import ExecuteSubnetConf            as aws_subnet
from    securitygroup.securitygroup         import ExecuteSecurityGroupConf     as aws_sg

# General variables
resource_type       = "lb"
resource_project    = getenv('IAC__PROJECT_ID')

class ExecuteALBConf:

    def __init__(self):

        resource_specs  = YAMLParse(resource_type).getSpecs()
        aws_subnet_id   = aws_subnet.getSubnet()
        aws_sg_id       = aws_sg.getSecurityGroup()

        for alb_name, alb_configuration in resource_specs["alb"].items():

            # AWS ALB Dynamic Variables
            resource_specific_type          = "alb"
            resource_name                   = alb_name
            resource_subnets                = alb_configuration["subnets"]
            resource_security_groups        = alb_configuration["security_groups"]

            resource_subnets_list = []
            for each_subnet_found in resource_subnets:
                resource_subnets_list.append(aws_subnet_id[str(each_subnet_found)])

            resource_security_groups_list = []
            for each_security_group_found in resource_security_groups:
                resource_security_groups_list.append(aws_sg_id[str(each_security_group_found)])

            # FIXME:
            # This needs to be reviewed as currently the subnets
            # are being added in a non-dynamic fashion
            alb = lb.LoadBalancer(

                resource_name,
                load_balancer_type  = "application",
                name                = resource_name,
                # subnet_mappings     = this_final_list,
                subnet_mappings=[
                    lb.LoadBalancerSubnetMappingArgs(
                        subnet_id       = resource_subnets_list[0],
                    ),
                    lb.LoadBalancerSubnetMappingArgs(
                        subnet_id       = resource_subnets_list[1],
                    ),
                    lb.LoadBalancerSubnetMappingArgs(
                        subnet_id       = resource_subnets_list[2],
                    ),
                ],
                security_groups     = resource_security_groups_list

                )