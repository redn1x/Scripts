#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import urllib2

dst_folder = "/opt/java/"

Versions = [6,7]
Updates = range(1,45)
Builds = range(1,21)
Archs = ["x64","i586"]
Platform = "linux"

def wget(url,dstfile):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'gpw_e24=http'))
    try:
        javafile = opener.open(url)
    except:
        print "failed"
        return False
    output = open(dstfile,'wb')
    output.write(javafile.read())
    output.close()
    return True


for Version in Versions:
    for Update in Updates:        
        for Arch in Archs:
            fold_name = '_'.join(['java',Arch,Platform])
            fold = dst_folder + fold_name
            if not os.path.exists(fold):
                os.makedirs(fold)
            
            URL_part1 = "http://download.oracle.com/otn-pub/java/jdk/"
            URL_part2 = "VERSIONuUPDATE-bBUILD/"
            URL_part2 = re.sub("VERSION",str(Version),URL_part2)
            URL_part2 = re.sub("UPDATE",str(Update),URL_part2)
            URL_part2 = re.sub("ARCHI",str(Arch),URL_part2)
            URL_part2 = re.sub("PLATFORM",str(Platform),URL_part2)
            
            filename = "jdk-VERSIONuUPDATE-PLATFORM-ARCHI.EXT"
            filename = re.sub("VERSION",str(Version),filename)
            filename = re.sub("UPDATE",str(Update),filename)
            filename = re.sub("ARCHI",str(Arch),filename)
            filename = re.sub("PLATFORM",str(Platform),filename)
            
            if "linux" == Platform:
                ext='tar.gz'
            if "windows" == Platform:
                ext='exe'
            if "macosx" == Platform:
                ext='dmg'
            filename = re.sub("EXT",str(ext),filename)
            URL1 = URL_part1 + URL_part2 + filename
            URL2 = URL_part1 + filename
                      
            goodbuild=False
            Build=25
            while goodbuild == False and Build > 0 :
                Build = Build - 1 
                b_URL1 = re.sub("BUILD",str(Build),URL1)
                b_URL2 = re.sub("BUILD",str(Build),URL2)
                print b_URL1
                print b_URL2
                print '/'.join([fold,filename])
                if wget(b_URL1,'/'.join([fold,filename])):
                    URL = 1
                    goodbuild = Build
                    Platforms = ["macosx","windows"]
                if wget(b_URL2,'/'.join([fold,filename])):
                    URL = 2
                    goodbuild = Build
                    Platforms = ["macosx","windows"]
                
                
            if goodbuild:
                for Platform in Platforms:
                    URL_part1 = "http://download.oracle.com/otn-pub/java/jdk/"
                    URL_part2 = "VERSIONuUPDATE-bBUILD/"
                    URL_part2 = re.sub("VERSION",str(Version),URL_part2)
                    URL_part2 = re.sub("UPDATE",str(Update),URL_part2)
                    URL_part2 = re.sub("ARCHI",str(Arch),URL_part2)
                    URL_part2 = re.sub("PLATFORM",str(Platform),URL_part2)
                    
                    filename = "jdk-VERSIONuUPDATE-PLATFORM-ARCHI.EXT"
                    filename = re.sub("VERSION",str(Version),filename)
                    filename = re.sub("UPDATE",str(Update),filename)
                    filename = re.sub("ARCHI",str(Arch),filename)
                    filename = re.sub("PLATFORM",str(Platform),filename)
                    
                    if "linux" == Platform:
                        ext='tar.gz'
                    if "windows" == Platform:
                        ext='exe'
                    if "macosx" == Platform:
                        ext='dmg'
                    filename = re.sub("EXT",str(ext),filename)
                    URL1 = URL_part1 + URL_part2 + filename
                    URL2 = URL_part1 + filename
                    if URL == 1:
                        wget(URL1,'/'.join([fold,filename]))
                    else:
                        wget(URL2,'/'.join([fold,filenam
