from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure

path_to_certificate = "../X509-cert-4213624397857697800.pem"
uri = "mongodb+srv://cluster0.dgvxubp.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(
    uri,
    tls=True,
    tlsCertificateKeyFile=path_to_certificate,
    server_api=ServerApi('1'))

db_name = "Quiz"
collection_name = "Questions"

db = client[db_name]
collection = db[collection_name]

try:
    client.admin.command('ismaster')
    print("MongoDB connection successful. Fetching documents...")
except ConnectionFailure:
    print("MongoDB connection failed.")

# Fetch documents
documents = collection.find()

print("Documents fetched. Now converting to txt...")

with open("output.txt", "w") as file:
    for doc in documents:
        # Write the question
        file.write(doc['question'] + '\n')
        
        # Write each option
        for option in doc['options']:
            file.write(option + '\n')
        
        # Write the answer (assuming it's one of the options)
        file.write(doc['answer'] + '\n')

print("Done.")