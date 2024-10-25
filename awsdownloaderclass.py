import boto3
from boto3.session import Session
import botocore
import logging



class awshandler:
  def __init__(self):
    pass
 
  def connect(self):   #you will need programmatic access with this one 
    session = Session(
      'ap-southeast-1', #region
      '<aws_id>', #aws id
      '<aws_key>', #aws key
    )
    self.client = session.client('s3')
    self.resource = session.resource('s3')
    logging.info('aws connected')

  def listfile(self):
    logging.info('aws listing files')
    result = self.client.list_objects(
        Bucket='s3.bucket.com',
        Prefix='builds',
    )
    list = []
    for obj in result['Contents']:
        list =(obj['Key'],obj['Size'])
    return list

  def getfilsize(self):
    result = self.client.list_objects(
        Bucket='s3.bucket.com',
        Prefix='builds',
    )
    list = []
    x = 0
    for obj in result['Contents']:
        list =(obj['Size'])
        if list > x:
           return list
        else:
           return 0 

  def dlfile(self,bucket,filename,location):
    try:
        logging.info('aws downloading:%s to %s'%(filename,location))
        self.resource.meta.client.download_file(bucket,filename,location)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
           print("The object does not exist.")
        else:
            raise 
  def dlist(self,list):
    for entry in list:
      self.dlfile(entry['bucket'],entry['filename'],entry['location'])

awstest = awshandler()
awstest.connect()
awstest.dlfile('s3.bucket.com', 'builds/UnixBuild7777.bin','/opt/UnixBuild7777.bin')
