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
f_jobid=""
options = "hj:"
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options)
    # checking each argument
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h"):
            print ("Syntax\n[-h] help\n[-j jobId]\n") 
        elif currentArgument in ("-j"):
            f_jobid=currentValue
             
except getopt.error as err:
    print (str(err))
    print ("Syntax\n[-h] help\n[-j jobId]\n")
    sys.exit(1)	 

if(len(f_jobid) < 1):
    print ("Syntax\n[-h] help\n[-j jobId]\n") 
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
URL=ctm_uri + "run/job/" + f_jobid + "/output"
#newHeaders['authorization']='Bearer' + objects['token']
newHeaders['x-api-key'] = ctm_token
resp = requests.get(url=URL,headers=newHeaders,verify=False)
if(resp.status_code == 200):
  print(resp.text)
