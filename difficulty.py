class Difficulty():
    def __init__(self, MAPSIZE, PHOZ, HOLE, TREASURE, BATS):
        self.mapsize = 5 + MAPSIZE
        self.START = 1
        self.phoz = 1 + PHOZ
        self.hole = 20 + HOLE
        self.treasure = 1 + TREASURE
        self.bats = 30 + BATS
    def diff_attrib(self):
        return self.mapsize, self.phoz, self.hole, self.treasure, self.bats

easy = Difficulty(0, 0, 0, 0, 0)
normal = Difficulty(3, 2, 5, 2, 5)
hard = Difficulty(5, 3, 10, 2, 10)
fadder = Difficulty(11, 4, 10, 3, 10)