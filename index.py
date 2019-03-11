import cherrypy
import os, os.path
from os import path
import random
import string
import csv
import redis
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import zipfile36
import datetime
from operator import itemgetter

class demoExample:
	def index(self):
		return open('index.html')
	index.exposed = True

	def trends(self):
		return open('trends.html')
	trends.exposed = True

	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	def getTrends(self):
		redisObj = redis.Redis(host='localhost', port=6379, db=0)
		finalList=[]
		prevList = []
		tempList = []
		xDict = {}
		xpList=[]
		prevList = redisObj.keys('*')
		for newItem in prevList:
			xDict={}
			xDict["HIGH"] = float(redisObj.hget(newItem,'HIGH').decode('utf-8'));
			xDict["Name"]  = newItem;
			xpList.append(xDict)
		xpList = sorted(xpList,key=itemgetter('HIGH'),reverse=True)
		print(redisObj.hget(prevList[0],'HIGH').decode('utf-8'))
		count=0
		for item in xpList:
			if(count>9):
				break
			else:
				y={}
				# print(item)
				y["NAME"] = item['Name'].decode('utf-8')
				y["CODE"] = redisObj.hget(item['Name'],'SC_CODE').decode('utf-8')
				y["OPEN"] = redisObj.hget(item['Name'],'OPEN').decode('utf-8')
				y["HIGH"] = redisObj.hget(item['Name'],'HIGH').decode('utf-8')
				y["LOW"] = redisObj.hget(item['Name'],'LOW').decode('utf-8')
				tempList.append(y)
				# print(y)
				count+=1
		print(tempList)
		return tempList
	getTrends.exposed = True

	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	def getSearch(self,txt1):
		redisObj = redis.Redis(host='localhost', port=6379, db=0)
		searchList = []
		tempList=[]
		searchList = redisObj.keys("*"+txt1+"*")
		for item in searchList:
			y={}
			# print(item)
			y["NAME"] = item.decode('utf-8')
			y["CODE"] = redisObj.hget(item,'SC_CODE').decode('utf-8')
			y["OPEN"] = redisObj.hget(item,'OPEN').decode('utf-8')
			y["HIGH"] = redisObj.hget(item,'HIGH').decode('utf-8')
			y["LOW"] = redisObj.hget(item,'LOW').decode('utf-8')
			tempList.append(y)
		return tempList
	getSearch.exposed = True

	def fetchCSV(self):
		html = urlopen("https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx") # Insert your URL to extract
		bsObj = BeautifulSoup(html.read(),features="lxml");

		for link in bsObj.find_all('a'):
			x = datetime.datetime.now()
			# Get the daily date
			# print("Equity/EQ"+str(int(x.strftime('%d'))-1)+ x.strftime('%m')+x.strftime("%y"))
			if "Equity/EQ080319" in str(link.get('href')) :
				# Request the file from the link
				req = requests.get(link.get('href'))
				# Store the file in disk
				with open("minemaster1.zip", "wb") as code:
					code.write(req.content)
				# Extract file
				with zipfile36.ZipFile('minemaster1.zip', "r") as z:
					z.extractall()

	def parseCSV(self):
		redisObj = redis.Redis(host='localhost', port=6379, db=0)
		with open('EQ080319.CSV', mode='r') as csv_file:
		    csv_reader = csv.DictReader(csv_file)
		    count = 0
		    for item in csv_reader:
		    	x={}
		    	x.update({"SC_CODE":item["SC_CODE"],"OPEN":item["OPEN"],"HIGH":str(item["HIGH"]),"LOW":item["LOW"]})
		    	redisObj.hmset(item["SC_NAME"].encode().decode('utf-8'),x)

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    dm = demoExample()
    boolVal = path.exists('minemaster1.zip')
    if not boolVal :
    	dm.fetchCSV()
    dm.parseCSV()
    # abc = dm.getTrends()
    cherrypy.quickstart(demoExample(), '/', conf)
    dm.arr = dm.getTrends()
# cherrypy.quickstart(demoExample())