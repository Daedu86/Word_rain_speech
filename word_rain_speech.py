import pygame
import random
import sys
from gtts import gTTS
import tempfile
import os

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FONT_SIZE = 36
WORD_SPEED = 1  # Speed of falling words

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wort Tetris")
clock = pygame.time.Clock()

# Load font
font = pygame.font.SysFont(None, FONT_SIZE)

# Define custom event for speech cleanup
CLEANUP_EVENT = pygame.USEREVENT + 1

# Define temp_file globally
temp_file = ""

# Function to generate a random German word
def generate_word():
    words_list = ["Apfel", "Banane", "Kirsche", "Orange", "Traube", "Wassermelone"]
    return random.choice(words_list)

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Function to play music asynchronously
def play_music(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# Function to speak the word
def speak_word(word):
    global temp_file  # Access the global variable
    # Convert text to speech using gTTS and save it to a temporary file
    tts = gTTS(text=word, lang='de')
    temp_file = tempfile.mktemp(suffix='.mp3')
    tts.save(temp_file)
    
    # Play the speech asynchronously
    play_music(temp_file)
    
    # Clean up: Stop the music playback after the speech finishes playing
    pygame.time.set_timer(CLEANUP_EVENT, 2000)  # Trigger cleanup event after 2 second

# Main game loop
score = 0
typed_word = ""
current_word = generate_word()

# Ensure SCREEN_WIDTH is large enough to accommodate the longest word plus some padding
max_word_x = max(0, SCREEN_WIDTH - FONT_SIZE * len(current_word))

word_x = random.randint(0, max_word_x)  # Start position for new word
word_y = -FONT_SIZE  # Start above the screen

# Start speaking the first word
speak_word(current_word)

# Flag to track if the game is running
running = True

while running:
    # Clear the screen
    screen.fill(BLACK)

    # Draw the current word
    draw_text(current_word, font, WHITE, screen, word_x, word_y)

    # Draw the typed word at the bottom of the screen
    draw_text(typed_word, font, WHITE, screen, 10, SCREEN_HEIGHT - FONT_SIZE - 10)

    # Update the display
    pygame.display.flip()

    # Move the word downwards
    word_y += WORD_SPEED

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_BACKSPACE:
                typed_word = typed_word[:-1]
            elif event.key == pygame.K_RETURN:
                if typed_word.lower() == current_word.lower():
                    score += 3
                    typed_word = ""  # Clear typed word
                    current_word = generate_word()  # Generate a new word
                    max_word_x = max(0, SCREEN_WIDTH - FONT_SIZE * len(current_word))
                    word_x = random.randint(0, max_word_x)  # Start position for new word
                    word_y = -FONT_SIZE  # Start above the screen
                    speak_word(current_word)  # Start speaking the new word
                else:
                    score -= 1  # Decrease score for wrong input
                    typed_word = ""  # Clear typed word
            else:
                typed_word += event.unicode

        # Handle cleanup event
        elif event.type == CLEANUP_EVENT:
            pygame.mixer.music.stop()  # Stop the music playback

    # Generate a new word if the word reaches the bottom of the screen
    if word_y > SCREEN_HEIGHT:
        score -= 1  # Decrease score for missed word
        typed_word = ""  # Clear typed word
        current_word = generate_word()  # Generate a new word
        max_word_x = max(0, SCREEN_WIDTH - FONT_SIZE * len(current_word))
        word_x = random.randint(0, max_word_x)  # Start position for new word
        word_y = -FONT_SIZE  # Start above the screen
        speak_word(current_word)  # Start speaking the new word

    # Cap the frame rate
    clock.tick(60)

# Quit pygame mixer when exiting the game loop to release resources
pygame.mixer.quit()
pygame.quit()
sys.exit()



























