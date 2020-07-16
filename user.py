from user.Korad import *
# function must be named 'func'

def func(on,off,voltage,current,device,status):
    if (on and off) :
        print("Error: non Clear Request")
        return 1
    if  Check_Serial_Connection(device) :
        return 1 
    if (status):
        Status=Get_Status(device)
        print("Device id is: "+GetID(device))
        print("Output Status is: "+OnOff_Str(Status))
        print("Actual Set Voltage: "+Get_V_Set(device)+" V")
        #if Status: print("Actual Delivered Voltage: "+Get_V_Delivered(device)+" V")
        #print("Actual Set Current: "+Get_I_Set('device')+" A")
        #if Status: print("Actual Delivered Current: "+Get_I_Delivered(device)+" A")
        #return 0
    if (on):
        if ((SetCurrent(device,current)==0) and (SetVoltage(device,voltage)==0)) :
            SetOP(device,1)
            return 0
        else :
            print("Error: could not set parameters")
            return 1
    if (off):
        SetOP(device,0)
        return 0   

