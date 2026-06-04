import json
import os
import boto3
import hashlib
from simhash import Simhash
from normalizer import normalize

def lambda_handler(event, context):
    # boto3 client MUST be created inside here, not at top level
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table(os.environ.get('TABLE_NAME', 'RecordsTable'))
    
    body = json.loads(event['body'])
    data = body['data']
    
    normalized = normalize(data)
    content_str = json.dumps(normalized, sort_keys=True)
    content_hash = hashlib.sha256(content_str.encode()).hexdigest()
    
    response = table.get_item(Key={'content_hash': content_hash})
    if 'Item' in response:
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'duplicate_exact', 'hash': content_hash})
        }
    
    text_for_simhash = " ".join(str(v) for v in normalized.values())
    simhash_value = Simhash(text_for_simhash).value
    
    item = {
        'content_hash': content_hash,
        'simhash': simhash_value,
        'data': normalized
    }
    table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'status': 'inserted', 'hash': content_hash})
    }