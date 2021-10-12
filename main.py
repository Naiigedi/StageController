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
	return deg/(360 * 10 / 60 + correction)


def deg2timeRpm(deg, rpm): # this motor speed is 0~10RPM.
	# 若干誤差があるため、補正係数を入れる予定（未計算）
	correction = 0
	return deg/(360 * int(rpm) / 60 + correction)

def cw():
	cwpin.duty_u16(0xFFFF)
	ccwpin.duty_u16(0)

def ccw():
	cwpin.duty_u16(0)
	ccwpin.duty_u16(0xFFFF)

def cw_rpm(rpm):
	rpm = int(rpm)
	duty = int(rpm / 10 * 0xFFFF)
	cwpin.duty_u16(duty)
	ccwpin.duty_u16(0)

def ccw_rpm(rpm):
	rpm = int(rpm)
	duty = int(rpm / 10 * 0xFFFF)
	cwpin.duty_u16(0)
	ccwpin.duty_u16(duty)

def brake():
	cwpin.duty_u16(0xFFFF)
	ccwpin.duty_u16(0xFFFF)

def wait_rotate(deg_list):
	deg = float(deg_list)
	rotation_time = deg2time(deg)
	utime.sleep(rotation_time)

def wait_rotate_rpm(deg_list, rpm):
	deg = float(deg_list)
	rotation_time = deg2timeRpm(deg, rpm)
	utime.sleep(rotation_time)


print("please input command and parameter.")
print("CW XXX [YYY]  rotation stage clockwise. XXX is degree(0~360). YYY is RPM(default 10RPM)")
print("CCW XXX [YYY] rotation stage counterclockwise. XXX is degree(0~360). YYY is RPM(default 10RPM)")

while True:
	commands = input()
	
	command_list = commands.split(" ")
	command_id = command_list[0]

	print(len(command_list))
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


	# for arg: 2
	elif(len(command_list)== 3):
		param1 = command_list[1]
		param2 = command_list[2]

		if command_id == "CW":
			if(param1.isdigit() and param2.isdigit()):
				print("rotating CW", param1)	
				led.value(1)

				# 　ここに時計回りの動作を記入する
				if(float(param2) > 0 or float(param2) < 10):
					cw_rpm(param2)
					wait_rotate_rpm(param1,param2)
					brake()
					led.value(0)
				else:
					print("please input RPM 0 ~ 10")
			else:
				print("please input number for the second argument")


		elif command_id == "CCW":
			if(param1.isdigit() and param2.isdigit()):
				print("rotating CCW", param1)
				led.value(1)

				# 　ここに時計回りの動作を記入する
				if(float(param2) > 0 or float(param2) < 10):
					ccw_rpm(param2)
					wait_rotate_rpm(param1,param2)
					brake()
					led.value(0)
				else:
					print("please input RPM 0 ~ 10")
			else:
				print("please input number for the second argument")

	
		# for arg > 2 (error cases)
		else:
			print("This is an undefined command id. Please retype it")