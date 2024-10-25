#!/usr/bin/env bash



set -e

folder="/var/www/db/"

check_filesage()
{

x=$(find $folder -iname '*.tgz' -mtime +5 | xargs ls -ltr)
echo "$x" > /home/manager/francis/foo
}

check_official_build() #filter official build like this build-0.1i-6666.tgz
{

ins=$(cat /home/manager/francis/foo  | awk '{print $9}' | cut -d '/' -f 5)
echo "$ins" > /home/manager/francis/build3
xy=$(cat /home/manager/francis/build3  | awk '/(^[build]+)-([0-9]+).([0-9a-z]+)-([0-9]+)/ {print $0}' > foo9)

}
filter(){

y=$(cat /home/manager/francis/foo9  | cut -d '-' -f 3 | tr -d .tgz)
echo  "$y" > foo10

}
check_buildusage()
{
file1=/home/manager/francis/foo10
file2=/home/manager/francis/foo5
sed -i d $file2
while IFS=  read line
do
    psql \
        --username=databaseuser \
        --dbname=database \
        --host=database.server.com  \
        --command=" \
            SELECT                                       \
                 "psn_version"."build" as BUILD,"domain"."id" as DOMAIN \
            FROM                                          \
                 "database"."public"."domain" "domain"      \
            INNER JOIN                                         \
                "database"."public"."build_version" "build_version"     \
            ON                                        \
                "domain"."build_version_id" = "build_version"."id" \
            WHERE                                                 \
                "build_version"."build" ='$line'"  \
| while read BUILD DOMAIN; do

echo $BUILD $DOMAIN >> "$file2"

done

done < "$file1"

}
delete_build(){

folder1="/var/www/db/"
x="/home/manager/francis/foo10"
y="/home/manager/francis/foo5"
n="/home/manager/francis/foo11"
z="/home/manager/francis/foo15"

while read BUILD DOMAIN
do
        echo "$BUILD" >> $n
done < "$y"

file3="/home/manager/francis/foo12"                                               #remove blank                  #remove duplicate

cat $n |  awk '{print $1}' | tr -d '-' | tr -d '+' | tr -d '(' | tr -d 'build' | sed '/^$/d;s/[[:blank:]]//g' | awk '!a[$0]++' > $file3

lastres=$(comm -3 --nocheck-order  $x $file3 |  sed '/^$/d;s/[[:blank:]]//g' | sed -r 's/(^|[^0-9])[0-9]([^0-9]|$)/\1\2/g; s/(^|[^0-9])[0-9]([^0-9]|$)/\1\2/g' | sed '/^$/d;s/[[:blank:]]//g')
echo "$lastres" > $z

while read line
do       
	#echo 'list' $line
    find $folder1 -name '*.tgz' | grep $line  | xargs ls -ltr >> /home/manager/francis/builddeletelog

done < "$z"



}
deregister(){

file2="/home/manager/francis/builddeletelog"

while IFS=  read line
do
    psql \
        --username=databaseuser \
        --dbname=database \
        --host=database.server.com  \
        --command=" \
            DELETE FROM "database"."public"."build_version"  \
            WHERE  "build_version"."build" ='$line'"  \


done < "$z"

}
check_filesage
check_official_build
filter
check_buildusage
delete_build
deregister
