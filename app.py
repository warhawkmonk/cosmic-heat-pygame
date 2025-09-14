
import streamlit as st
import os
import pygame
from PIL import Image
from classes.constants import WIDTH, HEIGHT
from classes.player import Player
from classes.bullets import Bullet
from st_keyup import st_keyup
from streamlit_autorefresh import st_autorefresh

os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.display.set_mode((1, 1))

value = st_keyup("Enter a value", key="0")

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

    # Compose game frame using PIL
    bg_img = Image.open('images/bg/background.jpg').convert('RGBA')
    frame = bg_img.copy()
    px, py = st.session_state.player.rect.topleft
    player_img = Image.open('images/player.png').convert('RGBA')
    frame.alpha_composite(player_img, (px, py))
    bullet_img = Image.open('images/bullets/bullet1.png').convert('RGBA')
    for bullet in st.session_state.bullets:
        bx, by = bullet.rect.topleft
        frame.alpha_composite(bullet_img, (bx, by))
    st.image(frame, caption='Cosmic Heat Frame', use_column_width=True)

    st.write(f"Score: {st.session_state.score}")
    st.write(f"Bullets: {st.session_state.bullet_counter}")

    if st.button('Back to Menu'):
        st.session_state.page = 'menu'
        st.rerun()
