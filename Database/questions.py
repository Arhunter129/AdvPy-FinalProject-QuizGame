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
    print("MongoDB connection successful. Inserting documents...")
except ConnectionFailure:
    print("MongoDB connection failed.")

trvia_questions = [
    {
        "question": "When was Python first released?",
        "options": ["1989", "1991", "1995", "2000"],
        "answer": "1991"
    },
    {
        "question": "What is the correct way to create a function in Python?",
        "options": ["function myFunction():", "def myFunction():", "create myFunction():", "new function myFunction():"],
        "answer": "def myFunction():"
    },
    {
        "question": "Which of these is not a core data type in Python?",
        "options": ["Lists", "Dictionary", "Tuples", "Class"],
        "answer": "Class"
    },
    {
        "question": "How do you insert COMMENTS in Python code?",
        "options": ["/* This is a comment */", "// This is a comment", "# This is a comment", "-- This is a comment"],
        "answer": "# This is a comment"
    },
    {
        "question": "What will be the output of the following code snippet? 'print('Python trivia[::-1]')'",
        "options": ["atirvt nohtyP", "Python trivia", "aivirt nohtyP", "Error"],
        "answer": "aivirt nohtyP"
    },
    {
        "question": "Which of the following is used to define a block of code in Python language?",
        "options": ["Braces {}", "Parentheses ()", "Indentation", "The word 'block"],
        "answer": "Indentation"
    },
    {
        "question": "Which one of the following is the correct etension of the Python file?",
        "options": [".pyt", ".pt", ".py", ".python"],
        "answer": ".py"
    },
    {
        "question": "What is the term used for checking whether a certain condition is true or false in Python?",
        "options": ["Iteration", "Decision-making", "Looping", "Sequencing"],
        "answer": "Decision-making"
    },
    {
        "question": "Which of the following is the correct operator for power (xy)?",
        "options": ["x^y", "x**y", "x^^y", "pow(x, y)"],
        "answer": "x**y"
    },
    {
        "question": "What keyword is used for creating a new class in Python?",
        "options": ["class", "struct", "object", "define"],
        "answer": "class"
    }
]

print("Done!")
