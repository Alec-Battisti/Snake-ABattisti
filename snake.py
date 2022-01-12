#!/usr/bin/env python3
# Alec Battisti
# CPSC 386-01
# alec.battisti@csu.fullerton.edu
# @Alec-Battisti
#
# This is a snake clone
#
import pygame
from gameBoard import Board
from directionObject import Direction
from leaderBoard import LeaderBoard
from score import Score
import pickle
import os


WIDTH, HEIGHT = 650, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
pygame.font.init()
titleFont = pygame.font.SysFont(None, 200)
title2Font = pygame.font.SysFont(None, 100)
textFont = pygame.font.SysFont(None, 50)
playerFont = pygame.font.SysFont(None, 25)
filename = "scores"
leaderboard = None
try:
    infile = open(filename, "rb")
    leaderboard = pickle.load(infile)
    infile.close()
except:
    leaderboard = LeaderBoard()


def drawHome():
    WIN.fill((0, 0, 0))
    title = titleFont.render("SNAKE", True, (0, 255, 0))
    WIN.blit(title, (75, 75))
    message = textFont.render("Press spacebar to start", True, (0, 255, 0))
    WIN.blit(message, (130, 500))
    pygame.display.update()


def drawLeader():
    WIN.fill((0, 0, 0))
    title = title2Font.render("GAME OVER", True, (0, 255, 0))
    WIN.blit(title, (100, 75))
    for i, v in enumerate(leaderboard.Scores):
        player = playerFont.render(
            str(i + 1)
            + ": "
            + str(v.Points)
            + " Pts. | "
            + str(v.Date)
            + " | "
            + str(v.Time)
            + "ms",
            True,
            (0, 255, 0),
        )
        WIN.blit(player, (185, 150 + 30 * (i + 1)))
    message = textFont.render("Press spacebar to play again", True, (0, 255, 0))
    WIN.blit(message, (110, 500))
    pygame.display.update()


def drawGame(board, score):
    WIN.fill((0, 0, 0))
    gameBoard = (75, 75, 500, 500)
    pygame.draw.rect(WIN, (0, 255, 0), gameBoard)
    scoreMessage = title2Font.render(
        "Score: " + str(score.Points), True, (255, 255, 255)
    )
    WIN.blit(scoreMessage, (0, 0))
    for x, i in enumerate(board.Data):
        for y, j in enumerate(i):
            loc = board.getGridLoc(Direction(x, y))
            if j == 1:
                snakeSeg = (loc.X, loc.Y, board.stepX, board.stepY)
                pygame.draw.rect(WIN, (0, 0, 255), snakeSeg)
            elif j > 1:
                food = (loc.X, loc.Y, board.stepX, board.stepY)
                pygame.draw.rect(WIN, (255, 0, 0), food)
    pygame.display.update()


def main():

    run = True
    clock = pygame.time.Clock()
    scene = 0
    board = Board(75, 75, 20, 20, 500, 500)
    ticker = 0
    scoreTimer = 0
    FPS = 60
    score = Score()
    while run:
        clock.tick(FPS)
        if scene == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    scene = 1
                    ticker = pygame.time.get_ticks()
                    scoreTimer = 0
                    FPS = 10
            drawHome()
        elif scene == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        board.Velocity = Direction(0, -1)
                    elif event.key == pygame.K_a:
                        board.Velocity = Direction(-1, 0)
                    elif event.key == pygame.K_s:
                        board.Velocity = Direction(0, 1)
                    elif event.key == pygame.K_d:
                        board.Velocity = Direction(1, 0)
            result = board.updateSnake()
            if result == 0:
                scene = 2
                FPS = 60
                board = Board(75, 75, 20, 20, 500, 500)
                score.Time = pygame.time.get_ticks() - ticker
                leaderboard.register(score)
                outfile = open(filename, "wb")
                pickle.dump(leaderboard, outfile)
                outfile.close()
                score = Score()
            elif result == 2:
                board.addFruit()
                score.Points += 5
            drawGame(board, score)
            if scoreTimer >= 30:
                score.Points += 1
                scoreTimer = 0
            scoreTimer += 1
        elif scene == 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    scene = 1
                    ticker = pygame.time.get_ticks()
                    scoreTimer = 0
                    FPS = 10
            drawLeader()
    pygame.quit()


if __name__ == "__main__":
    main()
