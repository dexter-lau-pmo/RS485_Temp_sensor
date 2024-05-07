# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 16:57:21 2024

@author: craps
"""

#TEST FILE ONLY! NOT USED
import serial

import time

import serial.tools.list_ports


# Get a list of available serial ports
ports = serial.tools.list_ports.comports()

# Print information about each port
for port in ports:
    print(port.device, port.name, port.description)
    

temp_ref_frame = [0x01, 0x04, 0x00, 0x01, 0x00, 0x01, 0x60, 0x0a] # Request frame for temp sensor
humid_ref_frame = [0x01, 0x04, 0x00, 0x02, 0x00, 0x01, 0x90, 0x0a] # Request frame for humidity sensor



ser = serial.Serial(port=port.device, baudrate=9600, timeout=1.0) # Remember, you might need to replace '/dev/ttyUSB0' with the port name where your USB to RS485 converter is connected

def get_temp():
    
  print("Fetch temp")
  ser.write(bytes(temp_ref_frame))

  time.sleep(1)

  buf = ser.read(7)
  print(buf)
  if buf:
      temp_value = (buf[3] << 8) | buf[4]

  temperature = temp_value / 10.0

  return temperature





def get_humidity():
  print("Fetch humidity")
  ser.write(bytes(humid_ref_frame))

  time.sleep(1)

  buf = ser.read(7)

  humid_value = (buf[3] << 8) | buf[4]

  humidity = humid_value / 10.0

  return humidity





while True:



  print("-----------------------------------------------")

  print("Temp: ", get_temp())

  time.sleep(3)



  print("-----------------------------------------------")

  print("Humidity: " , get_humidity())

  time.sleep(3)
  
  ser.close()
  break
  
