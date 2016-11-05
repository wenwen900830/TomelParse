# -*- coding:UTF-8 -*-  
import xml.etree.ElementTree as ET  
import xml.dom.minidom as minidom
from xml import etree
  
class Converter(object):  
    root = None      
    def __init__(self):  
        pass
    @staticmethod  
    def createRoot(rootTag):
        root = ET.Element(rootTag)  
        return root
    @staticmethod  
    def getXmlString(element,defaultEncoding='utf-8'):  
        try:               
            rough_string = ET.tostring(element, defaultEncoding)
            reparsed = minidom.parseString(rough_string)  
            return reparsed.toprettyxml(indent="  " , encoding=defaultEncoding)
        except:  
            print 'getXmlString:can not tranfer node to string correctly,please check the node'  
            return ''       
    @staticmethod  
    def collectionToXML(listobj,rootTag='list'):  
        try:  
            classname = listobj.__class__.__name__
            root = Converter.createRoot(rootTag)  
            if isinstance(listobj, list) or isinstance(listobj, tuple):
                  
                if len(listobj) >= 0:  
                    for obj in listobj:
                        itemE = Converter.classToXML(obj)  
                        root.append(itemE)  
            elif isinstance(listobj, dict):
                if len(listobj) >= 0:  
                    for key in listobj:
                        obj = listobj[key]  
                        itemE = Converter.classToXML(obj)  
                        itemE.set('key', key)  
                        root.append(itemE)  
            else:  
                print 'listToXML:error when transfer, the '+classname+' is not collection type'
            return root  
        except:  
            print 'collectionToXML:error when transfering collection type to xml type'  
            return None  
    @staticmethod  
    def classToElements(classobj,rootTag=None):   
        attrs = None
        elelist = []
        try:  
            attrs = classobj.keys()
        except:  
            print 'classToElements:invalid object,can not get the attr correctly'  
          
        if attrs != None and len(attrs) > 0:
            for attr in attrs:  
                attrvalue = classobj[attr]
                attrE = ET.Element(attr)  
                attrE.text = attrvalue  
                elelist.append(attrE)  
        return elelist           
    @staticmethod  
    def classToXML(classobj,rootTag=None):   
        try:  
            classname = classobj.__class__.__name__
            if rootTag != None:  
                root = Converter.createRoot(rootTag)  
            else:  
                root = Converter.createRoot(classname)  
            elelist = Converter.classToElements(classobj, rootTag)  
            for ele in elelist:  
                root.append(ele)  
            return root  
        except:  
            print 'classToXML:error when tranfer,please check the input object'  
            return None  
    @staticmethod
    def writeToFile(tree,filePath):
        tree.write(filePath, encoding="utf-8",xml_declaration=True)
         
