#!/usr/bin/env python 
# Filename : Zigbee.py
# Author : Derron 
# Mail : delong.qi@linksprite.com
# Date : 2016.11.30

import re
import os
import sys
import time
import json
import string
import serial
import binascii
import datetime

# if you want to see debug message , set self.debug = 1
class Zigbee:
	def __init__(self,dev,debug):
		self.debug = debug
		self.dev = dev
		self.version = '0.2'
		ser = serial.Serial(self.dev, 115200,timeout = 1)
		if ser.isOpen() == True:
			if self.debug == 1:
				print "open serial success!"
			self.ser = ser;
		else:
			if self.debug == 1:
				print "open serial failure!"
			return '1'
	
	# Function:string to hex		
	def hexShow(self,argv):
		result = ''
		hLen = len(argv)
		for i in xrange(hLen):
			hvol = ord(argv[i])
			hhex = '%02x'%hvol
			result += hhex+' '
		return result
	
	# Function:sensor register to zigbee gateway  	
	def register(self):
		start = datetime.datetime.now()
		while True:
			self.ser.write('\x02')
			self.ser.write('\x75')
			self.ser.write('\x1e')
			try:
				data = self.ser.readline()
			except Exception:
				data ='0';
			val=self.hexShow(data)
			leng = len(val)
			finsh = datetime.datetime.now()
			tim = (finsh-start).seconds
			if tim > 14:
				if self.debug == 1:
					print "register timeout!"
				return '1'
			if leng > 45:
				a = val.find("0e fc 02 e1",1)
				if a != -1:
					b=a+12
					mac = val[b:b+29]
					if self.debug == 1:
						print "register success!"
					return mac
					
	# Function:set target input handle
	def set_target(self,handle):
		start = datetime.datetime.now()
		send = "0c fc 02 01 04 01 01 01 02"+handle+"02 0a"
		s = send.replace(' ','')
		a=binascii.a2b_hex(s)
		while True:
			self.ser.write(a)
			try:
				recv=self.ser.readline()
			except Exception:
				recv = '0'
			rec=self.hexShow(recv)
			finsh = datetime.datetime.now()
			tim = (finsh - start).seconds
			if tim > 5:
				if self.debug == 1:
					print "set target timeout!"
				return '1'
			a = rec.find("04 fd 02 01",0)
			if a != -1:
				if self.debug == 1:
					print "set target success!"
				return '0'
		
	def set_target_tmp(self,handle):
		start = datetime.datetime.now()
		send = "0c fc 02 01 04 01 01 01 02"+handle+"02 0a"
		s = send.replace(' ','')
		a=binascii.a2b_hex(s)
		while True:
			self.ser.write(a)
			try:
				recv=self.ser.readline()
			except Exception:
				recv = '0'
			rec=self.hexShow(recv)
			finsh = datetime.datetime.now()
			tim = (finsh - start).seconds
			if tim > 5:
				if self.debug == 1:
					print "set target to tmp timeout!"
				return '1'
			a = rec.find("04 fd 02 01",0)
			if a != -1:
				if self.debug == 1:
					print "set target to tmp success!"
				return '0'

	def set_target_hum(self,handle):
		start = datetime.datetime.now()
		send = "0c fc 02 01 04 01 01 02 02"+handle+"02 0a"
		s = send.replace(' ','')
		a=binascii.a2b_hex(s)
		while True:
			self.ser.write(a)
			try:
				recv=self.ser.readline()
			except Exception:
				recv = '0'
			rec=self.hexShow(recv)
			finsh = datetime.datetime.now()
			tim = (finsh - start).seconds
			if tim > 5:
				if self.debug == 1:
					print "set target to hum timeout!"
				return '1'
			a = rec.find("04 fd 02 01",0)
			if a != -1:
				if self.debug == 1:
					print "set target to hum success!"
				return '0'
			
	# Function:get gateway mac address
	def gateway_mac(self):
		start = datetime.datetime.now()
		while True:
			self.ser.write('\x02')
			self.ser.write('\x14')
			self.ser.write('\x6f')
			try:
				data = self.ser.readline()
			except Exception:
				data = '0'
			dat = self.hexShow(data)
			leng = len(dat)
			finsh = datetime.datetime.now()
			tim = (finsh - start).seconds
			if tim > 5:
				if self.debug == 1:
					print "get gateway mac timeout!"
				return '1'
			if leng > 30:
				a = dat.find("0c 15 00 6f",0)
				if a != -1:
					dt = dat[15:38]
					return dt

	# Function:bind sensor with sensor gateway
	def bind(self,eq_mac,gat_mac):
		start = datetime.datetime.now()
		send = "16 d8"+eq_mac+"01 01 00 03"+gat_mac+"01"
		s = send.replace(' ','')
		a=binascii.a2b_hex(s)
		while True:
			self.ser.write(a)
			try:
				recv=self.ser.readline()
			except Exception:
				recv = '0'
			rec=self.hexShow(recv)
			finsh = datetime.datetime.now()
			tim = (finsh - start).seconds
			if tim > 8:
				if self.debug == 1:
					print "bind timeout!"
				return '1'
			b = rec.find("02 d9 00")
			if b != -1:
				if self.debug == 1:
					print "bind success!"
				return '0'

	def bind_tmp(self,eq_mac,gat_mac):
		start = datetime.datetime.now()
		send = "16 d8"+eq_mac+"01 02 04 03"+gat_mac+"01"
		s = send.replace(' ','')
		a=binascii.a2b_hex(s)
		while True:
			self.ser.write(a)
			try:
				recv=self.ser.readline()
			except Exception:
				recv = '0'
			rec=self.hexShow(recv)
			finsh = datetime.datetime.now()
			tim = (finsh - start).seconds
			if tim > 8:
				if self.debug == 1:
					print "bind tmp timeout!"
				return '1'
			b = rec.find("02 d9 00")
			if b != -1:
				if self.debug == 1:
					print "bind tmp success!"
				return '0'

	def bind_hum(self,eq_mac,gat_mac):
		start = datetime.datetime.now()
		send = "16 d8"+eq_mac+"02 05 04 03"+gat_mac+"01"
		s = send.replace(' ','')
		a=binascii.a2b_hex(s)
		while True:
			self.ser.write(a)
			try:
				recv=self.ser.readline()
			except Exception:
				recv = '0'
			rec=self.hexShow(recv)
			finsh = datetime.datetime.now()
			tim = (finsh - start).seconds
			if tim > 8:
				if self.debug == 1:
					print "bind hum timeout!"
				return '1'
			b = rec.find("02 d9 00")
			if b != -1:
				if self.debug == 1:
					print "bind hum success!"
				return '0'
	
	# Function:cluster
	def cluster(self):
		start = datetime.datetime.now()
		send = "08 FC 00 00 05 00 01 01 00"
		s = send.replace(' ','')
		a=binascii.a2b_hex(s)
		while True:
			self.ser.write(a)
			try:
				recv=self.ser.readline()
			except Exception:
				recv = '0'
			rec=self.hexShow(recv)
			leng = len(rec)
			finsh = datetime.datetime.now()
			tim = (finsh - start).seconds
			if tim > 5:
				if self.debug == 1:
					print "cluster timeout!"
				return '1'
			if leng > 30:
				b = rec.find("0b fe 03")
				if b != -1:
					if self.debug == 1:
						print "cluster success!"
					return rec[b+30:b+35]
					
	# Function:battery report ,input time is second
	def report(self,time):
		start = datetime.datetime.now()
		send = "11 FC 00 01 00 06 01 00 21 00 20"+time+"01 00 00"
		s = send.replace(' ','')
		a=binascii.a2b_hex(s)
		while True:
			self.ser.write(a)
			try:
				recv=self.ser.readline()
			except Exception:
				recv = '0'
			rec=self.hexShow(recv)
			leng = len(rec)
			finsh = datetime.datetime.now()
			tim = (finsh - start).seconds
			if tim > 5:
				if self.debug == 1:
					print "report timeout!"
				return '1'
			if leng > 15:
				b = rec.find("06 fd 00")
				if b != -1:
					if self.debug == 1:
						print "report success!"
					return '0'

	def report_tmp(self):
		start = datetime.datetime.now()
		send = "11 FC 00 02 04 06 01 00 00 00 29 05 00 05 00 01 00 00"
		s = send.replace(' ','')
		a=binascii.a2b_hex(s)
		while True:
			self.ser.write(a)
			try:
				recv=self.ser.readline()
			except Exception:
				recv = '0'
			rec=self.hexShow(recv)
			leng = len(rec)
			finsh = datetime.datetime.now()
			tim = (finsh - start).seconds
			if tim > 5:
				if self.debug == 1:
					print "report tmp timeout!"
				return '1'
			if leng > 15:
				b = rec.find("06 fd 00")
				if b != -1:
					if self.debug == 1:
						print "report tmp success!"
					return '0'

	def report_hum(self):
		start = datetime.datetime.now()
		send = "11 FC 00 05 04 06 01 00 00 00 21 05 00 05 00 01 00 00"
		s = send.replace(' ','')
		a=binascii.a2b_hex(s)
		while True:
			self.ser.write(a)
			try:
				recv=self.ser.readline()
			except Exception:
				recv = '0'
			rec=self.hexShow(recv)
			leng = len(rec)
			finsh = datetime.datetime.now()
			tim = (finsh - start).seconds
			if tim > 5:
				if self.debug == 1:
					print "report hum timeout!"
				return '1'
			if leng > 15:
				b = rec.find("06 fd 00")
				if b != -1:
					if self.debug == 1:
						print "report hum success!"
					return '0'
					
	# config battery level report time				
	def config(self,handle,tim):
		mm = {}
		tim1 = tim + 5
		tim  = format(tim,'04x')
		tim1 = format(tim1,'04x')
		tim_t = str(tim) + str(tim1)
		print tim_t
		a=self.gateway_mac()
		if a != '1':
			c = self.bind(handle,a)
			if c != '1':
				d = self.report(tim_t)
				if d != '1':
					mm["handle"] = handle
					mm["message"] = 'success'
					msg = json.dumps(mm)
					if self.debug == 1:
						print msg
					return msg
		mm["message"] = 'failed'
		msg = json.dumps(mm)
		if self.debug == 1:
			print msg
		return msg
		
	# remove sensor form zigbee gateway
	def remove(self,handle):
		mm = {}
		start = datetime.datetime.now()
		send = "0c e4 00 00 00 00 00 00 00 00 00"+ handle
		s = send.replace(' ','')
		a=binascii.a2b_hex(s)
		start = datetime.datetime.now()
		while True:
			self.ser.write(a)
			try:
				recv=self.ser.readline()
			except Exception:
				recv = '0'
			rec=self.hexShow(recv)
			finsh = datetime.datetime.now()
			tim = (finsh - start).seconds
			if tim > 14:
				mm['message'] = 'failed'
				msg = json.dumps(mm)
				if self.debug == 1:
					print msg
				return msg
			c = rec.find("c9 43 50")
			if c != -1:
				mm["handle"] = handle
				mm["message"] = 'success'
				msg = json.dumps(mm)
				if self.debug == 1:
					print msg
				return msg
			time.sleep(0.1)
   
	# get the zigbee message (battery messag and alarm message)
	def alarm(self):
		mm = {}
		try:
			recv = self.ser.readline()
		except Exception:
			recv = '0'
		val = self.hexShow(recv)
		leng = len(val)
		if leng >= 30:
			po = val.find("fe 01")
			pz = val.find("00 21 00 20")
			pa = val.find("01 02",0)
			pb = val.find("02 02",0)
			try:
				if po != -1:
					handle = val[po+21:po+26]
					handle = handle.replace(' ','')
					sta = val[po+46]
					mm["msg"] = "alarm"
					mm["handle"] = handle
					mm["value"] = sta
					msg = json.dumps(mm)
					if self.debug == 1:
						print msg
					return msg
				if pz != -1:
					aa = val[pz+12:pz+14]
					short = val[pz-21:pz-16]
					handle = short.replace(' ','')
					level = int(aa,16)/2
					level = str(level)
					mm["msg"] = "power"
					mm["handle"] = handle
					mm["value"] = level
					msg = json.dumps(mm) 
					if self.debug == 1:
						print msg
					return msg
				if pa != -1:
					tmp = val[a+39:a+44].replace(' ','')
					t = "0x" + tmp[2:4] + tmp[0:2]
					temp = int(t,16)
					tem = temp/100.0
					mm["msg"] = "temperature"
					#mm["handle"] = handle
					mm["value"] = tem
					msg = json.dumps(mm)
					if self.debug == 1:
						print msg
					return msg
				if pb != -1:
					hum = val[b+39:b+44].replace(' ','')
					h= "0x" + hum[2:4] + hum[0:2]
					temp = int(h,16)
					hum = temp/100.0
					mm["msg"] = "humidity"
					#mm["handle"] = handle
					mm["value"] = hum
					msg = json.dumps(mm)
					if self.debug == 1:
						print msg
					return msg
			except Exception:
				pass
		return '1'
		
    # This step include register,gateway_mac,set_target,bind...,some sensor is not fit this 	
	def add(self):
		mm = {}
		val=self.register()
		if val != '1':
			short = val[0:5]
			mac = val[6:29]
			mac = mac.replace(' ','')
			short = short.replace(' ','')
			gatmac = self.gateway_mac()
			gatmac = gatmac.replace(' ','')
			if gatmac != '1':
				gatemac = gatmac
				a = self.set_target(short)
				if a != '1':
					b = self.bind(mac,gatemac)
					if b != '1':
						c = self.cluster()
						if c != '1':
							zone_type = c
							zone_type = zone_type.replace(' ','')
							mm["handle"] = short
							mm["mac"] = mac 
							mm["gatewaymac"] = gatmac
							mm["type"] = zone_type
							msg = json.dumps(mm);
							if self.debug == 1:
								print "add sensor ok"
								print msg
							return msg
			mm["message"] = "failed"
			msg = json.dumps(mm)
			if self.debug == 1:
				print msg
			return msg

	def add_tmp_hum(self):
		mm = {}
		val=self.register()
		if val != 1:
			short = val[0:5]
			mac = val[6:29]
			mac = mac.replace(' ','')
			short = short.replace(' ','')
			gatmac = self.gateway_mac()
			gatmac = gatmac.replace(' ','')
			if gatmac != '1':
				gatemac = gatmac
				a = self.set_target_tmp(short)
				if a != '1':
					b = self.bind_tmp(mac,gatemac)
					if b != '1':
						c = self.report_tmp()
						if c != '1':
							d = self.set_target_tmp(short)
							if d != '1':
								e = self.bind_tmp(mac,gatemac)
								if e != '1':
									f = self.report_tmp()
									if f != '1':
										mm["handle"] = short
										mm["mac"] = mac 
										mm["gatewaymac"] = gatmac
										msg = json.dumps(mm);
										if self.debug == 1:
											print "add sensor ok"
											print msg
										return msg
		mm["message"] = "failed"
		msg = json.dumps(mm)
		if self.debug == 1:
			print msg
		return msg
		
# End of Zigbee.py module	
