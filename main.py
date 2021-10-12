# from typing import Coroutine
from machine import Pin, PWM, Timer
import utime

led = Pin(25, Pin.OUT)
cwpin = PWM(Pin(26, Pin.OUT))
ccwpin = PWM(Pin(27, Pin.OUT))

frequency = 20000 # 20kHz
cwpin.freq(int(frequency))
ccwpin.freq(int(frequency))

def deg2time(deg): # this motor speed is 10RPM.
	# 若干誤差があるため、補正係数(実測により求めた)を入れる
	correction = 0.8
	return deg/(60 + correction)

def cw():
	cwpin.duty_u16(0x8000)
	ccwpin.duty_u16(0)

def ccw():
	cwpin.duty_u16(0)
	ccwpin.duty_u16(0xFFFF)

def brake():
	cwpin.duty_u16(0xFFFF)
	ccwpin.duty_u16(0xFFFF)

def wait_rotate(deg_list):
	deg = float(deg_list)
	rotation_time = deg2time(deg)
	utime.sleep(rotation_time)



print("please input command and parameter.")
print("CW XXX   rotation stage clockwise. XXX is degree(0~360)")
print("CCW XXX  rotation stage counterclockwise. XXX is degree(0~360)")
print("The rotation default speed of this motor is 10RPM.")

while True:
	commands = input()
	
	command_list = commands.split(" ")
	command_id = command_list[0]
	if(len(command_list)<1):
		if  command_id == "LON":	# for debug
			led.value(1)
			print("LED ON")

		elif command_id == "LOFF":	# for debug
			led.value(0)
			print("LED OFF")

	else:
		if command_id == "CW":
			if(command_list[1].isdigit()):
				print("rotating CW", command_list[1])	
				led.value(1)

				# 　ここに時計回りの動作を記入する
				cw()
				wait_rotate(command_list[1])
				brake()
				led.value(0)
			else:
				print("please input number for the second argument")


		elif command_id == "CCW":
			if(command_list[1].isdigit()):
				print("rotating CCW", command_list[1])
				led.value(1)

				# 　ここに反時計回りの動作を記入する
				ccw()
				wait_rotate(command_list[1])
				brake()
				led.value(0)
			else:
				print("please input number for the second argument")


		else:
			print("This is an undefined command id. Please retype it")