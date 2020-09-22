import  pulumi, yaml

from    sys         import path
from    os          import getenv
from    pulumi_aws  import s3

path.append(getenv('IAC__PROJECT_MODULES_CONFIG'))

from    parse.yaml  import YAMLParse

# General variables
resource_type       = "s3"
resource_project    = getenv('IAC__PROJECT_ID')

class ExecuteS3Conf:

    def __init__(self):

        resource_specs = YAMLParse(resource_type).getSpecs()

        for s3_bucket_name, s3_bucket_configuration in resource_specs.items():

            # AWS S3 Dynamic Variables
            resource_name           = s3_bucket_name
            resource_namespace      = s3_bucket_configuration["namespace"]
            resource_environment    = s3_bucket_configuration["environment"]
            resource_id             = resource_project + "/" + resource_namespace + "/" + resource_environment + "/" + resource_type + "/" + resource_name

            # Create S3s
            bucket                  = s3.Bucket(

                resource_name,
                acl             = s3_bucket_configuration["acl"],
                force_destroy   = s3_bucket_configuration["force-destroy"],
                tags            = {

                    "Environment"       : resource_environment,
                    "Name"              : resource_name,
                    "ManagedBy"         : "Ascential",
                    "ManagedWith"       : "Pulumi",
                    "PulumiResourceId"  : resource_id,
                    "PulumiProject"     : pulumi.get_project(),
                    "PulumiStack"       : pulumi.get_stack()

                }

            )

            # Export the name of each S3 bucket for Peoplepoint
            pulumi.export(resource_id, bucket.id)