import os
import logging
import boto3
from boto3.session import Session
import botocore
import json
import socket
import subprocess
import os.path

FORMAT = '%(asctime)-15s - %(levelname)s - %(message)s'



if 'caliban' == socket.gethostname():
    calibanfolder = '''/opt'''
    debug = False
    logging.basicConfig(
        filename='/home/manager/logs/experimental.log',
        level=logging.INFO,
        format=FORMAT)

elif 'dev' in __file__:
    debug = True
    logging.basicConfig(
        filename='/home/manager/logs/experimental.log',
        level=logging.DEBUG,
        format=FORMAT)

else:
    serverfolder = '''/home/krault/disk2/Files/tests/'''
    debug = True
    logging.basicConfig(
        filename='/home/manager/logs/experimental.log',
        level=logging.DEBUG,
        format=FORMAT)


def download(builds):
    session = Session(region_name='us-east-1', aws_access_key_id="<aws progammatic access key id>, aws_secret_access_key="<aws progammatic access key>")
    s3 = session.resource('s3')
    logging.info('aws connected')
    try:
       for build in builds.keys():
           s3.meta.client.download_file('s3source.build.com', builds[build]["source"], builds[build]["target"])
    except botocore.exceptions.ClientError as e:
        print("Error while trying to download file: %s" %e)


def readfile():
    build4  = 'builds4.json' 
    directory = []
    directory = os.listdir('/opt/exp')
    if directory[1] == build4:
        file = '/opt/exp/builds4.json' 
        with open (file, 'r') as f:
            jsondata = json.load(f)
            latest = jsondata["latest"]
            a=latest.split("_")
            a[1]='Exp4'
            latest1 = '_'.join(a) 
            firstm = 'UnixBuildSetup'
            path2 = '/usr/local/bin/'
            folder = '/setups'
            firstx = ''.join([firstm,latest1]) #change
            source = 's3://s3source.build.com/exp4'
            destination = 's3://s3destination.build.com/builds'
            path = '/' + latest + folder + '/' + firstx +".bin"
            input1 = ' ' + source + path + ' ' + destination + '/' + firstx + ".bin"
            cmd1 = path2 + 'aws s3 cp'  + input1 + ' ' + '--acl' + ' ' + 'bucket-owner-full-control'
            p = subprocess.Popen(cmd1, shell = True ,stdout=subprocess.PIPE)
            output, error = p.communicate()
            p.stdout.close()


builds = {
   "exp10": {"source": "exp10/builds.json", "target": "/opt/exp/builds10.json"},
   "exp11": {"source": "exp11/builds.json", "target": "/opt/exp/builds11.json"},
   "exp12": {"source": "exp12/builds.json", "target": "/opt/exp/builds11.json"},
   "exp2": {"source": "exp2/builds.json", "target": "/opt/exp/builds2.json"},
   "exp3": {"source": "exp3/builds.json", "target": "/opt/exp/builds3.json"},
   "exp4": {"source": "exp4/builds.json", "target": "/opt/exp/builds4.json"},
   "exp7": {"source": "exp7/builds.json", "target": "/opt/exp/builds7.json"},
   "exp9": {"source": "exp9/builds.json", "target": "/opt/exp/builds9.json"},
   "exp13": {"source": "exp13/builds.json", "target": "/opt/exp/builds13.json"},

}

download(builds)
readfile()

