import os
from pymongo.mongo_client import MongoClient

# uri = os.environ.get('MONGODB_URI')
# uri = "mongodb+srv://myAtlasDBUser:q2pBnAR027OLpxtB@myatlasclusteredu.stsjihk.mongodb.net/?retryWrites=true&w=majority"
# host = os.environ.get('MONGODB_HOST')
# port = os.environ.get('MONGODB_PORT')
host = 'mongodb'
port = 27017

def testMongo():
    print('Beginning MongoDB connection test.')
    print('Connecting...')

    # Create a new client and connect to the server
    client = MongoClient(host, port)

    print('Pinging...')
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # mydb = client["sample-database"]
    # mycol = mydb['sample-collection']

    # mydata = {"msg": 'hello!'}

    # res = mycol.insert_one(mydata)

    # print(client.list_database_names())