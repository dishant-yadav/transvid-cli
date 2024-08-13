import boto3
from botocore.exceptions import NoCredentialsError

def create_folder(folder_name, bucket="temp-videos-storage"): 
    if folder_name is None:
        raise RuntimeError("Folder name not specified")
    
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(Bucket=bucket, Key=folder_name)
    except NoCredentialsError:
        print("Credentials not available")
        return False
    
    print(f"Folder '{folder_name}' created in bucket '{bucket}'")
    return True

def upload_to_s3(file_name, folder_name=None, bucket="temp-videos-storage"):
    folder_name=folder_name+"/"
    # If S3 object_name was not specified, use file_name
    if folder_name is None:
        raise RuntimeError("Folder name not specified")
    
    # Create the full object key (including folder name)
    file = folder_name + file_name


    # Initialize a session using Amazon S3
    # s3_client = boto3.client('s3')
    try:
        print("file=", file, "bucket=", bucket, "folder=", folder_name)
        # response = s3_client.upload_file(file, bucket, file)
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

