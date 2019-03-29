import boto3
import json
import os
from time import sleep
from botocore.exceptions import ClientError
from botocore.vendored import requests

def notify(slack_url, status, reason):
    slack_message = {
        'attachments':[
            {'text': 'CloudFormation Stack Status is {}'.format(status)},
            {'text': reason}
        ]
    }
    #requests.post(slack_url, json=slack_message)
    print("Stack operation is {}. [Message: {}]".format(status,reason))
    if status == 'Success':
        exit(0)
    else:
        exit(1)

if not os.path.isfile("config.json"):
    print("No configuration file.")
    exit(1)
with open("config.json") as file:
    config = json.loads(file.read())
template = "cloudformation.{}".format(config['format'])
if not os.path.isfile(template):
    print("No template file.")
    exit(1)
client = boto3.client('cloudformation')
args = config['options']
with open(template) as file:
    args['TemplateBody'] = file.read()
try:
    stack = client.create_stack(**args)
except ClientError as e:
    notify(config['notify']['slack'], 'Fail', e.response['Error']['Message'])
stackname = config['options']['StackName']
print("Stack creation initialized: {}".format(stack['StackId']))
while True:
    status = client.describe_stacks(StackName=stackname)['Stacks'][0]
    if status['StackStatus'] in ['CREATE_IN_PROGRESS', 'UPDATE_IN_PROGRESS', 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS', 'REVIEW_IN_PROGRESS']:
        print("Stack operation is in progress...")
        sleep(config['interval'])
        continue
    else:
        break
if status['StackStatus'] in ['CREATE_COMPLETE', 'UPDATE_COMPLETE']:
    notify(config['notify']['slack'], 'Success', 'Stack operation was success.')
else:
    notify(config['notify']['slack'], 'Fail', stack['StackStatusReason'])