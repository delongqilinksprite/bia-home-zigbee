#!/usr/bin/env python 
# Filename : zigbee_test.py
# Author : Derron 
# Mail : delong.qi@linksprite.com
# Date : 2016.11.30


import sys
import time
import Zigbee

# set debug = 1,and then you can see zigbee log
# ser_dev : serial nodes  
debug = 0
ser_dev = "/dev/ttyS1"
zigbee = Zigbee.Zigbee(ser_dev,debug)


def main():
	while True:
		msg = zigbee.alarm()
		if msg != '1':
			print msg		
		time.sleep(0.1)


if __name__ == '__main__':
	print 'Version:' + zigbee.version
	handle = '1234'
	time_second  = 110
	try:
		if sys.argv[1] == 'add':
			msg = zigbee.add()
			print msg
			main()
		if sys.argv[1] == 'config':
			msg = zigbee.config(handle,time_second)
			print msg
			main()
		if sys.argv[1] == 'remove':
			msg = zigbee.remove(handle)
			print msg
			main()
		if sys.argv[1] == 'add_tmp_hum':
			msg = zigbee.add_tmp_hum()
			print msg
			main()
		else:
			main()
	except KeyboardInterrupt:
		print "\nGoodBye!"
		zigbee.ser.close()
		exit()
