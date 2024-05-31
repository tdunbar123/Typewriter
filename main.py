import random
import asyncio
import sys
import pygame
import time

import pygame.display
    

pygame.init()

HEIGHT = 800
WIDTH = 800

screen = pygame.display.set_mode((HEIGHT, WIDTH))

font = pygame.font.SysFont("georgia", 36)
bigger_font = pygame.font.SysFont("georgia", 42)

BLUE = (100,100,255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

timer = 1.0
clock = pygame.time.Clock()
time_bar = pygame.Rect(HEIGHT/2, WIDTH/2-100, timer*90, 50)

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

async def draw_success(screen, word, score):
    screen.fill(BLUE)
    word_text = font.render(word, True, WHITE)
    success_text = bigger_font.render(word[0], True, GREEN)
    score_text = font.render(str(score), True, WHITE)
    pygame.draw.rect(screen, RED, time_bar)
    screen.blit(score_text, (HEIGHT/2, WIDTH/2-200))
    screen.blit(success_text, (HEIGHT/2-3, WIDTH/2-3))
    screen.blit(word_text, (HEIGHT/2, WIDTH/2))
    pygame.display.flip()
    clock.tick(30)
    await asyncio.sleep(0)

async def draw_fail(screen, word, score):
    screen.fill(BLUE)
    word_text = font.render(word, True, WHITE)
    fail_text = bigger_font.render(word[0], True, RED)
    score_text = font.render(str(score), True, WHITE)
    pygame.draw.rect(screen, RED, time_bar)
    screen.blit(score_text, (HEIGHT/2, WIDTH/2-200))
    screen.blit(fail_text, (HEIGHT/2-3, WIDTH/2-3))
    screen.blit(word_text, (HEIGHT/2, WIDTH/2))
    pygame.display.flip()
    clock.tick(30)
    await asyncio.sleep(0)

async def draw(screen, word, score):
    screen.fill(BLUE)
    word_text = font.render(word, True, WHITE)
    score_text = font.render(str(score), True, WHITE)
    pygame.draw.rect(screen, RED, time_bar)
    screen.blit(score_text, (HEIGHT/2, WIDTH/2-200))
    screen.blit(word_text, (HEIGHT/2, WIDTH/2))
    pygame.display.flip()
    clock.tick(30)
    await asyncio.sleep(0)

def create_20_random_letters():
    temp = ''
    for _ in range(20):
        temp += random.choice(LETTERS)
    return temp

async def main():
    word = create_20_random_letters()
    running = True
    gameover = False
    start = time.time()
    score = 0
    while running:
        time_passed = time.time() - start
        timer = 1.0 - time_passed
        time_bar.width = timer*90
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == word[0]:
                    score += 1
                    await draw_success(screen, word, score)
                    word = word[1::]
                    timer = 1.0
                    start = time.time()
                else:
                    await draw_fail(screen, word, score)
                    gameover = True
        while gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        word = create_20_random_letters()
                        start = time.time()
                        timer = 1.0
                        score = 0
                        gameover = False
            await draw_fail(screen, word, score)
        if len(word) < 10:
            word += create_20_random_letters()
        if timer < 0:
            gameover = True
        await draw(screen, word, score)

    pygame.quit()
    sys.exit()

asyncio.run(main())