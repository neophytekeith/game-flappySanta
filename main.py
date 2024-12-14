import streamlit as st
from PIL import Image, ImageDraw
import random
import time

# Initialize session state variables
if "santa_y" not in st.session_state:
    st.session_state.santa_y = 300
    st.session_state.gravity = 0
    st.session_state.pipes = []
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.high_score = 0

# Constants
WIDTH = 350
HEIGHT = 622
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
PIPE_GAP = 150
GRAVITY = 2
FLAP_STRENGTH = -40

# Load assets
background = Image.open("bg.png").resize((WIDTH, HEIGHT))
floor = Image.open("snow.png").resize((WIDTH, 100))
santa = Image.open("santa.png").resize((50, 50))
pipe_img = Image.open("pipe.png").resize((PIPE_WIDTH, PIPE_HEIGHT))

def reset_game():
    """Reset the game state."""
    st.session_state.santa_y = HEIGHT // 2
    st.session_state.gravity = 0
    st.session_state.pipes = []
    st.session_state.score = 0
    st.session_state.game_over = False

def create_pipe():
    """Create new pipes."""
    y_pos = random.randint(150, HEIGHT - PIPE_GAP - 100)
    return {"top": y_pos - PIPE_HEIGHT, "bottom": y_pos + PIPE_GAP, "x": WIDTH}

def move_pipes():
    """Move pipes to the left and generate new ones."""
    pipes = st.session_state.pipes
    for pipe in pipes:
        pipe["x"] -= 5
    # Remove pipes out of screen
    st.session_state.pipes = [pipe for pipe in pipes if pipe["x"] > -PIPE_WIDTH]
    # Add new pipe
    if not pipes or pipes[-1]["x"] < WIDTH - 200:
        st.session_state.pipes.append(create_pipe())

def check_collision():
    """Check for collision with pipes or floor/ceiling."""
    santa_y = st.session_state.santa_y
    for pipe in st.session_state.pipes:
        if (santa_y < pipe["top"] + PIPE_HEIGHT or santa_y > pipe["bottom"]) and 50 < pipe["x"] < 100:
            st.session_state.game_over = True
            return
    if santa_y <= 0 or santa_y >= HEIGHT - 50:  # Floor/ceiling collision
        st.session_state.game_over = True

def update_score():
    """Update the score when passing through pipes."""
    for pipe in st.session_state.pipes:
        if pipe["x"] == 50:  # Passed pipe
            st.session_state.score += 1
            st.session_state.high_score = max(st.session_state.high_score, st.session_state.score)

def render_frame():
    """Render a single frame of the game."""
    # Create a new image for the frame
    frame = background.copy()
    draw = ImageDraw.Draw(frame)

    # Draw pipes
    for pipe in st.session_state.pipes:
        # Draw top pipe (flipped)
        top_pipe = pipe_img.transpose(Image.FLIP_TOP_BOTTOM)
        frame.paste(top_pipe, (pipe["x"], pipe["top"]))
        # Draw bottom pipe
        frame.paste(pipe_img, (pipe["x"], pipe["bottom"]))

    # Draw Santa
    frame.paste(santa, (50, st.session_state.santa_y), santa)

    # Draw floor
    frame.paste(floor, (0, HEIGHT - 100))

    return frame

# Game loop
if not st.session_state.game_over:
    # Check for mouse click/tap (simulate flap)
    mouse_click = st.mouse_events()
    for event in mouse_click:
        if event["event"] == "click":
            st.session_state.gravity = FLAP_STRENGTH  # Flap when clicked

    # Move pipes and check for collisions
    move_pipes()
    check_collision()
    update_score()

    # Gravity and movement
    st.session_state.gravity += GRAVITY
    st.session_state.santa_y += st.session_state.gravity

    # Render and display frame
    frame = render_frame()
    st.image(frame, use_container_width=True)  # Updated parameter

else:
    # Game Over Screen
    st.write("Game Over!")
    st.write(f"Score: {st.session_state.score}")
    st.write(f"High Score: {st.session_state.high_score}")
    if st.button("Restart"):
        reset_game()

# Simulate animation by updating every 0.03 seconds
time.sleep(0.03)
