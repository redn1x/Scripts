#!/usr/bin/env bash

set -e

list=/tmp/instance.txt


getregion()
{

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



gather_suspended()
{

        psql -U database_user postgresql://my.database.server:5432/database -A -t -f /home/manager/query.sql | grep SITE >  $list  #change site everytime

}

awake()
{

        IFS='|'
        while read -r  SITE SUSPEND CLIENT  AWSINSTANCE IP
        do
                region=$(getregion $SITE)
                #x=$(echo $AWSINSTANCE |  sed 's/"//g')
                #echo $x
                aws ec2 start-instances --region $region --instance-ids $AWSINSTANCE

        done < "$list"
}

test_ping()
{
        list1=/tmp/instance.txt
        file=$(cat $list1 | cut -d '|' -f 5)

         for host in  $file
            do
                echo "running $host"
                sshpass -p myapssword ssh -t -o StrictHostKeyChecking=no serveruser@"$host" 'ping -c 2 web.server.myoffice > /dev/null'
                if [ $? = 0 ]
                then
                        echo working "$host" >> /tmp/working.txt
                else
                        echo not working "$host" >> /tmp/notworking.txt
                 fi

            done

}

create_image()
{



file1="/tmp/foo.txt"
file2="/tmp/bar.txt"
file3="/tmp/bar2.txt"

cat /tmp/notworking.txt | cut -d " " -f 3 >  $file1
cat /tmp/instance.txt | cut -d '|' -f 5  | sed 's/"//g' > $file2
cat /tmp/instance.txt | cut -d '|' -f 4,5  | sed 's/"//g' > $file3


result=$(awk 'FNR==NR {a[$1]; next} $1 in a' $file1 $file2)

for a in  $result
do
        foundins=$(grep $a $file3 | cut -d '|' -f  2)
        foundsite=$(grep $a $file3 | cut -d '|' -f  1)
        region=$(getregion $foundsite)
        aws ec2 create-image --region $region --instance-id $foundins --name backup_$foundins $(date)

done

}
stop_instance()
{

        IFS='|'
        while read -r  SITE SUSPEND CLIENT  AWSINSTANCE IP
        do
                region=$(getregion $SITE)
                #x=$(echo $AWSINSTANCE |  sed 's/"//g')
                #echo $x
                aws ec2 stop-instances  --region $region --instance-ids $AWSINSTANCE

        done < "$list"
}






gather_suspended
awake
test_ping
if [ -s /tmp/notworking.txt ]
then
        create_image
else
        stop_instance
fi
