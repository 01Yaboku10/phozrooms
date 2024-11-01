"""Modul för Phöz Rooms som sätter värden på de olika svårighetsgraderna"""

class Difficulty():
    """Klass för att sätta värden på svårighetsgrader"""
    def __init__(self, mapsize: int, phoz: int, hole: int, treasure: int, bats: int) -> None:
        """Sätter värdena för de olika svårighetsgraderna
                Argument:
                    mapsize(int): kartstorlek
                    phoz(int): mängd phöz
                    hole(int): mängd hål
                    treasure(int): mängd skatt
                    bats(int): mängd fladdermöss
                Retunerar:
                    None"""
        self.mapsize = 5 + mapsize
        self.START = 1
        self.phoz = 1 + phoz
        self.hole = 20 + hole
        self.treasure = 1 + treasure
        self.bats = 30 + bats

    def diff_attrib(self) -> tuple[int, int, int, int, int]:
        """Retunerar svårighetsgrads värderna"""
        return self.mapsize, self.phoz, self.hole, self.treasure, self.bats

easy = Difficulty(0, 0, 0, 0, 0)
normal = Difficulty(3, 1, 5, 2, 5)
hard = Difficulty(5, 2, 10, 2, 10)
fadder = Difficulty(11, 3, 10, 3, 10)
