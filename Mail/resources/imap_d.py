# Mathieu PETIT
# 1.0  2022/07/18 


from imap_tools import MailBox, MailMessageFlags, AND
import os,sys,getopt,time

argumentList = sys.argv[1:]

options = "i:k:l:p:d:t:f:s:m:ejruh"
try:
    # Parsing argument
    #arguments, values = getopt.getopt(argumentList, options)
    arguments, values = getopt.getopt(sys.argv[1:],"a:i:l:p:d:t:f:s:m:c:o:w:b:ejkruh")
except getopt.GetoptError as err:
    print(str(err))
    print("Syntax\n[-h] help\n\n")
    sys.exit(1)	 
     
mail_delete=False
mail_unread=False
mail_markread=False
mail_move=""
mail_savefolder=""
ctm_env=""
ctm_folder=""
mail_kill=0
mail_from=""
job=""


loop=0
delay=10
timeout=1
msgcount=0


    # checking each argument
for currentArgument, currentValue in arguments:
        if currentArgument in ("-h"):
            print ("Syntax\n[-h] help\n\n")
        elif currentArgument in ("-i"):
            mail_hostname=currentValue
        elif currentArgument in ("-k"):
            mail_kill=1
        elif currentArgument in ("-l"):
            mail_usrname=currentValue
        elif currentArgument in ("-p"):
            mail_password=currentValue
        elif currentArgument in ("-d"):
            mail_folder=currentValue
        elif currentArgument in ("-s"):
            mail_subject=currentValue
        elif currentArgument in ("-f"):
            mail_from=currentValue
        elif currentArgument in ("-t"):
            mail_savefolder=currentValue
        elif currentArgument in ("-m"):
            mail_move=currentValue
        elif currentArgument in ("-e"):
            mail_delete=True
        elif currentArgument in ("-c"):
            ctm_env=currentValue
        elif currentArgument in ("-o"):
            ctm_folder=currentValue
        elif currentArgument in ("-w"):
            timeout=60 * int(currentValue)
        elif currentArgument in ("-a"):
            delay=int(currentValue)
        elif currentArgument in ("-b"):
            job=currentValue

             
if len(sys.argv) < 14:
  print("Syntax\n[-h] help\n\n")
  sys.exit(1)

#### login to mailbox
try:
   mailbox = MailBox(mail_hostname).login(mail_usrname,mail_password)
except Exception as err:
   print(str(err))
   sys.exit(2)


###  set working mail folder
try:
   mailbox.folder.set(mail_folder)
except Exception as err:
   print(str(err))
   sys.exit(2)
print("INFO: processing ",mailbox.folder.get())


### if "run a job" , connect to API environment
if(ctm_folder > "") :
  set_environment = os.system("ctm environment set "  + ctm_env)
  print("ctm environment set " + ctm_env + "  ran with exit code %d" % set_environment)
  if (set_environment == 1) :
     print("ERROR ctm with environment ",ctm_env)
     sys.exit(3)

## Start the loop

while ( loop < timeout):
   print("LOOP: ",loop)
   try: 

#### search mails and mark it read 
      messages = mailbox.fetch(criteria=AND(seen=mail_unread,from_=mail_from,subject=mail_subject),
                           mark_seen=True,
                           bulk=True)
   except Exception as err:
      print(str(err))
      sys.exit(2)
   if (mail_from == "") :
      try: 
        messages = mailbox.fetch(criteria=AND(seen=mail_unread,subject=mail_subject),
                                  mark_seen=True,
                                  bulk=True)
      except Exception as err:
         print(str(err))
         sys.exit(2)
   
   aa=list(messages)

### parse the mails lists
   for msg in aa:
      msgcount=msgcount+1
      print(msg.from_, ': ',msg.subject, ' : ',msg.date_str)

### option: move the mail in an other folder
      if (mail_move>"") :
         if(mailbox.folder.exists(mail_move)) :
            mailbox.move(msg.uid,mail_move)
            print("MOVE: ",msg.uid," To ",mail_move)
         else :
            print("ERROR MOVE: ",msg.uid,' : ',mail_move,' does not exist')

### option: delete the mail      
      if(mail_delete) :
         mailbox.delete(msg.uid) 
         print("DELETE",msg.uid)

### option: save the attachments         
      if(mail_savefolder>"") :
         if(os.path.isdir(mail_savefolder)) :
            for att in msg.attachments:
               print(att.filename, att.content_type)  
               filepath=os.path.join(mail_savefolder,att.filename)
               with open(filepath,'wb') as f:
                  f.write(att.payload)
               print("INFO SAVE: ",att.filename,' To ',mail_savefolder)
         else :
           print("ERROR SAVE: ",msg.uid,' : ',mail_savefolder,' does not exist')

### if "run a job" , call API "run order job"  
      if(ctm_folder > "") :
         folder_job=ctm_folder + " " + job
         print("ctm  run order job "+folder_job)
         run_job = os.system("ctm run order "+ctm_env + " " + folder_job)
         print("ctm run order "+ctm_env + " " + folder_job + "  ran with exit code %d" % run_job)
         if (run_job == 1) :
           print("ERROR ctm with run order",folder_job)

### loop delay     
   time.sleep(delay)
   loop=loop + delay

### option: exit the loop if a mail has been found²
   if msgcount > 0 and mail_kill == 1 :
      break
print("END")

###  exit 100 if no mail has been found, thus the successor job is not triggered
if msgcount == 0:
   	print("No message matches search criteria")
   	sys.exit(100)
mailbox.logout()
sys.exit(0)
