
from probleme import Probleme, distManhattan, Noeud, astar
import random
from abc import ABCMeta, abstractmethod


class PathFindingProblem(Probleme):
    """ On definit un probleme comme étant: 
        - un état initial
        - un état but
        - une heuristique
        """
    """
    Les états sont des tuples.
    """
    def __init__(self, init, but, heuristique, bounds, obstacles):
        assert type(init) is tuple
        assert type(but) is tuple
        assert type(bounds) is tuple
        assert type(obstacles) is list

        super().__init__(init, but, heuristique)
        self.h = heuristique
        self.bounds = bounds
        self.obstacles = obstacles
        # input(str(bounds))

    def estBut(self, e):
        """ retourne vrai si l'état e est un état but
        """
        assert(isinstance(e, tuple)), "e not a tuple"
        return e == self.but
    
    def cost(self,e1,e2):
        """ donne le cout d'une action entre e1 et e2, 
            """
        assert(isinstance(e1, tuple)), "e1 not a tuple"
        assert(isinstance(e2, tuple)), "e2 not a tuple"

        return distManhattan(e1,e2)
    
    def successeurs(self,etat):
        """ retourne une liste avec les successeurs possibles
            """
        assert type(etat) is tuple, "etat not a tuple"
        w, h = self.bounds
        x, y = etat
        res = [(x + i, y + j) 
                for (i, j) in [(1, 0), (0, 1), (-1, 0), (0, -1)] 
                if i+x >= 0 and 
                j+y >= 0 and 
                i+x < w and 
                j+y < h and 
                (i+x, j+y) not in self.obstacles]
        # print("successeurs :", res)
        return res

    def immatriculation(self,etat):
        """ génère une chaine permettant d'identifier un état de manière unique
            """
        assert(isinstance(etat, tuple)), "etat not a tuple"

        x, y = etat
        return str(x) + " " + str(y)
    
    def h_value(self, etat, but):
        """ Retourne la valeur d'heuristique
            """
        assert(isinstance(etat, tuple)), "etat not a tuple"
        assert(isinstance(but, tuple)), "but not a tuple"

        return self.h(etat, but)
    
    # def set_obstacles(self, obs):
    #     self.obstacles = obs


class PathManager(object):
    """ Facilite la gestion du pathFinding
    """
    def __init__(self, init, but, heuristique, bounds, walls):
        """
        -- init : (int, int)
        -- but  : (int, int)
        -- heuristique : (int, int) -> int
        -- bounds : (int, int)
        -- walls : list((int, int))
        """
        self.currPos = init
        self.but = but
        self.heuristique = heuristique
        self.bounds = bounds
        self.walls = walls
        self.path_history = [] # Debug purpose

        """
        -- self.path : list(Noeud)
        """
        self.path = self.gen_path(PathFindingProblem(init, but, heuristique, bounds, walls))
        self.path_history.append("Initialization : self.gen_path(PathFindingProblem("+str(init)+", "+str(but)+", "+str(heuristique)+", "+str(bounds)+", walls)")
        self.path_history.append("Path = "+str([n.etat for n in self.path]))
        # self.path.pop() # First step is init

    def check_step(self, obstacles, currPos, verbose=False):
        """ Obstacles should contain players' positions aswell
        """
        assert type(obstacles) is list
        if len(obstacles) != 0:
            assert type(obstacles[0]) is tuple
        assert type(currPos) is tuple
        self.currPos = currPos

        if verbose :
            print("PATH:", [n.etat for n in self.path])
        if len(self.path) >= 1 and self.path[-1].etat == self.but and self.path[-1].etat in obstacles:
            x, y = self.currPos
            for i in range(5):
                x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
                self.path = [Noeud((x + x_inc, y + y_inc), 0)]
            self.path_history.append("Player blocking item:")
            self.path_history.append("Reducting path to "+str([n.etat for n in self.path]))
            
            return True
        return False
    @abstractmethod
    def checkStep_and_adjust(self, obstacles, currPos, verbose=False):
        """ Obstacles should contain players' positions aswell
        """
        if self.check_step(obstacles, currPos, verbose=False):
            return
        """Implement adjusting here"""


    def get_Path(self):
        return self.path

    def pop_step(self):
        if len(self.path) == 0 :
            self.path = self.gen_path(PathFindingProblem(self.currPos, self.but, self.heuristique, self.bounds, self.walls))
            self.path_history.append("Resetting path : "+str(self.currPos)+", "+str(self.but)+", "+str(self.heuristique)+", "+str(self.bounds)+", walls")

        self.path_history.append("Path pop " + str([n.etat for n in self.path]))
        return self.path.pop()

    def get_step(self):
        return self.path[-1]

    @staticmethod
    def gen_path(p):
        assert isinstance(p, PathFindingProblem)
        path = [astar(p)]
        n = 0
        while path[n].pere != None:
            assert isinstance(path[n].pere, Noeud)
            path.append(path[n].pere)
            n += 1
        return path
    def print_path_history(self):
        for ph in self.path_history:
            print(ph)
    def get_end(self):
        if len(self.path) > 0:
            return self.path[0]

# def augment_posList(posList):
#     newList = []
#     for (x, y) in posList:
#         newList.append((x, y))
#         newList.append((x+1, y))
#         newList.append((x, y+1))
#         newList.append((x-1, y))
#         newList.append((x, y-1))
#     return newList