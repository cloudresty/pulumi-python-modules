import  pulumi, yaml

from    sys         import path
from    os          import getenv
from    pulumi_aws  import elasticache

path.append(getenv('IAC__PROJECT_MODULES_CONFIG'))

from    parse.yaml                          import YAMLParse
from    elasticache.subnetgroup.subnetgroup import ExecuteElasticacheSubnetGroupConf    as aws_elasticache_subnet_group
from    securitygroup.securitygroup         import ExecuteSecurityGroupConf             as aws_sg

# General variables
resource_type       = "elasticache"
resource_project    = getenv('IAC__PROJECT_ID')

class ExecuteElasticacheRedisConf:

    def __init__(self):

        resource_specs                  = YAMLParse(resource_type).getSpecs()
        aws_elasticache_subnet_group_id = aws_elasticache_subnet_group.getSubnetGroup()
        aws_sg_id                       = aws_sg.getSecurityGroup()

        for elasticache_redis_name, elasticache_redis_configuration in resource_specs["redis"].items():

            # AWS EC2 Dynamic Variables
            resource_specific_type          = "redis"
            resource_name                   = elasticache_redis_name
            resource_number_of_nodes        = elasticache_redis_configuration["number_of_nodes"]
            resource_node_type              = elasticache_redis_configuration["node_type"]
            resource_engine_version         = elasticache_redis_configuration["engine_version"]
            resource_port                   = elasticache_redis_configuration["port"]
            resource_subnet_group           = elasticache_redis_configuration["subnet_group"]
            resource_parameter_group        = elasticache_redis_configuration["parameter_group"]
            resource_security_groups        = elasticache_redis_configuration["security_groups"]
            resource_security_groups_list   = []

            this_subnet_group               = aws_elasticache_subnet_group_id[str(resource_subnet_group)]

            for each_security_group_found in resource_security_groups:
                resource_security_groups_list.append(aws_sg_id[str(each_security_group_found)])
            # this_security_group         = aws_sg_id[str(resource_security_groups)]

            redis = elasticache.Cluster(

                resource_name,
                engine                  = resource_specific_type,
                num_cache_nodes         = resource_number_of_nodes,
                node_type               = resource_node_type,
                engine_version          = resource_engine_version,
                port                    = resource_port,
                subnet_group_name       = this_subnet_group,
                parameter_group_name    = resource_parameter_group,
                security_group_ids      = resource_security_groups_list

                )