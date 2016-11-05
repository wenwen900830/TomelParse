# -*- encoding: utf8 -*-
import os
import sys
relativePath = os.path.dirname(__file__)
sys.path.append(relativePath)
from parser import Parser
import json
from xmlHandler import Converter

class Toml(object):
    def __init__(self,input):
        self.parser = Parser(input)
    def toJSON(self,input=""):
        if input == "":
            parser = self.parser
        else:
            parser = Parser(input)
        sys.stdout.write(json.dumps(parser.runtime, ensure_ascii=False))
    #to do
    def toXml(self,input=""):
        if input == "":
            parser = self.parser
        else:
            parser = Parser(input, asJson=True)
        sys.stdout.write(Converter.collectionToXML(parser.runtime))

examplePath = relativePath + "\\example.toml"
js = Toml.toJSON(examplePath)
xml = Toml.toXml(examplePath)
