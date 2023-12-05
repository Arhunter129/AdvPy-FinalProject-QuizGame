from flask import Flask, render_template, Response, jsonify, request, g
import pygame
from PIL import Image
import io
import threading
from AK.PyQuizGame_Logic import question, check_answer, display_score, load_quiz, load_options, print_question


app = Flask(__name__)

# Pygame initialization
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.Surface((WIDTH, HEIGHT))

# Declare buttons as a global variable
buttons = []

# Modify the Button class to include an answer attribute
class Button:
    def __init__(self, text, rect, color, answer):
        self.text = text
        self.rect = rect
        self.color = color
        self.answer = answer

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

def generate(questions):
    print("Received questions:", questions)  # Add this line
    x, y = 10, 10  # Starting position
    font = pygame.font.Font(None, 36)

    # Clear the global buttons list
    global buttons
    buttons.clear()


    # Create buttons for each option
    for idx, option in enumerate(questions.options):
        button_rect = pygame.Rect(10, 375 + idx * 50, WIDTH - 20, 40)
        button = Button(f"{option}", button_rect, (0, 128, 255), idx)
        buttons.append(button)

    while True:
        # Handle Pygame events (e.g., quitting)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Update Pygame window (e.g., drawing)
        screen.fill((90, 90, 90))  # Grey Background

        # Display question
        question_rendered = font.render(questions.question, True, (255, 255, 255))
        screen.blit(question_rendered, (x, y))

        # Draw buttons on the screen
        for button in buttons:
            button.draw(screen)

        # Convert Pygame surface to PNG image
        img_str = pygame.image.tostring(screen, 'RGB')
        img = Image.frombytes('RGB', (WIDTH, HEIGHT), img_str)

        # Convert PIL image to byte stream
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')

        # Yield the byte stream
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + img_byte_array.getvalue() + b'\r\n')

@app.route('/')
def index():
    return render_template('game.html')

current_question_index = 0  # Define current_question_index as a global variable


@app.route('/video_feed')
def video_feed():
    global current_question_index

    if current_question_index < len(quiz):
        question_obj = quiz[current_question_index]
        current_question_index += 1
    else:
        question_obj = None

    # If there is no current question, return an empty response
    if question_obj is None:
        return Response("", mimetype='multipart/x-mixed-replace; boundary=frame')

    # Print for debugging purposes
    print(f"Current question: {question_obj}")

    return Response(generate(question_obj), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/handle_click', methods=['POST'])
def handle_click():
    global buttons

    data = request.form  # Access the data sent with the POST request
    x = float(data.get('x'))
    y = float(data.get('y'))
    print(f'Received click at coordinates ({x}, {y})')

    # Check if the coordinates are within any button rectangle
    for button in buttons:
        if button.rect.collidepoint(x, y):
            button_clicked = button.text
            user_answer = button.answer  # Extract the answer from the button
            print(f'Button "{button_clicked}" clicked!')
            show_feedback = False
            print(user_answer, button.answer)
            if user_answer == button.answer:
                show_feedback = True
                print("correct")

    return jsonify({'status': 'success'})


def run_flask():
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, app, use_reloader=False)

if __name__ == "__main__":

    file = open("../Database/output.txt")
    quiz = []  # create an empty list to store questions
    load_quiz(file, quiz)
    total_answers = len(quiz)
    print(quiz[0].question,quiz[0].answer)
    print(quiz[0].options[0])
    print(quiz[0].options[1])
    generate(quiz)

    app.run(debug=True)
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
