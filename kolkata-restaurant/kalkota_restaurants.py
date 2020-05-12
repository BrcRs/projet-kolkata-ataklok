# -*- coding: utf-8 -*-

# Nicolas, 2020-03-20

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random 
import numpy as np
import sys

from probleme  import distManhattan
from PathSplicing import SplicePathManager
from KolkataPath import KolkataPathManager, IdlePathManager
from Strategy import RandomRestau, Tetu, MeanRegression, WrongStochasticChoice, StochasticChoice, Idle

import math
    
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None, _fps=60):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'kolkata_6_10'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = _fps#240#5  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
def main(_m_ite=5, _map='kolkata_6_10', _nbPlayers=20, _nbRestaus=20, _nbTeams=0, _strats=[], _fps=5, _effectifs=[], _fastmode=False):

    #for arg in sys.argv:
    m_ite = _m_ite # default # Kolkata
    if _fastmode:
        iterations=23
    else:
        iterations = 60#20 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
        m_ite = int(sys.argv[2])
    print ("Iterations: ")
    print (iterations)
    print("Nb rounds:")
    print(m_ite)

    init(_map, (_fps/20) * _nbPlayers)
    # init()
    
    
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
    nbLignes = game.spriteBuilder.rowsize
    nbColonnes = game.spriteBuilder.colsize
    print("lignes", nbLignes)
    print("colonnes", nbColonnes)
    
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = min(_nbPlayers, len(players))
    
    
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    
    # on localise tous les objets  ramassables (les restaurants)
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
    nbRestaus = min(_nbRestaus, len(goalStates))
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
    
    # on liste toutes les positions permises
    allowedStates = [(x,y) for x in range(nbLignes) for y in range(nbColonnes)\
                     if (x,y) not in (wallStates + goalStates)] 
    

    # on cree une structure qui habritera les infos des joueurs
    players_data = {j:{} for j in range(nbPlayers)}

    # Initialisation des stratégies et des gains
    # Et des équipes !
    nbTeams = _nbTeams
    teams = {}
    if nbTeams == 0:
        """ Random setup """
        strategies = [RandomRestau, Tetu, MeanRegression, WrongStochasticChoice, StochasticChoice]
        # teams = {strat.__str__():[] for strat in strategies}
        print(teams)
        for j in range(nbPlayers):
            strat = (random.choice(strategies))
            players_data[j]['strat'] = strat(nbRestaus)
            players_data[j]["gain"] = 0
            if str(players_data[j]['strat']) in teams.keys():
                teams[str(players_data[j]['strat'])].append(j)
            else:
                teams[str(players_data[j]['strat'])] = [j]
        """"""
    else:
        """ Multiple Teams setup """
        # players_per_team = int(nbPlayers/nbTeams)
        players_placed = 0
        for cptTeams in range(nbTeams):
            strat = _strats[cptTeams]
            teams['Team '+str(cptTeams+1)+' : ' + strat.__str__()] = []

            for j in range(players_placed, players_placed + _effectifs[cptTeams]):
                players_data[j]['strat'] = strat(nbRestaus)
                players_data[j]["gain"] = 0
                teams['Team '+str(cptTeams+1)+' : ' + strat.__str__()].append(j)
            players_placed += _effectifs[cptTeams]
        """"""
    #==========================================================================
    # Boucle principale
    #==========================================================================
    for r in range(m_ite):
        print("-= Round", r+1, "=-")
        # num_restau : list(num_player)
        players_on_restau = {restau:[] for restau in range(nbRestaus)}
        #-------------------------------
        # Placement aleatoire des joueurs, en évitant les obstacles
        #-------------------------------
            
        posPlayers = initStates

        
        for j in range(nbPlayers):
            x,y = random.choice(allowedStates)
            players[j].set_rowcol(x,y)
            game.mainiteration()
            posPlayers[j]=(x,y)
            players_data[j]["pos"] = posPlayers[j]


            
            
        
        #-------------------------------
        # chaque joueur choisit un restaurant
        # Initialisation des path finders
        #-------------------------------

        # restau=[0]*nbPlayers
        for j in range(nbPlayers):
            # c = random.randint(0,nbRestaus-1)
            # # print(c)
            # restau[j]=c
            # input("debug: j=" + str(j))
            # input("debug: nbPlayers=" + str(nbPlayers))
            players_data[j]["restau"] = players_data[j]['strat'].choice()
            # if j == 0 :
                # print("Player", j, "is going to restau n°", players_data[j]["restau"])

            if players_data[j]["restau"] < 0:
                players_data[j]["path finder"] = IdlePathManager(
                players[j].get_rowcol())
            else:
                players_data[j]["path finder"] = KolkataPathManager(
                players[j].get_rowcol(), 
                goalStates[players_data[j]["restau"]], 
                distManhattan, 
                (game.screen.get_width()/game.spriteBuilder.spritesize, 
                game.screen.get_height()/game.spriteBuilder.spritesize), 
                wallStates)

            # print(j, "is going to", goalStates[players_data[j]["restau"]])

        
        #-------------------------------
        # Boucle principale de déplacements 
        #-------------------------------
        
            
        for i in range(iterations):
            
            for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
                ## Boost performances, but the game gets wierd
                if posPlayers[j] == goalStates[players_data[j]["restau"]] and _fastmode:
                    continue
                old_row,old_col = posPlayers[j]
                if not _fastmode:
                    players_data[j]["path finder"].set_currPos((old_row,old_col))
                # x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
                # next_row = row+x_inc
                # next_col = col+y_inc
                # and ((next_row,next_col) not in posPlayers)
                if _fastmode:
                    next_row, next_col = players_data[j]["path finder"].get_end().etat
                else:
                    next_row, next_col = players_data[j]["path finder"].pop_step().etat

                if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=19 and next_col>=0 and next_col<=19:
                    players[j].set_rowcol(next_row,next_col)
                    # print ("pos :", j, next_row,next_col)
                    game.mainiteration()
        
                    col=next_col
                    row=next_row
                    posPlayers[j]=(row,col)
                
        
            
                
                # si on est à l'emplacement d'un restaurant, on s'arrête
                if (row,col) == goalStates[players_data[j]["restau"]] and (old_row, old_col) != (row, col):
                    #o = players[j].ramasse(game.layers)
                    game.mainiteration()
                    print (j, "->", players_data[j]["restau"])
                    players_on_restau[players_data[j]["restau"]].append(j)
                # goalStates.remove((row,col)) # on enlève ce goalState de la liste
                    
                    
                    break
        
        freq = []
        freq_plyrs = []
        # Fin du round, distribution des gains
        for restau in range(nbRestaus):
            plyrs = players_on_restau[restau]
            freq.append(len(plyrs))
            freq_plyrs.append(plyrs)
            if len(plyrs) > 0:
                players_data[random.choice(plyrs)]['gain'] += 1
        # Affichage des gain
        print("Fréquentation :", freq)
        print("Répartition :", freq_plyrs)
        scores = [players_data[j]['gain'] for j in range(nbPlayers)]
        print("Scores :", scores)

        for t in teams.keys():
            # print("Score", t, " :", math.fsum([scores[j] for j in teams[t]]))
            moy = math.fsum([scores[j] for j in teams[t]]) / int(len(teams[t]))
            moy /= m_ite
            print("Score moyen d'un joueur de",t,":", (round(moy * 10000))/100, "%")

        # on informe les joueurs des fréquentations
        for j in range(nbPlayers):
            players_data[j]['strat'].append(freq)

    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    


