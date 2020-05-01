
from PathManager import PathManager, PathFindingProblem
from probleme import Noeud, astar
import random

class SplicePathManager(PathManager):
    """ Facilite la gestion du pathFinding en utilisant le path splicing
    """
    def __init__(self, init, but, heuristique, bounds, walls):
        """
        -- init : (int, int)
        -- but  : (int, int)
        -- heuristique : (int, int) -> int
        -- bounds : (int, int)
        -- walls : list((int, int))
        """
        super().__init__(init, but, heuristique, bounds, walls)

    def checkStep_and_adjust(self, obstacles, currPos, verbose=False, m=1):
        """ Obstacles should contain players' positions aswell
        -- m : int, number of steps to recalculate
        """
        if self.check_step(obstacles, currPos, verbose=False):
            return
            
        if len(self.path) >= 1 and self.path[-1].etat in obstacles:
            # print("Adjusting path")

            if len(self.path) > m :
                sub_path = self.gen_path(PathFindingProblem(currPos, self.path[-1-m].etat, self.heuristique, self.bounds, obstacles))
                self.path = self.path[:-1-m:] + sub_path
                self.path_history.append("Adjustement len(self.path) > m : "+str([n.etat for n in self.path[:-1-m:]])+" + "+str([n.etat for n in sub_path]))

            else :
                self.path = self.gen_path(PathFindingProblem(currPos, self.but, self.heuristique, self.bounds, obstacles))
                self.path_history.append("Adjustement len(self.path) <= m : self.gen_path(PathFindingProblem("+str(currPos)+", "+str(self.but)+", "+str(self.heuristique)+", "+str(self.bounds)+", "+str(obstacles)+")")
                self.path_history.append("Path = "+str([n.etat for n in self.path]))


            for e in range(random.randint(0, 2)) :
                if e > 0 :
                    self.path.append(Noeud(self.currPos, 0))
            if verbose :
                print("new path=", [n.etat for n in self.path])

        # input("Press enter to resume ...")