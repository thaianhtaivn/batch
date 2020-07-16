import configparser
import subprocess
import os
import sys
# pm.exe -[on | off] -device name -socket name 
# Examples: 

# "C:\Program Files\Eneregenie\Power Manager\pm.exe" -on -EG-PM -Socket1 
# "E:\Utils\PM3\pm.exe" -off -My EG-PM -Table lamp 
# Execute pm.exe with -info key to get the complete information on current devices states. For each of the connected devices the following information is provided and available from Info.ini file on Desktop: 

# DeviceName - the user specified device name; 
# Socket#name, where # is replaced by a certain socket number - the user specified socket name; 
# Socket#SwitchState, where # is replaced by a certain socket number - TRUE, when the socket is switched on, FALSE, when the socket is switched off; 
# Socket#VoltageState, where # is replaced by a certain socket number - TRUE, when voltage presence on the socket is detected, FALSE, when there is no voltage on the socket; 


def Get_PM_Info(pm_path) :
   if os.path.exists(pm_path) :
      subprocess.call([pm_path,"-info"]) #generate info file
   else :
      print("Error: "+ pm_path + " not found \n check Power Manager installation!")
      sys.exit(-1)
   info_file=os.path.join(os.environ["USERPROFILE"], "Desktop","info.ini")
   if os.path.exists(info_file) :
      config=configparser.ConfigParser()
      config.read(info_file)
      return config
   else :
      print("Error: No Info file from pm.exe")
      sys.exit(-1)
      
def Get_Device_List(pm_path) :
   info=Get_PM_Info(pm_path)
   sections=info.sections()
   device_list=[]
   for s in sections : device_list.append(info[s] ["DeviceName"])
   return device_list
   
def Print_Device_State(pm_path,device):
   info=Get_PM_Info(pm_path)
   device_list=Get_Device_List(pm_path)
   if device in device_list :
      print ("Name: "+device)
      dev=info[info.sections()[device_list.index(device)]]
      for i in range(0,4):
         print("\nSocket "+ str(i)+" :")
         print ("Name = "+ dev["Socket"+str(i)+"Name"] )
         if (dev["Socket"+str(i)+"SwitchState"] == "TRUE") :
            print ("State = ON")
         else :
            print ("State = OFF")
      return 0      
   else:
      print("Error: Device Not Found ") 
      sys.exit(-1)   

def Set_Socket_State(pm_path,device,socket,state) :
   info=Get_PM_Info(pm_path)
   device_list=Get_Device_List(pm_path)
   if device in device_list :
      dev=info[info.sections()[device_list.index(device)]]
      if socket=="all" :
         for i in range(0,4):
            if state:
               subprocess.call([pm_path,"-on","-"+device,"-"+dev["Socket"+str(i)+"Name"]])
            else :
               subprocess.call([pm_path,"-off","-"+device,"-"+dev["Socket"+str(i)+"Name"]])
         return 0
      for i in range(0,4):
         if (dev["Socket"+str(i)+"Name"] == socket):
            if state:
               subprocess.call([pm_path,"-on","-"+device,"-"+socket])
            else :
               subprocess.call([pm_path,"-off","-"+device,"-"+socket])
            return 0
      print("Error: Socket Not Found")
      sys.exit(-1)
   else:
      print("Error: Device Not Found ") 
      sys.exit(-1)  
