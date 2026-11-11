from array import array
import math
import os

import pygame


WIDTH = 1280
HEIGHT = 720
FPS = 60
BACKGROUND = (0, 0, 0)
PLAYER_HEIGHT = 174
PLAYER_SPEED = 240
MUSIC_SAMPLE_RATE = 22050
MUSIC_CHORDS = (
    (220.0, 329.64, 440.0, 659.24),
    (174.6, 261.64, 349.24, 523.24),
    (261.64, 392.0, 523.24, 784.0),
    (196.0, 293.68, 392.0, 587.32),
)

ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

pygame.mixer.pre_init(frequency=MUSIC_SAMPLE_RATE, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Наш Спецназ")
clock = pygame.time.Clock()
title_font = pygame.font.Font(None, 76)

if pygame.mixer.get_init() is not None:
    music_samples = array("h")
    chord_duration = 2.5
    music_duration = chord_duration * len(MUSIC_CHORDS)
    sample_count = int(MUSIC_SAMPLE_RATE * music_duration)

    for sample_index in range(sample_count):
        time = sample_index / MUSIC_SAMPLE_RATE
        chord_index = min(int(time / chord_duration), len(MUSIC_CHORDS) - 1)
        chord_time = time - chord_index * chord_duration
        fade = min(1.0, chord_time / 0.3, (chord_duration - chord_time) / 0.3)
        frequencies = MUSIC_CHORDS[chord_index]
        harmony = sum(
            math.sin(2 * math.pi * frequency * time) * volume
            for frequency, volume in zip(frequencies, (0.32, 0.2, 0.13, 0.08))
        )
        pulse = 0.85 + 0.15 * math.sin(2 * math.pi * 0.5 * time)
        sample = int(harmony * pulse * fade * 0.8 * 32767)
        music_samples.extend((sample, sample))

    background_music = pygame.mixer.Sound(buffer=music_samples.tobytes())
    background_music.set_volume(0.7)
    background_music.play(loops=-1)
else:
    print("Фоновая музыка отключена: аудиомикшер pygame недоступен.")

player_source = pygame.image.load(os.path.join(ASSET_DIR, "player.png")).convert_alpha()
player_source = player_source.subsurface(player_source.get_bounding_rect()).copy()
player_sprite = pygame.transform.smoothscale(
    player_source,
    (
        round(player_source.get_width() * PLAYER_HEIGHT / player_source.get_height()),
        PLAYER_HEIGHT,
    ),
)

state = "menu"
player_position = pygame.Vector2(WIDTH * 0.12, HEIGHT * 0.82)
running = True

while running:
    delta_time = min(clock.tick(FPS) / 1000, 0.05)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                (max(960, event.w), max(540, event.h)),
                pygame.RESIZABLE,
            )
        elif event.type == pygame.KEYDOWN:
            if state == "menu" and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                state = "level"
                player_position.update(screen.get_width() * 0.12, screen.get_height() * 0.82)
            elif state == "level" and event.key == pygame.K_ESCAPE:
                state = "menu"
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and state == "menu":
            state = "level"
            player_position.update(screen.get_width() * 0.12, screen.get_height() * 0.82)

    screen.fill(BACKGROUND)

    if state == "menu":
        title = title_font.render("НАШ СПЕЦНАЗ", True, (225, 231, 220))
        screen.blit(title, title.get_rect(center=screen.get_rect().center))
    else:
        keys = pygame.key.get_pressed()
        movement = pygame.Vector2(
            int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT]),
            int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP]),
        )

        if movement.length_squared():
            player_position += movement.normalize() * PLAYER_SPEED * delta_time

        player_width = player_sprite.get_width()
        player_position.x = max(
            player_width / 2,
            min(screen.get_width() - player_width / 2, player_position.x),
        )
        player_position.y = max(
            PLAYER_HEIGHT / 2,
            min(screen.get_height() - PLAYER_HEIGHT / 2, player_position.y),
        )
        screen.blit(player_sprite, player_sprite.get_rect(center=player_position))

    pygame.display.flip()

pygame.quit()
