import random
import math

class Strategy(object):

    def __init__(self, nbRestaus):
        """
        -- self.knowledge : list(list(int))
        """
        self.nbRestaus = nbRestaus
        self.knowledge = []

    def append(self, freqList):
        """
        -- freqList : list(int)
        """
        self.knowledge.append(freqList)
    
    def choice(self):
        """ Returns the number of a restau
        """
        raise NotImplementedError()


class RandomRestau(Strategy):
    def __init__(self, nbRestaus):
        super().__init__(nbRestaus)
    @staticmethod
    def __str__():
        return "Random"

    def choice(self):
        return random.randint(0, self.nbRestaus - 1)


class Tetu(Strategy):
    def __init__(self, nbRestaus):
        super().__init__(nbRestaus)
        self.favori = random.randint(0, self.nbRestaus - 1)
    @staticmethod
    def __str__():
        return "Tetu"

    def choice(self):
        return self.favori

class Idle(Strategy):
    def __init__(self, nbRestaus):
        super().__init__(nbRestaus)
    @staticmethod
    def __str__():
        return "Idle"

    def choice(self):
        return -1


class MeanRegression(Strategy):
    """
    Cette stratégie se base sur le principe de retour à la normale
    """
    def __init__(self, nbRestaus):
        super().__init__(nbRestaus)
        """
        -- self.mean_per_restau : list(list(double))
        -- self.means : list()
        """
        self.mean_per_restau = []
        self.means = []
    @staticmethod
    def __str__():
        return "Regression to the mean"

    def choice(self):
        if len(self.knowledge) <= 0:
            return random.randint(0, self.nbRestaus - 1)
        else:
            curr_means = []
            if len(self.mean_per_restau) > 0:
                for i in range(self.nbRestaus):
                    curr_means.append((self.knowledge[-2][i] * len(self.mean_per_restau) + self.knowledge[-1][i]) / (len(self.mean_per_restau) + 1))
            else:
                for i in range(self.nbRestaus):
                    curr_means.append(self.knowledge[-1][i])
            self.mean_per_restau.append(curr_means)
            self.means.append(math.fsum(self.mean_per_restau[-1]) / self.nbRestaus)
            
            # """ Tactic 1 """
            # maximum = 0
            # for i in range(1, len(self.mean_per_restau[-1])):
            #     if self.mean_per_restau[-1][i] > self.mean_per_restau[-1][maximum]:
            #         maximum = i
            # return maximum
            # """"""

            """ Tactic 2 """
            # print(self.mean_per_restau)

            scores = [0] * self.nbRestaus

            for restau in range(self.nbRestaus):
                for i in range(len(self.mean_per_restau)-1, -1, -1):
                    # print(i)
                    if self.knowledge[i][restau] > self.means[i]:
                        scores[restau] += 1
                    else:
                        break
            maximum = 0
            for i in range(1, len(scores)):
                if scores[i] > scores[maximum]:
                    maximum = i
            # print("\t", scores)
            # print("\tmaximum indix:", maximum)
            return maximum
            """"""

class WrongStochasticChoice(Strategy):
    def __init__(self, nbRestaus):
        super().__init__(nbRestaus)
        self.last_restau = -1

    @staticmethod
    def __str__():
        return "Wrong Stochastic Choice"
    
    def choice(self):
        if len(self.knowledge) <= 0:
            restau = random.randint(0, self.nbRestaus - 1)
            self.last_restau = restau
            return restau
        else:
            # 0 -> 1/0+1 -> 1
            # 1 -> 1/1+1 -> 0.5
            # 2 -> 1/2+1 -> 0.3333...
            # etc
            restau = 0
            best_div = 1000
            for r in range(self.nbRestaus):
                div = (1/(self.knowledge[-1][r] + 1))
                if random.randint(0, 100) < div * 100:
                    if div < best_div:
                        best_div = div
                        restau = r

            self.last_restau = restau
            return restau


class StochasticChoice(Strategy):
    def __init__(self, nbRestaus):
        super().__init__(nbRestaus)
        self.last_restau = -1
        
    @staticmethod
    def __str__():
        return "Stochastic Choice"

    
    def choice(self):
        if len(self.knowledge) <= 0:
            restau = random.randint(0, self.nbRestaus - 1)
            self.last_restau = restau
            return restau
        else:
            # 0 -> 1/0+1 -> 1
            # 1 -> 1/1+1 -> 0.5
            # 2 -> 1/2+1 -> 0.3333...
            # etc
            restau = self.last_restau
            div = (1/(self.knowledge[-1][self.last_restau] + 1))
            if random.randint(0, 100) > div * 100:    
                while restau == self.last_restau:
                    restau = random.randint(0, self.nbRestaus-1)
                self.last_restau = restau
            return restau