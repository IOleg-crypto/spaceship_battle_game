import pygame as pg

def display_information(font, count, score, render, screen):
    text_surface = font.render("Shot bullets : " + str(count), True, WHITE)
    text_score = font.render("Score : " + str(score), True, WHITE)
    text_health = font.render("Health : " + str(render.health), True, RED)

    text_rect = text_surface.get_rect()
    text_score_rect = text_score.get_rect()
    text_health_rect = text_health.get_rect()
    screen.blit(text_surface, text_rect)
    text_rect.topleft = (5, 10)
    text_score_rect.topleft = (text_rect.left, text_rect.bottom + 10)
    text_health_rect.topleft = (
        text_score_rect.left,
        text_score_rect.bottom + 10,
    )
    screen.blit(text_score, text_score_rect)
    screen.blit(text_health, text_health_rect)

def fps_counter(screen , clock):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(f"FPS: {fps}", True, pg.Color("white"))
    screen.blit(fps_text, (10, 40))