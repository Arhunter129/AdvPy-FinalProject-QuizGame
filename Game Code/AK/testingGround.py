class question:
    question: str = ""
    options: str = []
    answer:str = ""
    
    def __init__(self,q:str = "",opt:str = [],ans:str = "" ):
        self.question = q
        self.options = opt
        self.answer = ans

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
        #print_question(quiz[-1])


def load_options(options, data):
    for i in range(0,4):
        options.append(data.readline())

def print_question(question:question):
    print(question.question)
    for i in question.options:
        print(str(question.options.index(i))+")",i)

options = []
quiz: question = []
if(__name__ == "__main__"):
    file = open("C:\AdvPython\AdvPy-FinalProject-QuizGame\Game Code\AK\input.txt")
    load_quiz(file,quiz)
    file.close()
    for i in quiz:
        print_question(i)
        print("===============================================")
    
  