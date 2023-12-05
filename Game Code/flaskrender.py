from flask import Flask, render_template, Response, jsonify, request
import pygame
from PIL import Image
import io
import threading

app = Flask(__name__)

# Pygame initialization
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.Surface((WIDTH, HEIGHT))

# Declare buttons as a global variable
buttons = []

class Button:
    def __init__(self, text, rect, color):
        self.text = text
        self.rect = rect
        self.color = color  # Add a color attribute

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)  # Use the color attribute
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

def generate():
    x, y = 10, 10  # Starting position
    font = pygame.font.Font(None, 36)

    # Example question with answers
    question = "This is an example question, which has the correct answer of C."
    answers = [
        ("A: Is Not Correct!", 'A'),
        ("B: Also Not Correct!", 'B'),
        ("C: Is Correct!", 'C'),
        ("D: Go back to C, it's Correct!", 'D')
    ]

    global buttons  # Declare buttons as a global variable

    # Create buttons with different colors and stack them vertically
    buttons = [
        Button(answer_text, pygame.Rect(50, 300 + i * 60, 400, 50), (0, 0, 0))
        for i, (answer_text, _) in enumerate(answers)
    ]

    
    
    correct_answer = 'C'
    user_answer = None
    show_feedback = False

    while True:
        # Handle Pygame events (e.g., quitting)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Handle button clicks
            if event.type == pygame.MOUSEBUTTONDOWN and not show_feedback:
                if event.button == 1:  # Left mouse button
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            user_answer = button.text.split(":")[0].strip()  # Get the answer text
                            print(f'Button {user_answer} clicked!')
                            show_feedback = True  # Update show_feedback when a button is clicked

        # Update Pygame window (e.g., drawing)
        screen.fill((90, 90, 90))  # White background

        # Display question
        question_rendered = font.render(question, True, (0, 0, 0))
        screen.blit(question_rendered, (x, y))

        # Draw buttons
        for button in buttons:
            button.draw(screen)

        # Display feedback
        if show_feedback:
            if user_answer == correct_answer:
                feedback_text = "Correct! Well done."
            else:
                feedback_text = "Try again. Incorrect answer."

            feedback_rendered = font.render(feedback_text, True, (255, 0, 0))
            feedback_rect = feedback_rendered.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(feedback_rendered, feedback_rect)

            # Reset show_feedback after displaying feedback for a short duration
            pygame.time.delay(2000)  # Delay in milliseconds (adjust as needed)
            show_feedback = False

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

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/handle_click', methods=['POST'])
def handle_click():
    data = request.form  # Access the data sent with the POST request
    x = float(data.get('x'))
    y = float(data.get('y'))
    print(f'Received click at coordinates ({x}, {y})')

    # Check if the coordinates are within any button rectangle
    for button in buttons:
        if button.rect.collidepoint(x, y):
            button_clicked = button.text
            print(f'Button "{button_clicked}" clicked!')
            # Add your logic to handle the button click here

    return jsonify({'status': 'success'})

def run_flask():
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, app, use_reloader=False)

if __name__ == "__main__":
    app.run(debug=True)
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()