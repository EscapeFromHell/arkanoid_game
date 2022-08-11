import sys
import os

import pgzrun
import random


TITLE = 'Arkanoid clone'
WIDTH = 800
HEIGHT = 600
BALL_SIZE = 10
CHOICES = {
    1: 'easy',
    2: 'medium',
    3: 'hard'
}

paddle = Actor('paddleblue.png')
paddle.x = 370
paddle.y = 500
paddle_speed = 0

ball = Actor('ballblue.png')
ball.x = 150
ball.y = 250
ball_x_speed = 0
ball_y_speed = 0

score = 0
play_music = True
play_sound = True
game_start = True
game_over = False
game_win = False
bars_list = []


def input_difficulty(difficulty):
    '''Функция изменения сложности.'''
    global ball_x_speed, ball_y_speed, paddle_speed
    if difficulty == 'easy':
        ball_x_speed = -3
        ball_y_speed = -3
        paddle_speed = 4
    if difficulty == 'medium':
        ball_x_speed = -4
        ball_y_speed = -4
        paddle_speed = 5
    if difficulty == 'hard':
        ball_x_speed = -6
        ball_y_speed = -6
        paddle_speed = 7


def draw():
    '''Функция отрисовки объектов и экранов начала/конца игры'''
    global game_start, game_over, game_win, score, play_music, play_sound
    if game_start:
        screen.fill('black')
        screen.draw.text('Choose difficulty:', (300, 100))
        screen.draw.text('Press "E" to "Easy"', (300, 150))
        screen.draw.text('Press "M" to "Medium"', (300, 200))
        screen.draw.text('Press "H" to "Hard"', (300, 250))
        if keyboard.e:
            input_difficulty(CHOICES[1])
            game_start = False
        if keyboard.m:
            input_difficulty(CHOICES[2])
            game_start = False
        if keyboard.h:
            input_difficulty(CHOICES[3])
            game_start = False
    else:
        if not game_over:
            if play_music:
                music.play('music.wav')
                play_music = False
            screen.blit('background.png', (0, 0))
            screen.draw.text(f'{score}', (0, 0))
            paddle.draw()
            ball.draw()
            for bar in bars_list:
                bar.draw()
        if game_over:
            screen.fill('red')
            screen.draw.text(f'GAME OVER, Your score: {score}', (285, 150))
            screen.draw.text('Press "Space" to restart', (300, 250))
            music.stop()
            if play_sound:
                sounds.gameover.play()
                play_sound = False
        if game_win:
            screen.fill('Blue')
            screen.draw.text(f'You Win! Your score: {score}',  (315, 150))
            screen.draw.text('Press "Space" to restart', (300, 250))
            music.stop()
            if play_sound:
                sounds.gamewin.play()
                play_sound = False


def place_bars(x, y, image):
    '''Функция для размещения целей.'''
    bar_x = x
    bar_y = y
    for i in range(9):
        bar = Actor(image)
        bar.x = bar_x
        bar.y = bar_y
        bar_x += 70
        bars_list.append(bar)


coloured_box_list = [
    'element_blue_rectangle_glossy.png',
    'element_green_rectangle_glossy.png',
    'element_red_rectangle_glossy.png'
]
x = 120
y = 100
for coloured_box in coloured_box_list:
    place_bars(x, y, coloured_box)
    y += 50


def update():
    '''Функция настраивает управление и столкновения объектов.'''
    global paddle_speed
    if keyboard.escape:
        quit()
    if keyboard.space:
        restart_program()
    if (keyboard.a) and (paddle.x > 50):
        paddle.x = paddle.x - paddle_speed
    if (keyboard.d) and (paddle.x < 750):
        paddle.x = paddle.x + paddle_speed
    update_ball()
    global ball_x_speed, ball_y_speed, score
    for bar in bars_list:
        if ball.colliderect(bar):
            sounds.hit.play()
            bars_list.remove(bar)
            score += 1
            ball_y_speed *= -1
            rand = random.randint(0, 1)
            if rand:
                ball_x_speed *= -1
    if paddle.colliderect(ball):
        sounds.impact.play()
        ball_y_speed *= -1
        rand = random.randint(0, 1)
        if rand:
            ball_x_speed *= -1


def update_ball():
    '''Функция настраивает движение шара и условия победы/поражения'''
    global ball_x_speed, ball_y_speed, game_over, game_win, score
    ball.x -= ball_x_speed
    ball.y -= ball_y_speed
    if (ball.x >= (WIDTH - BALL_SIZE)) or (ball.x <= BALL_SIZE):
        sounds.impact.play()
        ball_x_speed *= -1
    if (ball.y >= (HEIGHT - BALL_SIZE)) or (ball.y <= BALL_SIZE):
        sounds.impact.play()
        ball_y_speed *= -1
    if ball.y >= 550:
        game_over = True
        ball_x_speed = 0
        ball_y_speed = 0
    if score == 27:
        game_win = True


def restart_program():
    '''Рестарт программы.'''
    python = sys.executable
    os.execl(python, python, * sys.argv)


pgzrun.go()
