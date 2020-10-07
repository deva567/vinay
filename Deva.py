from typing import Optional
from pymongo import MongoClient 
from fastapi import FastAPI
import hashlib
import secrets
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import pandas as pd
from vennam import DataFrameToDict
from datetime import date
import requests
from datetime import datetime
import time
app = FastAPI()

CONNECTION_STRING="mongodb+srv://Vd4vennam:Vd4vennam@cluster0.ulcey.mongodb.net/VinayAPI?retryWrites=true&w=majority"

try: 
	conn=MongoClient(CONNECTION_STRING)
	db = conn.VinayAPI
	collection = db.UserDetails
	collection1=db.superAdmin
	# collection2=db.pastData
	print("Connected successfully!!!") 
except Exception as e: 
	print("Could not connect to MongoDB") 
	print(e)

def tel_bot(message):

	Final_req='https://api.telegram.org/bot1266300791:AAHLFI-KGcjEkIZ1-qJBMa86w2LnriRkmgg/sendMessage?chat_id=-465280608&text='+message

	response=requests.get(Final_req)

	# collection.insert_one({"load_date_time":datetime.now(),"Vennam_Bot":'Testing from Vennam_Bot for HIstory Check'})

	# collection1.insert_one({"load_date_time":datetime.now(),"Vennam_Bot":response.json()})

	print( response.json())


@app.get("/")
def read_root():
    return {"Message": "Welcome to Deva's Homepage...."}



@app.post("/details")
async def details(FirstName: str,LastName:str, CompanyName:str,Designation:str,Email:str,WhatsappNumber:str,Location:str,ReferenceBy:str):
	username=collection.find_one({"Email":Email})
	if username !=None:
		tel_bot(f'{Email} --details already exist.')
		return {"Message":"The Official Email ID already exist."}
	else:
		collection.insert_one({"firstName":FirstName,"lastName":LastName,"CompanyName":CompanyName,"Designation":Designation,"Email":Email,"Mobile": WhatsappNumber,"Location":Location,"Reference":ReferenceBy})
		tel_bot(f'{Email} --details saved Successfully')
		return {"Message":"The user details are uploaded successfully"}


@app.post("/SignUp")
async def SignUp(UserName: str, Email:str,Password:str):
	username=collection1.find_one({"UserName":UserName})
	if username !=None:
	    return {"Message":"The UserName already exist choose another one."}
	else:
		if UserName=='Deva567' or UserName=='Vinay143':
			role='Super Admin'
			hashed_Password = hashlib.md5(Password.encode()).hexdigest()
			collection1.insert_one({"UserName": UserName,"Email":Email,"Password":hashed_Password,"Role":role,"userSecretKey":secrets.token_urlsafe(20)})
			tel_bot(f'{UserName} --SignUp Success')
			return {"Message":"The user details are uploaded successfully"}
		else:
			role='User'
			hashed_Password = hashlib.md5(Password.encode()).hexdigest()
			collection1.insert_one({"UserName": UserName,"Email":Email,"Password":hashed_Password,"Role":role,"userSecretKey":secrets.token_urlsafe(20)})
			tel_bot(f'{UserName} --SignUp Success')
			return {"Message":"The user details are uploaded successfully"}


@app.get("/SignIn")
async def SignIn(UserName:str,Password:str):
	username=collection1.find_one({"UserName":UserName})
	# print(username)
	if username:
		if username['UserName']==UserName and username['Password']==hashlib.md5(Password.encode()).hexdigest():
			if UserName=='Deva567' or UserName=='Vinay143':

				tel_bot(f'{UserName} --SignIn Success')
				lst=[]
				cursor = collection.find({},{ "_id": 0 })
				for document in cursor:
					lst.append(document)
					# print(document)

				return lst
			else:
				return {"Message":" You are not authorized user"}

		else:
			tel_bot(f'{UserName} --SignIn Failed due to incorrect Password')
			return {"Message":" The Password may be incorrect."}
	else:
		return {"Message":"You are not authorized user"}
