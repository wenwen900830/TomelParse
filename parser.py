# -*- encoding: utf8 -*-
from datetime import datetime as dt
import re
import sys
from reader import Reader
import json
from xmlHandler import Converter
import os
relativePath = os.path.dirname(__file__)
class Parser(object):

	def __init__(self, input, asJson=False, pedantic=True):
		self._asJson = asJson
		self._is_pedantic = pedantic
		self.reader = Reader(input)
		self.runtime = dict()
		self.kgObj = self.runtime
		self.mainLoop()

	def loadKeyGroup(self, keygroup):
		cg = self.runtime
		nlist = keygroup.split('.')
		for index, name in enumerate(nlist):
			if not name:
				raise Exception("Unexpected emtpy symbol in %s" % keygroup)
			elif not name in cg:
				cg[name] = dict()
			elif isinstance(cg[name], dict) and index == len(nlist)-1 and self._is_pedantic:
				raise Exception("Duplicated keygroup definition: %s" % keygroup)
			cg = cg[name]
		self.kgObj = cg

	def parseEXP(self):
		ISO8601 = re.compile(r'^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}Z$')
		FLOAT = re.compile(r'^[+-]?\d(>?\.\d+)?$')
		STRING = re.compile(r'(?:".*?[^\\]?")|(?:\'.*?[^\\]?\')')

		token = self.reader.custom_next()
		if token == '[':
		# Array
			array = []
			self.reader.skip('[')
			while self.reader.top() != ']':
				array.append(self.parseEXP())
				if len(array) > 1 and self._is_pedantic\
				   and type(array[-1]) != type(array[0]):
					raise Exception("Array of mixed data types.")
				if self.reader.custom_next() != ',':
					break
				self.reader.skip( ",")
			self.reader.allownl()
			self.reader.skip("]")
			return array
		elif STRING.match(token):
		# String
			return self.reader.pop()[1:-1].decode('string-escape')
		elif token in ('true', 'false'):
		# Boolean
			return {'true': True, 'false': False}[self.reader.pop()]
		elif token.isdigit() or token[1:].isdigit() and token[0] in ('+', '-'):
		# Integer
			return int(self.reader.pop())
		elif FLOAT.match(token):
		# Float
			return float(self.reader.pop())
		elif ISO8601.match(token):
		# Date
			date = dt.strptime(self.reader.pop(), "%Y-%m-%dT%H:%M:%SZ")
			return dt.strftime(date,"%Y-%m-%dT%H:%M:%SZ")
		raise Exception("Invalid token: %s" % token)

	def parseCOMMENT(self):
		pass
	
	def parseKEYGROUP(self):
		symbol = self.reader.pop()[1:-1]
		if not symbol or symbol.isspace():
			raise Exception("Empty keygroup found.")
		self.loadKeyGroup(symbol)
	
	def parseASSIGN(self):
		var = self.reader.pop()
		self.reader.pop(expect='=')
		val = self.parseEXP()
		if self.kgObj.get(var):
			raise Exception("Cannot rewrite variable: %s" % var)
		self.kgObj[var] = val

	def mainLoop(self):
		while self.reader._readNextLine():
			token = self.reader.custom_next()
			if token == "#":
				self.parseCOMMENT()   #continue
			elif token[0] == "[":
				self.parseKEYGROUP()
			elif re.match(r'[^\W\d_]', token, re.U):
				self.parseASSIGN()
			else:
				raise Exception("Unrecognized token: %s" % token)
			self.reader.assertEOL()

examplePath = relativePath + "\\example.toml"
parser = Parser(examplePath)
con = Converter.collectionToXML(parser.runtime)
sys.stdout.write(Converter.getXmlString(con))
print "hello"
