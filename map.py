"""Modul för att skapa spelkartan till Phöz Rooms"""

import failsafe
import generation

START = 1

class Map():
    """Klass för kartan"""

    def __init__(self, diff: object, admin: bool) -> None:
        """initialiserande metod som först genererar en tom spelkarta och sedan
        kallar på en metod för att fylla den med objekt.
            Argument:
                diff(object): objekt för svårighetsgrads klassen.
                admin(bool): spelarens admin status
            Retunerar:
                None"""
        self.mapsize, self.phoz, self.hole, self.treasure, self.bats = diff.diff_attrib()

        self.map = [[0 for _ in range(self.mapsize)] for _ in range(self.mapsize)]  #  skapar en mapsize x mapsize stor lista, där _ är en temporär variabel
        generation.spawner(self.map, self.mapsize, START, self.phoz, self.hole, self.treasure, self.bats, admin)

    def generate_map(self, admin: bool) -> None:
        """Skriver ut spelkartan. Kollar först om mängden kartobjekt
        överstiger antalet 'rum' i matrisen, och genererar isåfall ingen karta."""
        if failsafe.is_spawn_limit(self.mapsize, START, self.phoz, self.hole, self.treasure, self.bats):
            if admin:  
                for row in self.map:
                    print(row)
        else:
            print("ERROR: Spawn items exceeds that of available spawn points.")
