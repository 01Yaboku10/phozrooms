class Difficulty():
    def __init__(self, mapsize: int, phoz: int, exam: int, treasure: int, drunkard: int) -> None:
        self.mapsize = 5 + mapsize
        self.START = 1
        self.phoz = 1 + phoz
        self.exam = 20 + exam
        self.treasure = 1 + treasure
        self.drunkard = 30 + drunkard

    def diff_attrib(self) -> tuple[int, int, int, int, int]:
        return self.mapsize, self.phoz, self.exam, self.treasure, self.drunkard

easy = Difficulty(0, 0, 0, 0, 0)
normal = Difficulty(3, 1, 5, 2, 5)
hard = Difficulty(5, 2, 10, 2, 10)
fadder = Difficulty(11, 3, 10, 3, 10)
