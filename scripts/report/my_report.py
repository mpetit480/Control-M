#!/usr/bin/env python3
#install :  pip3 install requests
# version 0.1 08/2022  Mathieu Petit, BMC Software
# version 0.2 03/2023  Mathieu Petit, BMC Software
import requests
from requests.structures import CaseInsensitiveDict
import sys,getopt
import json
import datetime
import warnings
import os
warnings.filterwarnings("ignore")

env="centos802"
limit="1000"
cpt=0

#BASE_PATH = os.path.abspath("")
#with open(BASE_PATH + "/secrets", "r") as fp:
#    ctm_uri = fp.readline().strip()
#    ctm_user = fp.readline().strip()
#    ctm_pwd = fp.readline().strip()

ini_path=os.path.abspath(os.path.dirname(__file__))

import configparser
config = configparser.ConfigParser()
config.read(ini_path+'/env.ini') #path of your .ini file
ctm_uri = config.get(env,"url") 
#ctm_user = config.get(env,"username") 
#ctm_pwd = config.get(env,"password") 
ctm_token = config.get(env,"token") 


fullreport=[]
indent_space="    "
argumentList = sys.argv[1:]
 
# Options
f_application="*"
f_jobname="*"
options = "hj:a:"
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options)
    # checking each argument
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h"):
            print ("Syntax\n[-h] help\n[-j jobname] [-a application]\n")
        elif currentArgument in ("-j"):
            f_jobname=currentValue
        elif currentArgument in ("-a"):
            f_application=currentValue
             
except getopt.error as err:
    print (str(err))
    print ("Syntax\n[-h] help\n[-j jobname] [-a application]\n")
    sys.exit(1)	 

if(len(f_jobname) < 1):
    print ("Syntax\n[-h] help\n[-j jobname] [-a application]\n")
    print('\nDEbug: {} \n'.format(f_jobname))
    sys.exit(1)



newHeaders = CaseInsensitiveDict()
newHeaders['Content-type']='application/json'
newHeaders['Accept']='application/json'
newHeaders['charset']='UTF-8'

####################################
####  Get token
####################################

#URL=ctm_uri + "/session/login"
#data= {
# 'username':ctm_user,
# 'password':ctm_pwd
#}

#resp = requests.post(url=URL,headers=newHeaders,verify=False,json=data)
#if(resp.status_code == 200):
#        objects=json.loads(resp.content)
#     #   print(json.dumps(objects,indent=4))
#else:
#   resp.raise_for_status
#
##print('\nToken: {} \n'.format(objects['token']))

#####################################
##  Query AAPI to get run statuses
######################################

URL=ctm_uri + "/run/jobs/status?jobname=" + f_jobname + "&application=" + f_application + "&limit=" + limit
#newHeaders['authorization']='Bearer' + objects['token']
newHeaders['x-api-key'] = ctm_token
resp = requests.get(url=URL,headers=newHeaders,verify=False)
if(resp.status_code == 200):
        objects=json.loads(resp.content)
      #  print(json.dumps(objects,indent=4))
#        prev_folder=""
        for i in objects['statuses']:
           tags=""
           if i['held'] == True:
              tags=tags+"H"
           if i['cyclic'] == True:
              tags=tags+"C"
           if i['deleted'] == True:
              tags=tags+"D"

###  Fill a list to build a database of jobs statuses

           fullreport.append({'Myjobname':i['name'],'Mytype':i['type'],'Myfolder':i['folder'],'Mystatus':i['status'],'Mystart':i['startTime'],'Myend':i['endTime'],'Myjobid':i['jobId'],'Myhost':i['host'],'Mytype':i['type'],'Mytag':tags})
#          if(prev_folder == i['folder']):
#             print('   {:30} \t\t\t{:10} {:12.12} {:12.12}'.format(i['name'],i['status'],i['startTime'],i['endTime']))
#          else:
#             print('{:30} \t\t\t{:10} {:12.12} {:12.12}'.format(i['name'],i['status'],i['startTime'],i['endTime']))
#          prev_folder=i['folder']
           
else:
   print(resp.raise_for_status())

### Sort the list to have correct order display
fullreport.sort(key=lambda x: x.get('Myjobid'))
#fullreport.sort(key=lambda x: x.get('Mykey'))

###########################################################
####   Display the report
##########################################################

print('Report: Limit '+ limit + '\n')
print('{:<54}{:10}{:<18}{:<22}{:<22}{:<18}{:<18}{:^10}'.format('Job Name','Type','Status','Start Time','End Time','Job Id','Host','Held/Cyclic/Deleted'))
print('_____________________________________________________________________________________________________________________________________________________________\n')
for i in fullreport:
   if  i['Mytype'] == 'Folder':
      indent=""
   if i['Myfolder'].find('/') == -1 and i['Mytype'] != 'Folder':
      indent=indent_space
   if  i['Mytype'] == 'Sub-Table':
      indent=indent+indent_space
   if i['Myfolder'].find('/') == 1:
      indent=indent+indent_space
   if i['Myfolder'].find('/') == 2:
      indent=indent+indent_space
   Mystart=i['Mystart']
   if len(i['Mystart']) == 14:
       Mystart=str(datetime.datetime.strptime(i['Mystart'],'%Y%m%d%H%M%S'))
   Myend=i['Myend']
   if len(i['Myend']) == 14:
       Myend=str(datetime.datetime.strptime(i['Myend'],'%Y%m%d%H%M%S'))
   print('{:<54}{:10}{:<18}{:<22}{:<22}{:<18}{:<18}{:^10}'.format(indent+i['Myjobname'],i['Mytype'],i['Mystatus'],Mystart,Myend,i['Myjobid'],i['Myhost'],i['Mytag']))
   cpt=cpt+1
#print(fullreport)
print('\n\nReport: '+ str(cpt) + ' jobs. Limit is '+ limit + '\n')


