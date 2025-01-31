#!/usr/bin/env python3
import boto3
import os

def test_wasabi_connection():
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
        
        # List objects in bucket to test access
        print(f"Testing access to bucket: {bucket}")
        response = s3_client.list_objects_v2(Bucket=bucket, MaxKeys=1)
        print("\nBucket access successful!")
        
        # Get bucket location
        location = s3_client.get_bucket_location(Bucket=bucket)
        print(f"\nBucket Location: {location}")
        
        # Try to get bucket usage if possible
        try:
            metrics = s3_client.get_metric_statistics(
                Namespace='AWS/S3',
                MetricName='BucketSizeBytes',
                Dimensions=[{'Name': 'BucketName', 'Value': bucket}],
                StartTime='2024-01-01T00:00:00Z',
                EndTime='2024-12-31T23:59:59Z',
                Period=3600,
                Statistics=['Average']
            )
            print(f"\nBucket Metrics: {metrics}")
        except Exception as e:
            print(f"\nNote: Could not get bucket metrics: {str(e)}")
            
        # Print current environment configuration
        print("\nCurrent Configuration:")
        print(f"S3_ENDPOINT: {os.getenv('S3_ENDPOINT')}")
        print(f"S3_REGION: {os.getenv('S3_REGION', 'us-east-1')}")
        print(f"S3_BUCKET: {os.getenv('S3_BUCKET')}")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nPlease check:")
        print("1. Your credentials are correct")
        print("2. The bucket exists and is accessible")
        print("3. Your endpoint URL is correct for Wasabi")
        print("4. Your account is active and in good standing")

if __name__ == "__main__":
    test_wasabi_connection()