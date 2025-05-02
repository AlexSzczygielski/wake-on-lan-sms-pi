#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time
import subprocess
import configparser

#SETUP
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW)


#Serial port
try:
    ser = serial.Serial("/dev/ttyS0",115200)
    ser.flushInput()
except serial.SerialException as e:
    print(f"Serial port error: {e}")
    exit(1)


# Load config
config = configparser.ConfigParser()
config.read('/home/pi/Desktop/config.ini') #Change this to your file path


#definitions
powerKey = 6
macAddr = config['Settings']['mac_address']
telNumber = config['Settings']['trusted_number']
maxMessageMemory = int(config['Settings']['max_messages'])
#macAddr = '' #Set this to your devices' mac address
#telNumber = '' #Set this to number that will send key message in +.... format
#maxMessageMemory = 25 #Set this to number of messages that your SIM card can hold


#FUNCTIONS
def WakeOnLan(message):
	#Function responsible for magic packet
	if telNumber in message: #prevents unknown numbers access
		print(f'Received message from friendly number {telNumber}')
		print(f'Turning on the device {macAddr} by sending magic packet')
		subprocess.run(['wakeonlan', macAddr])
	else: print(f'Unknown number, abort')


def SendAt(command,timeout):
	#Function used for sending AT commands, then checks output through CheckResponse
	#Called by ReceiveShortMessage()
	rec_buff = ''
	decode = ''
	ser.write((command+'\r\n').encode()) #encode - txt to bytes, for serial
	time.sleep(timeout)


	#Check current response in serial
	if ser.inWaiting(): #checks if any bytes availavle to read
		time.sleep(0.01 )
		
		rec_buff = ser.read(ser.inWaiting()) #read available bytes
		decode = rec_buff.decode() #decode - bytes to txt
		print(decode)

	return decode
	
	
def ClearMessages():
	# Deletes SMS messages from slot 1 to max
	print(f'Clearing SMS messages (slots 1–{maxMessageMemory-1})')
	for i in range(1, maxMessageMemory):
		SendAt(f'AT+CMGD={i}', 0.5)
	time.sleep(1)
	print('Messages cleared.')


def ReceiveShortMessage():
	#This function monitors SMS input constantly
	print('Check SMS')
	message = ''
	message = SendAt('AT+CMGL="REC UNREAD"', 1) #Show all unread messages

	if message != '':
		if 'on' in message:
			WakeOnLan(message)

	if '+SMS FULL' in message:
		print("Full SIM memory detected, deleting ALL SMS messages")
		ClearMessages() #Comment this out if you don't want to clear messages


def power_on(powerKey):
	print('SIM7600X is starting:')
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(powerKey,GPIO.OUT)
	time.sleep(0.1)
	GPIO.output(powerKey,GPIO.HIGH)
	time.sleep(2)
	GPIO.output(powerKey,GPIO.LOW)
	time.sleep(20)
	ser.flushInput()
	print('SIM7600X is ready')

def power_down(powerKey): #not used here
	print('SIM7600X is loging off:')
	GPIO.output(powerKey,GPIO.HIGH)
	time.sleep(3)
	GPIO.output(powerKey,GPIO.LOW)
	time.sleep(18)
	print('Good bye')

#MAIN PROGRAM:
#power_on(powerKey)
SendAt('AT+CMGF=1', 1) #Set SMS mode to text
while True:
	ReceiveShortMessage()
	time.sleep(5)  # Avoid CPU hammering