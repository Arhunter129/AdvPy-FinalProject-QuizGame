import typing


class question:
    question: str = ""
    options: list[str] = []
    answer: str = ""

    def __init__(self, q: str, opt: list[str], ans: str):
        self.question = q
        self.options = opt
        self.answer = ans


def check_answer(user: str, answer: str) -> bool:
    if (answer == user):
        return True
    else:
        return False


def display_score(correct: int, total: int) -> float:
    percent = (correct / total) * 100
    print("Your score is: ", percent, "%\n")
    print("You got ", correct, " answers right out of ", total, " questions")
    return percent


def load_quiz(data: typing.Any, quiz: typing.Any) -> None:
    for line in data:
        if (line == "\n"):
            ask = data.readline()
        else:
            ask = line
        opt: list[str] = []
        load_options(opt, data)
        ans = data.readline()
        quiz.append(question(ask, opt, ans))


def load_options(options: list[str], data: typing.Any) -> None:
    for i in range(0, 4):
        options.append(data.readline())


def print_question(quest: typing.Any) -> None:
    print(quest.question)
    for i in quest.options:
        print(str(quest.options.index(i)) + ")", i)


quiz = [question]  # array will be loaded with questions
user: int
result = False
correct_answers = 0
total_answers = 0
# game loop
if (__name__ == "__main__"):
    file = open("input.txt")
    load_quiz(file, quiz)
    total_answers = len(quiz)
    for i in quiz:
        print_question(i)
        user = int(input("Please enter your answer:"))
        result = check_answer(i.options[user], i.answer)
        if (result):
            print("\nCorrect!\n")
            correct_answers += 1
        else:
            print("\nIncorrect\n")
            print("The Correct answer is:", i.answer)
    display_score(correct_answers, total_answers)
