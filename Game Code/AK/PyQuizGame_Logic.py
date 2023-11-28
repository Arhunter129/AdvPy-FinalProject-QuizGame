from dataclasses import dataclass
"""
uri = "mongodb+srv://cluster0.dgvxubp.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='<path_to_certificate>',
                     server_api=ServerApi('1'))
db = client['testDB']
collection = db['testCol']
doc_count = collection.count_documents({})
print(doc_count)

"""
class question:
    question: str = ""
    options: str = {"","","",""}
    answer:str = ""
    def __init__(self,q:str,opt:str,ans:str ):
        self.question = q
        self.options = opt
        self.answer = ans


def check_answer(user:str,answer:str) -> bool:
    if(answer == user):
        return True
    else:
        return False
    
def display_score(correct:int,total:int)->None:
    percent = (correct/total)*100
    print("Your score is: ", percent, "%\n")
    print("You got ", correct, " answers right out of ", total," questions")

def load_questions(Q_array:question,numOfQ:int):#will need a variable for what comes from the database
    for i in numOfQ:
        quest,option,answer = "" #these will be aquired from the database
        Q_array[i] = question(quest,option,answer)

questions:question = {}#array will be loaded with questions
user = ""
result = False
correct_answers = 0
total_answers = len(questions)
#game loop
for i in questions:
    print(i.question)
    for j in i.options:
        print(j)
    user = int(input("Please enter your answer:"))
    result = check_answer(i.options[user], i.answer)
    if(result == True):
        print("\nCorrect!\n")
        correct_answers += 1
    else:
        print("\nIncorrect\n")

