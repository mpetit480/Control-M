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
null=None
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
f_server=""
options = "hs:"
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options)
    # checking each argument
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h"):
            print ("Syntax\n[-h] help\n[-s server]\n") 
        elif currentArgument in ("-s"):
            f_server=currentValue
             
except getopt.error as err:
    print (str(err))
    print ("Syntax\n[-h] help\n[-s server]\n")
    sys.exit(1)	 

if(len(f_server) < 1):
    print ("Syntax\n[-h] help\n[-s server]\n") 
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
##  Query AAPI to get Agent statuses
######################################
URL=ctm_uri + "config/server/" + f_server + "/agents"
#newHeaders['authorization']='Bearer' + objects['token']
newHeaders['x-api-key'] = ctm_token
resp = requests.get(url=URL,headers=newHeaders,verify=False)
if(resp.status_code == 200):
        objects=json.loads(resp.content)
#        print(json.dumps(objects,indent=4))
        for i in objects['agents']:
###  Fill a list to build a database of jobs statuses

           if "version" not in i:
               i['version']='-'
           if "operatingSystem" not in i:
               i['operatingSystem']='-'
           if "tag" not in i:
               i['tag']='-'
           if "hostgroups" not in i:
               i['hostgroups']='-'
           else:
               i['hostgroups']=','.join(i['hostgroups'])
           fullreport.append({'Myagent':i['nodeid'],'Mystatus':i['status'],'Myversion':i['version'],'MyOS':i['operatingSystem'],'Mygroup':i['hostgroups'],'Mytag':i['tag']})
else:
   print(resp.raise_for_status())

### Sort the list to have correct order display
fullreport.sort(key=lambda x: x.get('Myagent'))
#fullreport.sort(key=lambda x: x.get('Mykey'))

###########################################################
####   Display the report
##########################################################

print('Report: Limit '+ limit + '\n')
print('{:<54}{:18}{:<18}{:<22}{:<25}{:<18}'.format('Agent','Status','Version','OS','HostGroups','Tag'))
print('_____________________________________________________________________________________________________________________________________________________________\n')
for i in fullreport:
   print('{:<54}{:18}{:<18}{:<25}{:<18}{:<18}'.format(i['Myagent'],i['Mystatus'],i['Myversion'],i['MyOS'],i['Mygroup'],i['Mytag']))
   cpt=cpt+1
#print(fullreport)
print('\n\nReport: '+ str(cpt) + ' Agents. Limit is '+ limit + '\n')


