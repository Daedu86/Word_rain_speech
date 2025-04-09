import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FONT_SIZE = 36

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Word Tetris")
clock = pygame.time.Clock()

# Load font
font = pygame.font.SysFont(None, FONT_SIZE)

# Function to generate a random word
def generate_word():
    words_list = ["apple", "banana", "cherry", "orange", "grape", "watermelon"]
    return random.choice(words_list)

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Function to get speed input from user
def get_speed_input(screen, font):
    speed_input = ""
    input_rect = pygame.Rect(100, 200, 200, FONT_SIZE)
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if speed_input.isdigit() and 1 <= int(speed_input) <= 10:
                        return int(speed_input)
                elif event.key == pygame.K_BACKSPACE:
                    speed_input = speed_input[:-1]
                else:
                    speed_input += event.unicode

        screen.fill(BLACK)
        draw_text("Enter speed (1 to 10):", font, WHITE, screen, 50, 150)
        pygame.draw.rect(screen, WHITE, input_rect, 2)
        draw_text(speed_input, font, WHITE, screen, input_rect.x + 5, input_rect.y + 5)

        pygame.display.flip()
        clock.tick(60)

# Get speed from user
speed = get_speed_input(screen, font)

# Define game variables within the loop for reinitialization
score = 0
typed_word = ""

# Main game loop
while True:
    # Define game variables within the loop for reinitialization
    word_speed = speed
    words = []

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_BACKSPACE:
                typed_word = typed_word[:-1]
            elif event.key == pygame.K_RETURN:
                if typed_word == current_word:
                    score += 5
                    current_word = generate_word()
                    word_x = random.randint(0, SCREEN_WIDTH - FONT_SIZE * len(current_word))
                    word_y = -FONT_SIZE
                else:
                    score -= 5
                typed_word = ""
            else:
                typed_word += event.unicode

    # Clear the screen
    screen.fill(BLACK)

    # Draw the score
    draw_text("Score: " + str(score), font, WHITE, screen, 10, 10)

    # Generate a new word if needed
    if not 'current_word' in locals():
        current_word = generate_word()
        word_x = random.randint(0, SCREEN_WIDTH - FONT_SIZE * len(current_word))
        word_y = -FONT_SIZE

    # Move the word
    word_y += speed
    if word_y > SCREEN_HEIGHT:
        current_word = generate_word()
        word_x = random.randint(0, SCREEN_WIDTH - FONT_SIZE * len(current_word))
        word_y = -FONT_SIZE
        score -= 5

    # Draw the current word
    draw_text(current_word, font, WHITE, screen, word_x, word_y)

    # Draw the typed word
    draw_text(typed_word, font, WHITE, screen, 10, SCREEN_HEIGHT - FONT_SIZE - 10)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
