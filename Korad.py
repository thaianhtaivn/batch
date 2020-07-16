##Modules##
import serial                  #Manages serial connectivity between PC and instrument  
import time                    #Implements delays
import binascii                #Translates power supply STATUS query from ascii to binary 
import io
import sys
import argparse

#==============================================================================
# Define protocol commands
#==============================================================================



REQUEST_SET_VOLTAGE = b"VSET1?"  # request the set voltage
REQUEST_SET_CURRENT = b"ISET1?"  # Request the set current

SET_VOLTAGE = b"VSET1:"  # Set the  output voltage
SET_CURRENT = b"ISET1:"  # Set the output current

SET_OUTPUT = b"OUT"  # Enable(1)/Disable(0) the power output

REQUEST_STATUS = b"STATUS?"  # Request POWER SUPPLY status:
                             #
                             # Contents 8 bits in the following format
                             # Bit Item Description
                             # 0 CH1 0=CC mode, 1=CV mode
                             # 1 CH2 0=CC mode, 1=CV mode
                             # 2, 3 Tracking 00=Independent, 01=Tracking series,11=Tracking parallel
                             # 4 Beep 0=Off, 1=On
                             # 5 Lock 0=Lock, 1=Unlock
                             # 6 Output 0=Off, 1=On
                             # 7 N/A N/A
                             #
REQUEST_ID = b"*IDN?" #Returns the KA3005P identification (Manufacturer, model name,).
REQUEST_ACTUAL_VOLTAGE = b"VOUT1?"  # Request real output voltage
REQUEST_ACTUAL_CURRENT = b"IOUT1?"  # Requst the real output current
#SET_OVP = b"OVP"  # Enable(1)/Disable(0) OverVoltageProtection
#SET_OCP = b"OCP"  # Enable(1)/Disable(0) OverCurrentProtection
#==============================================================================
# Methods
#==============================================================================
#==============================================================================
# Variables
#==============================================================================
VMAX = "12"
IMAX = "2.5"

def isfloat(x):
    try:
        float(x)
        return True
    except:
        return False

def GetID(device):
    PS = serial.Serial(device,
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    PS.write(REQUEST_ID)  # Request the ID from the Power Supply
    PSID = str(PS.read(16))[2:-1]
    PS.flushInput()
    PS.close()
    return(PSID)

def Get_I_Set(device):
    PS = serial.Serial(device,
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    PS.write(REQUEST_SET_CURRENT)  # Request the target current
    I_set = str(PS.read(5))[2:-1]
    PS.flushInput()
    PS.close()
    return(I_set)


def Get_V_Set(device):
    PS = serial.Serial(device,
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    PS.write(REQUEST_SET_VOLTAGE)  # Request the target voltage
    V_set = str(PS.read(5))[2:-1]
    PS.flushInput()
    PS.close()
    return(V_set)


def Get_Status(device):
    PS = serial.Serial(device,
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    PS.write(REQUEST_STATUS)  # Request the status of the PS
    Stat = PS.read(5).hex()
    st=Stat
    output=int(st,16) & 0x40 #check if output power is on or off
    PS.flushInput()
    PS.close()
    if output :
        return 1
    return 0
        


def SetVoltage(device,voltage):
    if not isfloat(voltage):
        print("Error: voltage value is not a float")
        return 1
    PS = serial.Serial(device,
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    if (float(voltage) > float(VMAX)):
        voltage = VMAX
    voltage = "{:2.2f}".format(float(voltage))
    Output_string = SET_VOLTAGE + bytes(voltage, "utf-8")
    PS.write(Output_string)
    PS.flushInput()
    PS.close()
    time.sleep(0.5)
    VeriVolt = "{:2.2f}".format(float(Get_V_Set(device)))  # Verify PS accepted
    if (VeriVolt != voltage):
        print ("ERROR: Voltage was not set correctly")
        return 1
    else :
        return 0


def SetCurrent(device,current):
    if not isfloat(current):
        print("Error: voltage value is not a float")
        return 1
    PS = serial.Serial(device,
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    if (float(current) > float(IMAX)):
        current = IMAX
    current = "{:2.2f}".format(float(current))
    Output_string = SET_CURRENT + bytes(current, "utf-8")
    PS.write(Output_string)
    PS.flushInput()
    PS.close()
    time.sleep(0.5)
    VeriAmp = "{:2.2f}".format(float(Get_I_Set(device)))
    if (VeriAmp != current):
        print ("ERROR: Current was not set correctly")
        return 1
    else :
        return 0


def Get_V_Delivered(device):
    PS = serial.Serial(device,
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    PS.write(REQUEST_ACTUAL_VOLTAGE)  # Request the actual voltage
    V_actual = str(PS.read(5))[2:-1]
    PS.flushInput()
    PS.close()
    return(V_actual)


def Get_I_Delivered(device):
    PS = serial.Serial(device,
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    PS.write(REQUEST_ACTUAL_CURRENT)  # Request the actual current
    time.sleep(0.015)
    I_actual =str(PS.read(5))[2:-1]
    PS.flushInput()
    PS.close()
    return(I_actual)


def SetOP(device,OnOff):
    PS = serial.Serial(device,
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()

    Output_string = SET_OUTPUT + bytes(str(OnOff), "utf-8")
    PS.write(Output_string)
    PS.flushInput()
    PS.close()
    return 0
    
def Check_Serial_Connection(device) :
    PS = serial.Serial(device,
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    if(PS.isOpen() == False):
        print("Error: Device unreacheble")
        return 1
    else :
        PS.close()
        return 0    
        

def OnOff_Str(val):
    if (val==1) :
        return "ON"
    elif (val==0) :
        return "OFF"
    else:
        return "ERROR"
		

