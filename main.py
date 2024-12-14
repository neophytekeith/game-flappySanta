import streamlit as st
import pygame
import random

# Initialize the Pygame library
pygame.init()

# Set game window size
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Santa")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game constants
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_VELOCITY = 3
SANTA_WIDTH = 50
SANTA_HEIGHT = 50

# Define the Santa class
class Santa(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SANTA_WIDTH, SANTA_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Prevent Santa from going off the screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def flap(self):
        self.velocity = FLAP_STRENGTH

# Define the Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = PIPE_WIDTH
        self.height = random.randint(100, HEIGHT - PIPE_GAP - 100)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.bottom = self.height
        self.rect.top = self.height - PIPE_GAP

    def update(self):
        self.rect.x -= PIPE_VELOCITY
        if self.rect.right < 0:
            self.kill()

# Initialize the game
def reset_game():
    st.session_state.santa = Santa()
    st.session_state.santa_group = pygame.sprite.Group(st.session_state.santa)
    st.session_state.pipes = pygame.sprite.Group()
    st.session_state.game_over = False
    st.session_state.score = 0

# Game loop function
def game_loop():
    santa = st.session_state.santa
    santa_group = st.session_state.santa_group
    pipes = st.session_state.pipes
    game_over = st.session_state.game_over

    if not game_over:
        # Check for mouse click/tap (simulate flap)
        if st.button('Flap'):
            santa.flap()

        # Add new pipes
        if random.randint(1, 50) == 1:
            new_pipe = Pipe()
            pipes.add(new_pipe)

        # Update game objects
        santa_group.update()
        pipes.update()

        # Check for collisions
        if pygame.sprite.spritecollideany(santa, pipes) or santa.rect.top <= 0 or santa.rect.bottom >= HEIGHT:
            st.session_state.game_over = True

        # Update the score
        st.session_state.score += 1

        # Drawing the game objects
        screen.fill(WHITE)
        santa_group.draw(screen)
        pipes.draw(screen)

        # Show the score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {st.session_state.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    else:
        # Display Game Over
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("Game Over", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 3))

    # Update the display
    pygame.display.update()

# Streamlit UI
if 'game_over' not in st.session_state:
    reset_game()

# Main game loop
while True:
    game_loop()
