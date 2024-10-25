from boto3.session import Session
import boto3
import botocore


session = Session(region_name='us-east-1', aws_access_key_id="<aws_access_key_id>", aws_secret_access_key="<aws_access_key>")  

s3 = session.resource('s3')
try:
    s3.meta.client.download_file('s3.company.com', 'build/3333/setups/UnixBuild3333.bin','/opt/UnixBuild3333.bin') 
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise
