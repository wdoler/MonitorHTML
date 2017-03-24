#!/usr/bin/python

import sys
import json
from lxml import html
import requests
from datetime import date
import smtplib
import re

#######################################################################
#   
#   HTMLscraper.py
#
#       This programming exercise will go through a list of websites,
#           find a HTML xpath tag, get all of the text inside of that 
#           tag, and return that data and the date for when the 
#           program found it. If there are changes, then it will
#           email a user the changes aswell as a list of everything
#           it has found
#
#       Input: two json files
#           1) list of websites to monitor
#           2) Email address and password
#
#       Todo: change to OOP
#
#######################################################################

inputWebsiteTxt = 'monitorWebsites.json'
passwordsTxt = 'passwords.json'

def getNew(dictNew, dictOld):
    difference = []
    for name in dictNew:
        if (name in dictOld):
            pass
        else:
            difference.append(name)
    return difference

def getExpired(dictNew, dictOld):
    remove = []
    for name in dictOld:
        if name in dictNew:
            pass
        else:
            remove.append(name)
    return remove

def addList(newList, dictOld):
    for item in newList:
        dictOld.update({item:today.strftime("%m-%d-%Y")})

def removeList(removeList, dictOld):
    for name in remove:
        dictOld.pop(name)

def getList(url,tagToFind):
    # For running behind the TI proxy
    proxies = {
      'http': 'http://webproxy.xyz.com:80',
      'https': 'http://webproxy.xyz.com:80'
    }
    try:
        page = requests.get(url)  
    except:
        page = requests.get(url, proxies = proxies)
    tree = html.fromstring(page.content)
    titles = tree.xpath(find)
    return titles

def scrubList(titles,regexString):
    scrubbedList = []
    for x in titles:
        x = re.sub(r'([^-a-zA-Z\d\s:])','',str(x))
        #print("'"+x+"'\n")
        if(re.search(regexString,x)!=None):
            scrubbedList.append(x)
    return scrubbedList

def sendEmail(body, emailData):
    email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (emailData["gmail_user"], ", ".join(emailData["to"]), 'HTML scraping updates', body)   
    try:
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.ehlo()
        print("connected")
        #sendemails
        print ("Sending to: "+emailData["gmail_user"])
        server_ssl.login(emailData["gmail_user"], emailData["gmail_password"])
        print("logged in")
        server_ssl.sendmail(emailData["gmail_user"],emailData["to"], email_text)
        server_ssl.close()
        print("Email Sent!\n")
    except:
        print("**Something went wrong connecting to gmail smtp ssl\n") 
    
def makeString(Dict):
    returnString = ''
    for key in Dict:
            returnString = returnString + '\t' + key + '\r\n'
            for item in Dict[key]:
                returnString = returnString + '\t    ' + item + '\r\n'
    return returnString

####################################################################
#
#   Program Start
#
####################################################################
    
with open(inputWebsiteTxt,'r') as jsonData:
    siteData = json.load(jsonData)

with open(passwordsTxt,'r') as psswdData:
    personalData = json.load(psswdData)

recentlyAddedDict = {}
recentlyRemovedDict = {}
allDict = {}

for key in siteData["Websites"]:
    url = siteData["Websites"][key]["url"]
    print ("Website to search: "+url)
    find = siteData["Websites"][key]["XpathSearch"]
    print ("String to find: "+find)
    titles = getList(url,find)
    today = date.today()
    
    scrubbedList = scrubList(titles,siteData["Websites"][key]["regexFilter"])
    allDict[key] = scrubbedList
    
    #get newly found
    new = getNew(scrubbedList,siteData["Websites"][key]['found'])
    addList(new,siteData["Websites"][key]['found'])

    # Remove old that dont exist anymore
    remove = getExpired(scrubbedList,siteData["Websites"][key]['found'])
    removeList(remove,siteData["Websites"][key]['found'])
    if(len(new)!=0):
        recentlyAddedDict[key] = new 
    if(len(remove)!=0):
        recentlyRemovedDict[key] = remove 


# Check if there are changes
if((len(recentlyAddedDict.values())!=0)or(len(recentlyRemovedDict.values())!=0)):
    addedString = makeString(recentlyAddedDict)
    removedString = makeString(recentlyRemovedDict)
    allString = makeString(allDict)
    
    body  = "Below is a list of changes \n\n Newly added: \n %s \n Removed: \n %s \n All Found: \n %s" % (addedString, removedString,allString)
    print (body+"\n")

    sendEmail(body, personalData) 
    
    print ("Writing to File\n")
    with open(inputWebsiteTxt,"w") as outFile:
        outFile.write (json.dumps(siteData, sort_keys=True, indent=4, separators=(',', ': ')))
else:
    print("\n****NO CHANGES****\n")
    
print("Script Complete!")