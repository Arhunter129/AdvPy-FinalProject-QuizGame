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
    x, y = 10, HEIGHT // 2  # Starting position
    font = pygame.font.Font(None, 36)

    # Example text with word wrapping
    question = "This is an example question, which has the correct answer of C."
    texts = [
        question,
        "A: Is Not Correct!",
        "B: Also Not Correct!",
        "C: Is Correct!",
        "D: Go back to C, it's Correct!"
    ]

    # Create buttons with different colors
    button_a = Button("A", pygame.Rect(50, 500, 100, 50), (255, 0, 0))  # Red
    button_b = Button("B", pygame.Rect(200, 500, 100, 50), (0, 255, 0))  # Green
    button_c = Button("C", pygame.Rect(350, 500, 100, 50), (0, 0, 255))  # Blue
    button_d = Button("D", pygame.Rect(500, 500, 100, 50), (255, 255, 0))  # Yellow

    buttons = [button_a, button_b, button_c, button_d]

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
                            user_answer = button.text
                            print(f'Button {button.text} clicked!')

        # Update Pygame window (e.g., drawing)
        screen.fill((255, 255, 255))  # White background

        for i, text in enumerate(texts):
            rendered_text = font.render(text, True, (0, 0, 0))
            if y + rendered_text.get_height() * (i + 1) <= HEIGHT:
                screen.blit(rendered_text, (x, y + rendered_text.get_height() * i))

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

    # Add your logic to handle the click here

    return jsonify({'status': 'success'})

# ...

def run_flask():
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, app, use_reloader=False)

# ...

if __name__ == "__main__":
    app.run(debug=True)
    #flask_thread = threading.Thread(target=run_flask)
    #flask_thread.start()
