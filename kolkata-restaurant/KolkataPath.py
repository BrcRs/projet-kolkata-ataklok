from PathManager import PathManager
from probleme import Noeud


class KolkataPathManager(PathManager):
    def __init__(self, init, but, heuristique, bounds, walls):
        super().__init__(init, but, heuristique, bounds, walls)

    def pop_step(self):
        if len(self.path) == 0 :
            self.path = [Noeud(self.currPos, 0)]
            self.path_history.append("waiting : "+str(self.currPos)+", "+str(self.but)+", "+str(self.heuristique)+", "+str(self.bounds)+", walls")

        self.path_history.append("Path pop " + str([n.etat for n in self.path]))
        return self.path.pop()

    def set_currPos(self, pos):
        self.currPos = pos