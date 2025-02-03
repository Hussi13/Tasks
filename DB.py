""" import pymongo
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://sw01082238:Tay1989_@tasks.yohjn.mongodb.net/?retryWrites=true&w=majority&appName=Tasks"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
    
db=client["Tasks"]
collection = db["Task"]
post = {"First Name":"Hussein", 
"Last Name": "Alnazal", "Email": "SW01082238@STUDENT.UNITEN.EDU.MY"}

collection.insert_one(post)
"""


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

cluster = MongoClient("mongodb+srv://HusseinDB:Od8qEQZvB9sBIwQI@cluster0.fhj27.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

"""Od8qEQZvB9sBIwQI """
# Create a new client and connect to the server


# Send a ping to confirm a successful connection
try:
    cluster.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
        
db=cluster["HusseinDB"]
collection = db["HusseinDB"]
post = {"First Name":"Hussein", 
"Last Name": "Alnazal", "Email": "SW01082238@STUDENT.UNITEN.EDU.MY"}
collection.insert_one(post)