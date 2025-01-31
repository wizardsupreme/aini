#!/usr/bin/env python3
import boto3
import os
import json

def test_small_upload():
    try:
        # Initialize S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
            endpoint_url=os.getenv('S3_ENDPOINT'),
            region_name=os.getenv('S3_REGION', 'us-east-1')
        )
        
        bucket = os.getenv('S3_BUCKET')
        
        # Create a tiny test object
        test_data = {
            'test': 'This is a small test file',
            'timestamp': '2025-01-31'
        }
        
        print(f"Attempting to upload small test file to bucket: {bucket}")
        
        # Try to upload
        s3_client.put_object(
            Bucket=bucket,
            Key='test-upload.json',
            Body=json.dumps(test_data)
        )
        
        print("Upload successful!")
        
        # Try to read it back
        print("\nAttempting to read the file back...")
        response = s3_client.get_object(Bucket=bucket, Key='test-upload.json')
        data = json.loads(response['Body'].read().decode('utf-8'))
        print(f"Retrieved data: {data}")
        
        # Print object metadata
        print("\nObject metadata:")
        head = s3_client.head_object(Bucket=bucket, Key='test-upload.json')
        print(f"Content Length: {head['ContentLength']} bytes")
        print(f"Last Modified: {head['LastModified']}")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nDebug information:")
        print(f"Bucket: {bucket}")
        print(f"Endpoint: {os.getenv('S3_ENDPOINT')}")
        print(f"Region: {os.getenv('S3_REGION', 'us-east-1')}")

if __name__ == "__main__":
    test_small_upload()