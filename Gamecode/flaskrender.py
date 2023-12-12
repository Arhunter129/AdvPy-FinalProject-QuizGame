from flask import Flask, render_template, Response, jsonify, request, g
import pygame
from PIL import Image
import io
import threading
from AK.PyQuizGame_Logic import question, check_answer, display_score, load_quiz, load_options, print_question, split_text
import time
from typing import List

app = Flask(__name__)

# Initialization Game window
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.Surface((WIDTH, HEIGHT))

# Global variables
buttons = List[question]
current_question_index = 0
# Stores button data
class Button:
    def __init__(self, text, rect, color, answer, correct):
        print(type(text))
        self.text = text
        self.rect = rect
        self.color = color
        self.answer = answer
        self.correct = correct
        self.clicked = False

    def draw(self, surface):
        if self.clicked:
            pygame.draw.rect(surface, (255, 0, 0), self.rect)  # Sets incorrect buttons red
        elif self.correct:
            pygame.draw.rect(surface, (0, 255, 0), self.rect)  # Sets correct buttons green
        else:
            pygame.draw.rect(surface, self.color, self.rect)  # Default color

        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)


# Generates a new frame and exports it to the flask server
def generate(questions):
    x, y = 10, 10  # Starting position
    font = pygame.font.Font(None, 36)
    global buttons
    global answer
    buttons.clear()

    # Creates four buttons based on quiz data
    for idx, option in enumerate(questions.options):
        is_correct = option == question.answer
        button_rect = pygame.Rect(10, 375 + idx * 50, WIDTH - 20, 40)
        button = Button(f"{option.strip()}", button_rect, (0, 128, 255), option, correct=is_correct)
        buttons.append(button)

    while True:

        # Handle Pygame events (e.g., quitting)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        #Sets background to grey
        screen.fill((90, 90, 90))

        # Display question
        answer = questions.answer
        question_text = questions.question.strip()
        max_line_length = WIDTH/12
        split_question = split_text(question_text, max_line_length)
        lines = split_question.split("\n")
        for i, line in enumerate(lines):
            line_rendered = font.render(line, True, (255, 255, 255))
            screen.blit(line_rendered, (x, y + i * 30))

        # Display buttons
        for button in buttons:
            button.draw(screen)

        # Convert to PNG image
        img_str = pygame.image.tostring(screen, 'RGB')
        img = Image.frombytes('RGB', (WIDTH, HEIGHT), img_str)

        # Convert PIL to byte stream
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')

        # Yield the byte stream
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + img_byte_array.getvalue() + b'\r\n')


@app.route('/')
def index():
    return render_template('game.html')


@app.route('/video_feed')
def video_feed():
    global current_question_index

    if current_question_index < len(quiz):
        question_obj = quiz[current_question_index]
    else:
        question_obj = quiz[0]

    return Response(generate(question_obj), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/handle_click', methods=['POST'])
def handle_click():
    global buttons
    global current_question_index
    global score
    data = request.form
    x = float(data.get('x'))
    y = float(data.get('y'))
    reload_page = False
    wrong_answer_clicked = False


    # Check if (x,y) is within any button rectangle
    for button in buttons:
        if button.rect.collidepoint(x, y):
            button_clicked = button.text.strip()
            user_answer = button.answer.strip()
            button.correct = user_answer == answer.strip()
            if button.correct:
                current_question_index += 1
                score += 1
                print(score, len(quiz))
                if current_question_index >= len(quiz):
                    print(display_score(score,len(quiz)))
                    current_question_index = 0
                    score = 0
                reload_page = True
                time.sleep(1)
            elif ~button.correct:
                button.clicked = True
                score -= 1

    return jsonify({'status': 'success', 'reload_page': reload_page})


def run_flask():
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, app, use_reloader=False)


if __name__ == "__main__":
    # TODO finish moving load quiz , score, and queastion calls to game logic
    global score
    score = 0
    with open("./database/output.txt", "r") as file:
        quiz = []
        load_quiz(file, quiz)

    total_answers = len(quiz)
    generate(quiz)
    app.run(debug=True)
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
