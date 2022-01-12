class Direction:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __neg__(self):
        return Direction(self.X * -1, self.Y * -1)

    def __add__(self, other):
        return Direction(self.X + other.X, self.Y + other.Y)
