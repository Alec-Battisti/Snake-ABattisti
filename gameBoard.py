from snakeObject import Snake
from directionObject import Direction
import math
import random
import traceback


class Board:
    def __init__(self, x, y, r, c, w, h):
        self.Data = [[0 for i in range(c)] for j in range(r)]
        self.X = x
        self.Y = y
        self.C = c
        self.R = r
        self.stepX = math.floor(w / c)
        self.stepY = math.floor(h / r)
        self.Snake = Snake(math.floor(self.C / 2), math.floor(self.R / 2))
        self.Data[self.Snake.location.X][self.Snake.location.Y] = 1
        self.Velocity = Direction(1, 0)
        self.addFruit()

    def getGridLoc(self, location):
        return Direction(
            location.X * self.stepX + self.X, location.Y * self.stepY + self.Y
        )

    def getCell(self, location):
        return self.Data[location.X][location.Y]

    def setCell(self, location, x):
        self.Data[location.X][location.Y] = x

    def addFruit(self):
        randX, randY = None, None
        while 1:
            randX, randY = random.randint(0, self.R - 1), random.randint(0, self.C - 1)
            if self.Data[randX][randY] == 0:
                break
        self.setCell(Direction(randX, randY), random.randint(2, 4))

    def updateSnake(self):
        nextLoc = self.Snake.location + self.Velocity
        try:
            if self.getCell(nextLoc) == 1:
                return 0
        except:
            return 0

        if self.getCell(nextLoc) == 0:
            self.setCell(nextLoc, 1)
            self.setCell(self.Snake.tail, 0)
            self.Snake.move(self.Velocity)
            return 1
        elif self.getCell(nextLoc) > 1:
            self.setCell(nextLoc, 1)
            self.Snake.grow(self.Velocity)
            return 2

        return 1
