#!/usr/bin/env python3
import s3fs
import os

def list_with_s3fs():
    # Create S3 filesystem object
    fs = s3fs.S3FileSystem(
        key=os.getenv('S3_ACCESS_KEY'),
        secret=os.getenv('S3_SECRET_KEY'),
        endpoint_url=os.getenv('S3_ENDPOINT'),
        use_listings_cache=False
    )
    
    bucket = os.getenv('S3_BUCKET')
    print(f"\nTrying to list contents of bucket '{bucket}' using s3fs")
    print("=" * 60)
    
    try:
        # List all files in bucket
        files = fs.ls(f"{bucket}/")
        
        if files:
            print("\nFiles found:")
            for f in files:
                info = fs.info(f)
                size_mb = info['size'] / (1024 * 1024)
                print(f"- {f} ({size_mb:.2f} MB)")
                print(f"  Modified: {info['LastModified']}")
        else:
            print("No files found in bucket")
            
        # Try to get bucket info
        try:
            bucket_info = fs.info(bucket)
            print("\nBucket Info:")
            print(bucket_info)
        except Exception as e:
            print(f"\nCould not get bucket info: {str(e)}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nDebug info:")
        print(f"Endpoint URL: {os.getenv('S3_ENDPOINT')}")
        print(f"Region: {os.getenv('S3_REGION')}")

if __name__ == "__main__":
    list_with_s3fs()