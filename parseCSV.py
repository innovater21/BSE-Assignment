import csv
import redis
redisObj = redis.Redis(host='localhost', port=6379, db=0)
with open('EQ080319.CSV', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    count = 0
    for item in csv_reader:
    	x={}
    	x.update({"SC_CODE":item["SC_CODE"],"OPEN":item["OPEN"],"HIGH":str(item["HIGH"]),"LOW":item["LOW"]})
    	redisObj.hmset(item["SC_NAME"].encode().decode('utf-8'),x)
    	# print("SC_CODE :",item['SC_CODE'])
    	print("SC_NAME :",redisObj.hget(item['SC_NAME'],'HIGH').decode('utf-8'))
    	count+=1
    print(count)

