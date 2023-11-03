import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiple Choice Game")

# Button properties
button_width, button_height = 200, 50
button_spacing = 20
button_x = (WIDTH - button_width) // 2
button_y = (HEIGHT - (4 * button_height + 3 * button_spacing)) // 2

# Button colors
button_colors = [WHITE] * 4

# Questions and answers
questions = ["What is the capital of France?", "Which planet is known as the Red Planet?", "What is the largest mammal?", "What is the symbol for water in chemistry?"]
correct_answers = ["Paris", "Mars", "Blue Whale", "H2O"]
user_answers = [""] * 4

# Fonts
font = pygame.font.Font(None, 36)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for i in range(4):
                if button_x <= x <= button_x + button_width and button_y + i * (button_height + button_spacing) <= y <= button_y + i * (button_height + button_spacing) + button_height:
                    user_answers[i] = input(f"Enter your answer to question {i + 1}: ")
    
    screen.fill(WHITE)

    # Draw buttons and text
    for i in range(4):
        button_rect = pygame.Rect(button_x, button_y + i * (button_height + button_spacing), button_width, button_height)
        pygame.draw.rect(screen, button_colors[i], button_rect)
        text_surface = font.render(questions[i], True, GREEN)
        screen.blit(text_surface, (button_x + 10, button_y + i * (button_height + button_spacing) + 10))

    pygame.display.flip()

# Check answers and display results
for i in range(4):
    if user_answers[i] == correct_answers[i]:
        button_colors[i] = GREEN
    else:
        button_colors[i] = (255, 0, 0)
        print(f"Question {i + 1}: Incorrect. Your answer: {user_answers[i]}, Correct answer: {correct_answers[i]}")

# Keep the window open for a few seconds before quitting
pygame.time.delay(5000)

pygame.quit()
sys.exit()
