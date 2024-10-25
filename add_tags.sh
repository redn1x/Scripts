#!/bin/bash
#set -x
#DEBUG=true
export AWS_PROFILE=automation_access
getregion()
{ # getregion pod => region
        pod="$(echo $1 | tr '[A-Z]' '[a-z]' | tr -d '"' )"
   case $pod in
        aume*) region=ap-southeast-2 ;;
        irdu*) region=eu-west-1 ;;
        frpr*) region=eu-west-3 ;;
        usva*) region=us-east-1 ;;
        brsp*) region=sa-east-1 ;;
        jptk*) region=ap-northeast-1 ;;
        usca*) region=us-west-1 ;;
        camo*) region=ca-central-1 ;;
        defr*) region=eu-central-1 ;;
   esac
   echo $region
}


date
IFS='|'
psql -U database_user postgresql://my.postgresql.server:5432/database -A -t -f /home/manager/tags/query.sql | while read CLIENT POD AWSINSTANCE DOMAIN
do
        region=$(getregion $POD)
        echo TAG  = $CLIENT –region=$region –aws=$AWSINSTANCE –
        aws ec2 create-tags --resources $AWSINSTANCE --tags Key=Customer,Value=$CLIENT --region $region --output table
        aws ec2 create-tags --resources $AWSINSTANCE --tags Key=BU,Value=$DOMAIN --region $region --output table
        aws ec2 describe-tags --filters "Name=resource-id,Values=$AWSINSTANCE" --region $region --output table
        EBS_ID=$(aws ec2 describe-instances --instance-ids $AWSINSTANCE --query 'Reservations[*].Instances[*].BlockDeviceMappings[*].[Ebs.VolumeId]' --region $region --output text)
        echo $EBS_ID | while read EBSID
        do
                aws ec2 create-tags --resources $EBSID --tags Key=Customer,Value=$CLIENT --region $region --output table
                aws ec2 create-tags --resources $EBSID --tags Key=BU,Value=$DOMAIN --region $region --output table
                aws ec2 create-tags --resources $EBSID --tags Key=PoD,Value=$POD --region $region --output table
                aws ec2 describe-tags --filters "Name=resource-id,Values=$EBSID" --region $region --output table
        done
done
