import  pulumi, yaml

from    sys         import path
from    os          import getenv
from    pulumi_aws  import rds

path.append(getenv('IAC__PROJECT_MODULES_CONFIG'))

from    parse.yaml                  import YAMLParse
from    rds.subnetgroup.subnetgroup import ExecuteRDSSubnetGroupConf    as aws_rds_subnet_group
from    securitygroup.securitygroup import ExecuteSecurityGroupConf     as aws_sg

# General variables
resource_type       = "rds"
resource_project    = getenv('IAC__PROJECT_ID')

class ExecuteRDSAuroraConf:

    def __init__(self):

        resource_specs          = YAMLParse(resource_type).getSpecs()
        aws_rds_subnet_group_id = aws_rds_subnet_group.getSubnetGroup()
        aws_sg_id               = aws_sg.getSecurityGroup()

        # for rds_aurora_name, rds_aurora_configuration in resource_specs["aurora"].items():

        #     # AWS RDS Aurora Dynamic Variables
        #     resource_specific_type          = "aurora"
        #     resource_name                   = rds_aurora_name

        #     print(rds_aurora_name)

        #     if rds_aurora_configuration["setup_type"] == "instance":

        #         resource_instance_type          = rds_aurora_configuration["instance_type"]
        #         resource_engine                 = rds_aurora_configuration["engine"]
        #         resource_engine_version         = rds_aurora_configuration["engine_version"]
        #         resource_allocated_storage      = rds_aurora_configuration["allocated_storage"]
        #         resource_storage_type           = rds_aurora_configuration["storage_type"]
        #         resource_subnet_group           = rds_aurora_configuration["subnet_group"]
        #         resource_parameter_group        = rds_aurora_configuration["parameter_group"]
        #         resource_security_groups        = rds_aurora_configuration["security_groups"]
        #         resource_database_name          = rds_aurora_configuration["database_name"]
        #         resource_username               = rds_aurora_configuration["username"]
        #         resource_password               = rds_aurora_configuration["password"]
        #         resource_security_groups_list   = []

        #         this_subnet_group               = aws_rds_subnet_group_id[str(resource_subnet_group)]

        #         for each_security_group_found in resource_security_groups:
        #             resource_security_groups_list.append(aws_sg_id[str(each_security_group_found)])

                # aurora = rds.Cluster(

                #     resource_name,
                #     instance_class          = resource_instance_type,
                #     engine                  = resource_engine,
                #     engine_version          = resource_engine_version,
                #     allocated_storage       = resource_allocated_storage,
                #     # storage_type            = resource_storage_type,
                #     db_subnet_group_name    = this_subnet_group,
                #     parameter_group_name    = resource_parameter_group,
                #     vpc_security_group_ids  = resource_security_groups_list,
                #     name                    = resource_database_name,
                #     username                = resource_username,
                #     password                = resource_password

                #     )

            # elif rds_aurora_configuration["setup_type"] == "cluster":

            #     print(rds_aurora_configuration["setup_type"])

            # else:

            #     print("Couldn't identify the setup type from your RDS YAML configration file")
            #     print("This should be being 'instance' or 'cluster'.")

        # default = rds.Cluster(
        #     "default",
        #     cluster_identifier="main-production-rds-aurora",
        #         availability_zones=[
        #             "eu-west-2a",
        #             "eu-west-2b",
        #             "eu-west-2c",
        #         ],
        #         database_name="mydb",
        #         master_username="foo",
        #         master_password="barbut8chars",
        #         final_snapshot_identifier = "lastsnapshot"
        # )

        # instances_count = range(0)
        # cluster_instances = []

        # for n in instances_count:

        #     cluster_instances.append(

        #         rds.ClusterInstance(

        #             f"clusterInstances-{n+1}",
        #             identifier=f"main-production-rds-aurora-{n+1}",
        #             cluster_identifier=default.id,
        #             instance_class="db.t3.medium",
        #             engine=default.engine,
        #             engine_version=default.engine_version,
        #             apply_immediately = True

        #         )

        #     )