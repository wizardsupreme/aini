#!/usr/bin/env python3
import boto3
import os
from botocore.config import Config

def check_bucket_detailed():
    # Print environment variables (with secrets masked)
    print("Current Configuration:")
    print(f"S3_ENDPOINT: {os.getenv('S3_ENDPOINT')}")
    print(f"S3_REGION: {os.getenv('S3_REGION')}")
    print(f"S3_BUCKET: {os.getenv('S3_BUCKET')}")
    print(f"S3_ACCESS_KEY: {os.getenv('S3_ACCESS_KEY')[:4]}...{os.getenv('S3_ACCESS_KEY')[-4:]}")
    
    # Create a custom configuration
    config = Config(
        signature_version='s3v4',
        retries = dict(
            max_attempts = 3
        )
    )
    
    try:
        # Initialize S3 client with explicit configuration
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
            endpoint_url=os.getenv('S3_ENDPOINT'),
            region_name=os.getenv('S3_REGION', 'us-east-1'),
            config=config
        )
        
        bucket = os.getenv('S3_BUCKET')
        print(f"\nAttempting to list contents of bucket: {bucket}")
        
        # Try to get bucket location first
        try:
            location = s3_client.get_bucket_location(Bucket=bucket)
            print(f"Bucket location: {location}")
        except Exception as e:
            print(f"Could not get bucket location: {str(e)}")
        
        # List objects with detailed error handling
        try:
            # First, try a simple list
            response = s3_client.list_objects_v2(
                Bucket=bucket,
                MaxKeys=1000  # Increase if needed
            )
            
            if 'Contents' in response:
                print("\nFiles found:")
                for obj in response['Contents']:
                    print(f"- {obj['Key']} ({obj['Size']/1024/1024:.2f} MB)")
                print(f"\nTotal objects: {len(response['Contents'])}")
                
                if response.get('IsTruncated', False):
                    print("Note: More files exist but listing is truncated")
            else:
                print("\nNo objects found in bucket")
                
            # Print response metadata for debugging
            print("\nResponse Metadata:")
            for key, value in response.get('ResponseMetadata', {}).items():
                print(f"{key}: {value}")
                
        except Exception as e:
            print(f"\nError listing objects: {str(e)}")
            
        # Try to check bucket ACL
        try:
            acl = s3_client.get_bucket_acl(Bucket=bucket)
            print("\nBucket ACL:")
            print(acl)
        except Exception as e:
            print(f"\nCould not get bucket ACL: {str(e)}")
            
    except Exception as e:
        print(f"\nMain error: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Verify these credentials match your Wasabi console")
        print("2. Check if bucket name is correct")
        print("3. Ensure endpoint matches bucket region")
        print("4. Verify IAM/user permissions include s3:ListBucket")

if __name__ == "__main__":
    check_bucket_detailed()