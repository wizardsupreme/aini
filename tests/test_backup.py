#!/usr/bin/env python3
import consul
import boto3
import json
import os
import time

def test_consul_s3_backup():
    # Initialize Consul client
    c = consul.Consul(
        host=os.getenv('CONSUL_HTTP_ADDR', 'localhost').split(':')[0],
        port=int(os.getenv('CONSUL_HTTP_ADDR', 'localhost:8500').split(':')[1])
    )
    
    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
        endpoint_url=os.getenv('S3_ENDPOINT'),
        region_name=os.getenv('S3_REGION', 'us-east-1')
    )
    
    bucket = os.getenv('S3_BUCKET')
    backup_key = 'aini-consul-backup.json'
    
    # 1. Put test data in Consul
    test_key = 'aini/test/backup'
    test_value = {
        'timestamp': time.time(),
        'test_data': 'This is a test backup'
    }
    
    print(f"Writing test data to Consul: {test_value}")
    c.kv.put(test_key, json.dumps(test_value))
    
    # 2. Trigger backup
    # Get all KV pairs
    index, data = c.kv.get('aini/', recurse=True)
    if data:
        state = {
            item['Key']: json.loads(item['Value'].decode('utf-8'))
            for item in data 
            if item['Value']
        }
        
        print(f"Backing up state to S3: {state}")
        s3_client.put_object(
            Bucket=bucket,
            Key=backup_key,
            Body=json.dumps(state, indent=2)
        )
    
    # 3. Verify backup in S3
    print("\nVerifying backup in S3...")
    try:
        response = s3_client.get_object(Bucket=bucket, Key=backup_key)
        backup_data = json.loads(response['Body'].read().decode('utf-8'))
        print(f"Retrieved backup from S3: {backup_data}")
        
        # Verify our test data is in the backup
        if test_key in backup_data:
            print("\n✅ Test successful! Data was properly backed up to S3")
        else:
            print("\n❌ Test failed! Could not find test data in backup")
            
    except Exception as e:
        print(f"\n❌ Error retrieving backup: {str(e)}")

if __name__ == "__main__":
    test_consul_s3_backup()