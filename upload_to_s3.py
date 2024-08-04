import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_s3(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Initialize a session using Amazon S3
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    return True

if __name__ == "__main__":
    # video-thumbnail-temp-1 input.mp4_thumbnail.png
    # video-transcoding-temp-1 input.mp4
    success = upload_to_s3('input.mp4_thumbnail.png', 'video-thumbnail-temp-1', 'input.mp4_thumbnail.png')

    if success:
        print("Upload Successful")
    else:
        print("Upload Failed")

