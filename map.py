import failsafe
import generation
import movement

MAPSIZE = 5
START = 1
PHOZ = 1
HOLE = 20  #  I %
TREASURE = 1
BATS = 30  #  I %

class Map():

    def __init__(self, diff, admin):
        self.mapsize, self.phoz, self.hole, self.treasure, self.bats = diff.diff_attrib()

        self.map = [[0 for _ in range(self.mapsize)] for _ in range(self.mapsize)]  #  skapar en mapsize x mapsize stor lista, där _ är en temporär variabel
        generation.spawner(self.map, self.mapsize, START, self.phoz, self.hole, self.treasure, self.bats, admin)
    def __str__(self):
        return str(self.map)

    def generate_map(self, admin):
        """Genererar spelkartan. Kollar först om mängden kartobjekt
        överstiger antalet 'rum' i matrisen, och genererar isåfall ingen karta."""
        if failsafe.is_spawn_limit(self.mapsize, START, self.phoz, self.hole, self.treasure, self.bats):
            if admin:   
                for row in self.map:
                    print(row)
        else:
            print("Spawn items exceeds that of available spawn points")