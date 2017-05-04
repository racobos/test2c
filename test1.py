import sys
from requests.auth import HTTPBasicAuth
import json
import requests
from xml.etree import ElementTree
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element,SubElement,Comment,tostring, parse, XML, fromstring, tostring

url='http://127.0.0.1:8080/api/running/services/'
USER='admin'
PASS='admin'
headers = {'Accept': 'application/vnd.yang.data+xml','Content-Type': 'application/vnd.yang.data+xml'}

def createXml(vals):
    originNode = vals[0]
    destinationNode = vals[1]
    pwID = vals[2]
    localInterface = vals[3]
    remoteInterface = vals[4]
    vlanID = vals[5]
    vplsID = vals[6]
    top=Element('multipoint', xmlns="http://example.com/multipoint")
    child_1=SubElement(top,'vplsID')
    child_1.text=vplsID
    child_2=SubElement(top,'originNode')
    child_2.text=originNode
    child_3=SubElement(top,'localInterface')
    child_3.text=localInterface
    child_4=SubElement(top,'vlanID')
    child_4.text=vlanID
    child_5=SubElement(top,'spokes')
    child_6=SubElement(child_5,'pwID')
    child_6.text=pwID
    child_7=SubElement(child_5,'destinationNode')
    child_7.text=destinationNode
    child_8=SubElement(child_5,'remoteInterface')
    child_8.text=remoteInterface
    xmlstr=ElementTree.tostring(top,encoding='utf-8',method='xml')
    return xmlstr


def getService(xmlstr,html):
    a = requests.get(html,headers=headers,auth=HTTPBasicAuth(USER,PASS))
    return a

def updateService(xmlstr,html):
    b = requests.patch(html, data=xmlstr,headers=headers,auth=HTTPBasicAuth(USER,PASS))
    return b

def createService(xmlstr,url):
    b = requests.post(url, data=xmlstr,headers=headers,auth=HTTPBasicAuth(USER,PASS))
    return b

def createVpls(vals):
    xmlstr = createXml(vals)

    # c = createService(xmlstr,url)
    # return c

    a = getService(xmlstr,html=url+'multipoint/'+vals[6])
    if a.status_code == 200:
        print "Service exist, updating..."
        b = updateService(xmlstr,html=url+'multipoint/'+vals[6])
    else:
        print "Service does not exist, creating..."
        b = createService(xmlstr,url)

    print b.status_code
    return b.status_code

