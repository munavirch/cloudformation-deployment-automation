# cloudformation-deployment-automation
Automatic deployment of AWS CloudFormation templates

# How to use

1. Clone the repository to a new repository.
2. Edit config.json with below properties.
- format: template format, yaml or json
- type: update or create
- region: region to deploy the stack
- options: key word arguments to be passed to create_stack/update_stack API call. [Refere here for create_stack.](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_stack) [Refer here for update_stack.](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.update_stack)
- interval: number of seconds to wait between consecutive stack status checks
- notify.slack - slack webhook URL for notification