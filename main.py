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
	# Since there is an error, a correction factor is inserted to compensate.
	correction = 0.8
	return deg/(360 * 10 / 60 + correction)


def deg2timeRpm(deg, rpm): # this motor speed is 0~10RPM.
	# Since there is an error, a correction factor will be included (not yet calculated).
	correction = 0
	return deg/(360 * rpm / 60 + correction)

def cw():
	cwpin.duty_u16(0xFFFF)
	ccwpin.duty_u16(0)

def ccw():
	cwpin.duty_u16(0)
	ccwpin.duty_u16(0xFFFF)

def cw_rpm(rpm):
	rpm = rpm
	duty = int(rpm / 10 * 0xFFFF)
	cwpin.duty_u16(duty)
	ccwpin.duty_u16(0)

def ccw_rpm(rpm):
	rpm = rpm
	duty = int(rpm / 10 * 0xFFFF)
	cwpin.duty_u16(0)
	ccwpin.duty_u16(duty)

def brake():
	cwpin.duty_u16(0xFFFF)
	ccwpin.duty_u16(0xFFFF)
	print("rotation finish")

def wait_rotate(deg_list):
	deg = deg_list
	rotation_time = deg2time(deg)
	utime.sleep(rotation_time)

def wait_rotate_rpm(deg_list, rpm):
	deg = deg_list
	rotation_time = deg2timeRpm(deg, rpm)
	utime.sleep(rotation_time)


def check_param_float(param):
	try:
		param = float(param)
	except ValueError:
		print("Value error")
		return False
	else:
		return param

print("please input command and parameter.")
print("CW XXX [YYY]  rotation stage clockwise. XXX is degree(0~360). YYY is RPM(default 10RPM)")
print("CCW XXX [YYY] rotation stage counterclockwise. XXX is degree(0~360). YYY is RPM(default 10RPM)")

while True:
	commands = input()
	
	command_list = commands.split(" ")
	command_id = command_list[0]

	# print(len(command_list))
	# for arg: 0
	if(len(command_list)==1):
		if  command_id == "LON":	# for debug
			led.value(1)
			print("LED ON")

		elif command_id == "LOFF":	# for debug
			led.value(0)
			print("LED OFF")


	# for arg: 1
	elif(len(command_list)== 2):
		param1 = command_list[1]
		param1_float = check_param_float(param1)

		if command_id == "CW":
			if(param1_float == False):
				print("please input number for the second argument")
			else:
				print("rotating CW", param1_float, "deg")	
				led.value(1)

				cw()
				wait_rotate(param1_float)
				brake()
				led.value(0)


		elif command_id == "CCW":
			if(param1_float == False):
				print("please input number for the second argument")
			else:
				print("rotating CCW", param1_float, "deg")
				led.value(1)

				ccw()
				wait_rotate(param1_float)
				brake()
				led.value(0)


	# for arg: 2
	elif(len(command_list)== 3):
		param1 = command_list[1]
		param2 = command_list[2]
		param1_float = check_param_float(param1)
		param2_float = check_param_float(param2)

		if command_id == "CW":
			if(param1_float == False or param2_float == False):
				print("please input number for the second argument")
			
			else:
				print("rotating CW", param1_float, "deg at", param2_float, "RPM")	
				led.value(1)

				if(param2_float > 0 or param2_float < 10):
					cw_rpm(param2_float)
					wait_rotate_rpm(param1_float, param2_float)
					brake()
					led.value(0)
				else:
					print("please input RPM 0 ~ 10")


		elif command_id == "CCW":
			if(param1_float == False or param2_float == False):
				print("please input number for the second argument")
			
			else:
				print("rotating CCW", param1_float, "deg at", param2_float, "RPM")	
				led.value(1)

				if(param2_float > 0 or param2_float < 10):
					ccw_rpm(param2_float)
					wait_rotate_rpm(param1_float, param2_float)
					brake()
					led.value(0)
				else:
					print("please input RPM 0 ~ 10")

	
		# for arg > 2 (error cases)
		else:
			print("This is an undefined command id. Please retype it")