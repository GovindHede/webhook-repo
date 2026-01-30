from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import sys

# URI provided by user
uri = "mongodb+srv://Govi:d8DvS13wCoW2PagQ@cluster0.ps59tsj.mongodb.net/?appName=Cluster0"

print(f"Attempting to connect with URI: {uri}")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    print("Sending ping...")
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"CONNECTION FAILED: {e}")
    sys.exit(1)
