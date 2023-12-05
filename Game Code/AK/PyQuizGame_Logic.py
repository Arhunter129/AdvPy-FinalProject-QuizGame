
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

def load_quiz(data,quiz:question):
    for line in data:
        if(line == "\n"):
            ask = data.readline()
        else:
            ask = line
        opt = []
        load_options(opt,data)
        ans = data.readline()
        quiz.append(question(ask,opt,ans))

def split_text(text, max_length):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) <= max_length:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    if current_line:
        lines.append(current_line.strip())

    return "\n".join(lines)

def load_options(options, data):
    for i in range(0,4):
        options.append(data.readline())

def print_question(question:question):
    print(question.question)
    for i in question.options:
        print(str(question.options.index(i))+")",i)

quiz:question = []#array will be loaded with questions
user = ""
result = False
correct_answers = 0
total_answers = len(quiz)
#game loop
if(__name__ == "__main__"):
    file = open("../Database/output.txt")
    load_quiz(file,quiz)
    for i in quiz:
        print_question(i)
        user = int(input("Please enter your answer:"))
        result = check_answer(i.options[user], i.answer)
        if(result == True):
            print("\nCorrect!\n")
            correct_answers += 1
        else:
            print("\nIncorrect\n")
            print("The Correct answer is:",i.answer)

