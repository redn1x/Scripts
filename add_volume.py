#!/usr/bin/python
import boto3
import botocore
from boto3.session import Session
#from read_configs import *
#import argparse, os
import datetime, time
import argparse, os, sys, subprocess, shutil
import logging

from dateutil.parser import parse
#from boto.ses.connection import SESConnection
from botocore.exceptions import ClientError

from read_config import *

#REGION = "eu-central-1"

cwd = os.getcwd()
logLevel = logging.DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(logLevel)
# create a file handler
handler = logging.FileHandler('add_volume.log')
handler.setLevel(logLevel)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

def create_volume_tags(vid,iname):
	#session = Session(region_name='ap-northeast-1', aws_access_key_id=ACCOUNT_AWSID, aws_secret_access_key=ACCOUNT_AWSSECRET)
	session = Session(region_name=account_region, aws_access_key_id=ACCOUNT_AWSID, aws_secret_access_key=ACCOUNT_AWSSECRET)
	ec2 = session.client('ec2')		
	response = ec2.create_tags(Resources=[vid], Tags=[{'Key': 'Name', 'Value': iname + "-log"},])

def attach_volume(instance_id,volume_id):
        try:
                session = Session(region_name=account_region, aws_access_key_id=ACCOUNT_AWSID, aws_secret_access_key=ACCOUNT_AWSSECRET)
                ec2 = session.client('ec2')
                response = ec2.attach_volume(Device='/dev/xvdf',InstanceId=instance_id,VolumeId=volume_id,)
                print "Attachment Successful!!!"
                logger.info ("Attachment Successful!!!")
        except ClientError as e:
                logger.error(str(e))
                print(str(e))
        except Exception as e:
                logger.error(str(e))
                print(str(e))

def create_volume(az):
        try:
                session = Session(region_name=account_region, aws_access_key_id=ACCOUNT_AWSID, aws_secret_access_key=ACCOUNT_AWSSECRET)
                ec2 = session.client('ec2')
                response = ec2.create_volume(AvailabilityZone=az,Size=100,VolumeType='gp2',)
                #logger.info (response)
		vid = response['VolumeId']
		print "New Volume Created " + vid
	        logger.info ("New Volume Created " + vid)
		return vid
        except ClientError as e:
                logger.error(str(e))
                print(str(e))
        except Exception as e:
                logger.error(str(e))
                print(str(e))

def describe_instance_availabilityzone(instance_name):
        try:
                session = Session(region_name=account_region, aws_access_key_id=ACCOUNT_AWSID, aws_secret_access_key=ACCOUNT_AWSSECRET)
                ec2 = session.client('ec2')
                response = ec2.describe_instances(Filters=[{'Name': 'tag-value','Values': [instance_name,]},],)
		#logger.info(response)
                for res in response['Reservations']:
                        az = res['Instances'][0]['Placement']['AvailabilityZone']
                        logger.info(az)
                        return az
        except ClientError as e:
                logger.error(str(e))
                print(str(e))
        except Exception as e:
                logger.error(str(e))
                print(str(e))

def describe_instance_instance_id(instance_name):
        try:
                session = Session(region_name=account_region, aws_access_key_id=ACCOUNT_AWSID, aws_secret_access_key=ACCOUNT_AWSSECRET)
                ec2 = session.client('ec2')
                response = ec2.describe_instances(Filters=[{'Name': 'tag-value','Values': [instance_name,]},],)
                #logger.info(response)
                for res in response['Reservations']:
                        iid = res['Instances'][0]['InstanceId']
                        logger.info(iid)
                        return iid
        except ClientError as e:
                logger.error(str(e))
                print(str(e))
        except Exception as e:
                logger.error(str(e))
                print(str(e))

def input_yes_or_no_option():
        print "Select 1 for YES 2 For No \n1:YES \n2:NO"
        logger.info ("Select 1 for YES 2 For No \n1:YES \n2:NO")
        yon = int(raw_input("Select 1 or 2: "))
        print yon
        logger.info (yon)
        try:
                if yon == 1:
                        #print "Proceed on Security Group Creation"
                        #logger.info ("Proceed on Security Group Creation")
                        return yon
                        #input_pod_name()
                else:
                        print "System Exit"
                        sys.exit(1)
        except Exception as e:
                logger.error(str(e))
                print(str(e))


def input_instance_id():
        instanceid = str(raw_input("Enter InstanceID: "))
        logger.info (instanceid)
        result = describe_instances(instanceid)
        return result

def input_instance_name():
        instance_name = str(raw_input("Enter InstanceName of Instance that you like to Increase/Add Volume: "))
        logger.info (instance_name)
        az = describe_instance_availabilityzone(instance_name)
	iid = describe_instance_instance_id(instance_name)
        logger.info(az)
	logger.info(iid)
	vid = create_volume(az)
	logger.info(vid)
	create_volume_tags(vid,instance_name)
	print "\nWill proceed attaching " + vid + " to InstanceName: " + instance_name + " InstanceID: " + iid + "\n"
	logger.info("\nWill proceed attaching " + vid + " to InstanceName: " + instance_name + " InstanceID: " + iid + "\n")
	confirm_yon = input_yes_or_no_option()
	if confirm_yon == 1:
		print "Procced on Attachement"
		attach_volume(iid,vid)

	
def get_region():

        us_list = ['us1', 'us2', 'us3', 'us4', 'us5','us6', 'us7', 'us8' 'us9']
        au_list = ['au1', 'au2', 'au3', 'au4', 'au5','au6', 'au7', 'au8' 'au9']
        jp_list = ['jp1', 'jp2', 'jp3', 'jp4', 'jp5','jp6', 'jp7', 'jp8' 'jp9']
        ca_list = ['ca1', 'ca2', 'ca3', 'ca4', 'ca5','ca6', 'ca7', 'ca8' 'ca9']
        ger_list = ['ger1', 'ger2', 'ger3', 'ger4', 'ger5','ger6', 'ger7', 'ger8' 'ger9']
        ir_list = ['ir', 'ir2', 'ir3', 'ir4', 'ir5','ir6', 'ir7', 'ir8' 'ir9']
        fr_list = ['fr', 'fr2', 'fr3', 'fr4', 'fr5','fr6', 'fr7', 'fr8' 'fr9']
        br_list = ['br1', 'br2', 'br3', 'br4', 'br5','br6', 'br7', 'br8' 'br9']

        print "****************************************"
        print "*      Get Region From Site Name         *"
        print "****************************************"
        print "\n \n"
        pn = str(raw_input("Enter Site Name: "))
        logger.info (pn)
        global account_region
        try:
                for i in us_list:
                        if pn in i:
                                logger.info ("Region Set to us-east-1")
                                account_region = "us-east-1"
                for i in au_list:
                        if pn in i:
                                logger.info ("Region Set to ap-southeast-2")
                                account_region = "ap-southeast-2"
                for i in jp_list:
                        if pn in i:
                                logger.info ("Region Set to ap-northeast-1")
                                account_region = "ap-northeast-1"
                for i in ca_list:
                        if pn in i:
                                logger.info ("Region Set to ca-central-1")
                                account_region = "ca-central-1"
                for i in ger_list:
                        if pn in i:
                                logger.info ("Region Set to eu-central-1")
                                account_region = "eu-central-1"
                for i in ir_list:
                        if pn in i:
                                logger.info ("Region Set to eu-west-1")
                                account_region = "eu-west-1"
                for i in fr_list:
                        if pn in i:
                                logger.info ("Region Set to eu-west-3")
                                account_region = "eu-west-3"
                for i in br_list:
                        if pn in i:
                                logger.info ("Region Set to sa-east-1")
                                account_region = "sa-east-1i"
			#else:
			#	logger.info("Site Not Found Please try again!!!!")
			#	print "Site Not Found Please try again!!!!"
			#	account_region = None
			#	print account_region
        except UnicodeDecodeError, ue:
                logger.error(str(ue))
                print(str(ue))




get_region()
if account_region is None:
	sys.exit(1)
else:
	input_instance_name()
