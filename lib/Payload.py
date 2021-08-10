#!/usr/bin/python


import random
import re


RN = "\r\n"
EndChunk = "0\r\n\r\n"
def Chunked(data):
	return hex(len(data))[2:]+RN+data+RN

class Payload():
	def __init__(self, host=None):
		self.header = None
		self.body = None
		self.method = "GET"
		self.endpoint = "/"
		self.host = host
		self.cl = -1

	def __str__(self):
		def replace_random(match):
			return str(random.random()).split('.')[1]


		if (self.header == None):
			raise AttributeError("No header data specified in Payload instance")
		if (self.body == None):
			raise AttributeError("No body data specified in Payload instance")
		if (self.host == None):
			raise AttributeError("No host specified in Payload instance")

                #                    \r\n
		result = self.header + RN + self.body
		result = re.sub("__RANDOM__",replace_random,result)

		if (self.cl < 0):
			result = re.sub("__REPLACE_CL__",str(len(self.body)),result)
		else:
			result = re.sub("__REPLACE_CL__",str(self.cl),result)

		result = re.sub("__METHOD__",self.method,result)
		result = re.sub("__ENDPOINT__",self.endpoint,result)
		result = re.sub("__HOST__",self.host,result)

		return (result)

	def __setattr__(self, name, value):
		if name == "body" and (type("string") != type(value) and value != None):
			raise AttributeError("Only string types allowed")
		if name == "header" and (type("string") != type(value) and value != None):
			raise AttributeError("Only string types allowed")
		if name == "host" and (type("string") != type(value) and value != None):
			raise AttributeError("Only string types allowed")
		self.__dict__[name] = value
