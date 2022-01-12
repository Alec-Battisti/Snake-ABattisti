from directionObject import Direction


class Snake:
    def __init__(self, x, y):
        self.location = Direction(x, y)
        self.length = 1
        self.data = []

    def updateLocation(self, direction):
        self.location += direction

    def grow(self, direction):
        self.length += 1
        self.data.insert(0, -direction)
        self.updateLocation(direction)

    def move(self, direction):
        self.data.insert(0, -direction)
        self.data.pop()
        self.updateLocation(direction)

    @property
    def tail(self):
        return self.location + sum(self.data, Direction(0, 0))
