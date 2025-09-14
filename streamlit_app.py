import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
import os
import pygame
from classes.constants import WIDTH, HEIGHT
from classes.player import Player
from classes.bullets import Bullet
import streamlit as st
from st_keyup import st_keyup
from streamlit_autorefresh import st_autorefresh
value = st_keyup("Enter a value", key="0")
# Initialize Pygame display in dummy mode for compatibility with image conversion, even if not used for rendering
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.display.set_mode((1, 1))

# Initialize session state for game variables
if 'page' not in st.session_state:
    st.session_state.page = 'menu'
if 'player' not in st.session_state:
    st.session_state.player = Player()
    st.session_state.bullets = []
    st.session_state.bullet_counter = 200
    st.session_state.score = 0
    st.session_state.is_shooting = False
    st.session_state.last_shot_time = 0

# Menu page
if st.session_state.page == 'menu':
    st.title('Cosmic Heat')
    menu_img = Image.open('images/mainmenu.jpg')
    st.image(menu_img, use_column_width=True)
    if st.button('Play'):
        st.session_state.page = 'game'
        st.rerun()
    if st.button('Exit'):
        st.stop()

# Game page
if 'pos' not in st.session_state:
    st.session_state.pos = value
elif st.session_state.page == 'game':
    st.title('Cosmic Heat - Game')
    
    # Auto-refresh every 100ms to simulate a game loop
    st_autorefresh(interval=100, key="game_refresh")

    # Handle input
    if value:
        if value[-1] == 'a' and st.session_state.pos != value:
            st.session_state.player.move_left()
            st.session_state.pos = value
        elif value[-1] == 'd' and st.session_state.pos != value:
            st.session_state.player.move_right()
            st.session_state.pos = value
        elif value[-1] == 'w' and st.session_state.pos != value:
            st.session_state.player.move_up()
            st.session_state.pos = value
        elif value[-1] == 's' and st.session_state.pos != value:
            st.session_state.player.move_down()
            st.session_state.pos = value
        elif value[-1] == ' ' and st.session_state.pos != value:
            if st.session_state.bullet_counter > 0:
                bullet = Bullet(st.session_state.player.rect.centerx, st.session_state.player.rect.top)
                st.session_state.bullets.append(bullet)
                st.session_state.bullet_counter -= 1
            st.session_state.pos = value

    # Update bullets
    updated_bullets = []
    for bullet in st.session_state.bullets:
        bullet.update()
        if bullet.rect.centery > 0:
            updated_bullets.append(bullet)
    st.session_state.bullets = updated_bullets

    # Draw using matplotlib
    fig, ax = plt.subplots(figsize=(6, 8))
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.set_facecolor('black')
    ax.plot(st.session_state.player.rect.centerx, st.session_state.player.rect.centery, 'r^', markersize=20)
    for bullet in st.session_state.bullets:
        ax.plot(bullet.rect.centerx, bullet.rect.centery, 'bo', markersize=8)
    ax.axis('off')
    st.pyplot(fig)

    st.write(f"Score: {st.session_state.score}")
    st.write(f"Bullets: {st.session_state.bullet_counter}")

    if st.button('Back to Menu'):
        st.session_state.page = 'menu'
        st.rerun()