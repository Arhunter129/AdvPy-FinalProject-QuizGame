from typing import List
import io
class question:
    question: str = ""
    options: List[str] = ["","","",""]
    answer:str = ""
    def __init__(self,q:str,opt:List[str],ans:str ):
        self.question = q
        self.options = opt
        self.answer = ans


def check_answer(user:str, answer:str) -> bool:
    if(answer == user):
        return True
    else:
        return False
    
def display_score(correct:int, total:int)->None:
    percent = (correct/total)*100
    print("Your score is: ", percent, "%\n")
    print("You got ", correct, " answers right out of ", total," questions")

def load_quiz(data: io.TextIOBase, quiz:List[question]) -> None:
    for line in data:
        if(line == "\n"):
            ask = data.readline()
        else:
            ask = line
        opt:List[str] = []
        load_options(opt,data)
        ans = data.readline()
        quiz.append(question(ask,opt,ans))

def split_text(text:str , max_length:int) -> str:
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

def load_options(options:List[str], data: io.TextIOBase) -> None:
    for i in range(0,4):
        options.append(data.readline())

def print_question(question:question) -> None:
    print(question.question)
    for i in question.options:
        print(str(question.options.index(i))+")",i)

