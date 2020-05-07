from aws_cdk import core
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_dynamodb as _ddb
from aws_cdk import aws_apigateway as _ag


class SaCdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create DynamoDB
        ddb_table = _ddb.Table(self,
                               id='sa-table-cms',
                               table_name='sa_table_cms',
                               partition_key=_ddb.Attribute(
                                   name='ID', type=_ddb.AttributeType.STRING))

        # Permissions
        lambda_role = _iam.Role(
            self,
            id='sa-cms-role',
            assumed_by=_iam.ServicePrincipal('lambda.amazonaws.com'))

        # WARNING: This is an example on how to include AWS managed policy. Don't use this for production. Please use the example of policy document for DynamoDB instead.
        lambda_role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'CloudWatchLogsFullAccess'))

        policy_statement = _iam.PolicyStatement(effect=_iam.Effect.ALLOW)
        policy_statement.add_actions("dynamodb:*")
        policy_statement.add_resources(ddb_table.table_arn)
        lambda_role.add_to_policy(policy_statement)

        # Create Lambda Functions
        fn_lambda_create_post = _lambda.Function(
            self,
            "sa-cms-createPost",
            code=_lambda.AssetCode("../sa-lambda/create-post/"),
            handler="app.lambda_handler",
            tracing=_lambda.Tracing.ACTIVE,
            timeout=core.Duration.seconds(30),
            role=lambda_role,
            runtime=_lambda.Runtime.PYTHON_3_8)

        fn_lambda_list_post = _lambda.Function(
            self,
            "sa-cms-listPost",
            code=_lambda.AssetCode("../sa-lambda/list-post/"),
            handler="app.lambda_handler",
            tracing=_lambda.Tracing.ACTIVE,
            timeout=core.Duration.seconds(30),
            role=lambda_role,
            runtime=_lambda.Runtime.PYTHON_3_8)

        fn_lambda_get_post = _lambda.Function(
            self,
            "sa-cms-getPost",
            code=_lambda.AssetCode("../sa-lambda/get-post/"),
            handler="app.lambda_handler",
            tracing=_lambda.Tracing.ACTIVE,
            timeout=core.Duration.seconds(30),
            role=lambda_role,
            runtime=_lambda.Runtime.PYTHON_3_8)

        fn_lambda_delete_post = _lambda.Function(
            self,
            "sa-cms-deletePost",
            code=_lambda.AssetCode("../sa-lambda/delete-post/"),
            handler="app.lambda_handler",
            timeout=core.Duration.seconds(30),
            tracing=_lambda.Tracing.ACTIVE,
            role=lambda_role,
            runtime=_lambda.Runtime.PYTHON_3_8)

        fn_lambda_create_post.add_environment("DYNAMODB_TABLE",
                                              ddb_table.table_name)
        fn_lambda_get_post.add_environment("DYNAMODB_TABLE",
                                           ddb_table.table_name)
        fn_lambda_list_post.add_environment("DYNAMODB_TABLE",
                                            ddb_table.table_name)
        fn_lambda_delete_post.add_environment("DYNAMODB_TABLE",
                                              ddb_table.table_name)

        api = _ag.RestApi(
            self,
            id='sa-api-gateway',
            # default_cors_preflight_options=_ag.CorsOptions(
            # allow_methods=['ANY'],
            # allow_origins=['*'],
            # allow_headers=['Access-Control-Allow-Origin','Access-Control-Allow-Headers','Content-Type']
            # )
        )
        posts_resource = api.root.add_resource('posts')
        posts_with_id_resource = posts_resource.add_resource("{id}")
        posts_resource.add_method('POST',
                                  _ag.LambdaIntegration(fn_lambda_create_post))
        posts_with_id_resource.add_method(
            'GET', _ag.LambdaIntegration(fn_lambda_get_post))
        posts_resource.add_method('GET',
                                  _ag.LambdaIntegration(fn_lambda_list_post))
        posts_with_id_resource.add_method(
            'DELETE', _ag.LambdaIntegration(fn_lambda_delete_post))
