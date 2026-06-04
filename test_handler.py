import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import boto3
from moto import mock_aws

# Fake creds must be set BEFORE importing handler
os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
os.environ['AWS_DEFAULT_REGION'] = 'ap-south-1'
os.environ['TABLE_NAME'] = 'RecordsTable'

@mock_aws
def test_dedupe_flow():
    # Import handler INSIDE the test, after moto starts
    from handler import lambda_handler
    
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    dynamodb.create_table(
        TableName='RecordsTable',
        KeySchema=[{'AttributeName': 'content_hash', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'content_hash', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    
    event = {"body": json.dumps({"data": {"email": "a@test.com"}})}
    
    res1 = lambda_handler(event, None)
    assert json.loads(res1['body'])['status'] == 'inserted'
    
    res2 = lambda_handler(event, None)
    assert json.loads(res2['body'])['status'] == 'duplicate_exact'