import  pulumi, yaml

from    sys         import path
from    os          import getenv
from    pulumi_aws  import iam

path.append(getenv('IAC__PROJECT_MODULES_CONFIG'))

from    parse.yaml  import YAMLParse

# General variables
resource_type       = "iam"
resource_project    = getenv('IAC__PROJECT_ID')

class ExecuteIAMUsersConf:

    def __init__(self):

        resource_specs = YAMLParse(resource_type).getSpecs()

        for iam_user_name, iam_user_configuration in resource_specs["user"].items():

            # IAM User Dynamic Variables
            resource_name           = iam_user_name
            resource_namespace      = iam_user_configuration["namespace"]
            resource_environment    = iam_user_configuration["environment"]
            resource_id             = resource_project + "/" + resource_namespace + "/" + resource_environment + "/" + resource_type + "/user/" + resource_name

            # Resetting all optional variables
            # with the default value None
            resource_user_environment       = \
            resource_user_namespace         = \
            resource_user_path              = \
            resource_user_console_access    = \
            resource_user_access_keys       = \
            resource_user_inline_policy     = \
            resource_user_iam_policy        = \
            resource_user_tag               = None

            # Cheking the documents content, if present
            # we will be assigning their values to our variables,
            # otherwise we'll set them to None
            resource_user_environment       = iam_user_configuration["environment"]     if "environment"    in iam_user_configuration else None
            resource_user_namespace         = iam_user_configuration["namespace"]       if "namespace"      in iam_user_configuration else None
            resource_user_path              = iam_user_configuration["path"]            if "path"           in iam_user_configuration else None
            resource_user_console_access    = iam_user_configuration["console-access"]  if "console-access" in iam_user_configuration else None
            resource_user_access_keys       = iam_user_configuration["access-keys"]     if "access-keys"    in iam_user_configuration else None
            resource_user_inline_policy     = iam_user_configuration["user-policies"]   if "user-policies"  in iam_user_configuration else None
            resource_user_iam_policy        = iam_user_configuration["iam-policies"]    if "iam-policies"   in iam_user_configuration else None
            resource_user_tags              = iam_user_configuration["tags"]            if "tags"           in iam_user_configuration else None


            # Create IAM User
            iam_user = iam.User(

                resource_name,
                path        = resource_user_path,
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

            pulumi.export(
                resource_name,
                (
                    iam_user.id,
                    iam_user.arn,
                    iam_user.unique_id
                )
            )

            # Create Inline User Policy
            if resource_user_inline_policy is not None:

                for resource_user_inline_policy_key, resource_user_inline_policy_value in resource_user_inline_policy.items():

                    user_policy = iam.UserPolicy(

                        resource_user_inline_policy_key,
                        user    = iam_user.name,
                        policy  = resource_user_inline_policy_value

                    )

            # Create CLI / Programmatic Access Key
            if resource_user_access_keys is not None:

                for resource_user_access_keys_key in resource_user_access_keys:

                    # print(resource_user_access_keys_key)

                    user_access_key = iam.AccessKey(

                        resource_user_access_keys_key,
                        user = iam_user.name

                        )

                    #
                    # WARNING
                    #
                    # pulumi.export(resource_user_access_keys_key, user_access_key.encrypted_secret)
                    pulumi.export(

                        resource_user_access_keys_key,
                        (
                            user_access_key.id,
                            user_access_key.secret
                        )
                    )