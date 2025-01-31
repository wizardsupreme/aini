#!/usr/bin/env python3
import boto3
import os
from datetime import datetime

def list_bucket_contents():
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
        print(f"\nListing contents for bucket: {bucket}")
        print("=" * 60)
        
        # List buckets first
        buckets = s3_client.list_buckets()
        print("\nAvailable buckets:")
        for b in buckets['Buckets']:
            print(f"- {b['Name']} (Created: {b['CreationDate']})")
        
        print("\nBucket contents:")
        print("=" * 60)
        
        total_size = 0
        total_files = 0
        
        # Use paginator to handle buckets with many objects
        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket):
            if 'Contents' in page:
                for obj in page['Contents']:
                    total_files += 1
                    total_size += obj['Size']
                    print(f"File: {obj['Key']}")
                    print(f"Size: {obj['Size'] / (1024*1024):.2f} MB")
                    print(f"Last Modified: {obj['LastModified']}")
                    print("-" * 50)
        
        print("\nSummary:")
        print(f"Total Files: {total_files}")
        print(f"Total Size: {total_size / (1024*1024*1024):.2f} GB")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print("\nDebug Information:")
        print(f"Endpoint: {os.getenv('S3_ENDPOINT')}")
        print(f"Region: {os.getenv('S3_REGION')}")
        print(f"Bucket: {os.getenv('S3_BUCKET')}")

if __name__ == "__main__":
    list_bucket_contents()