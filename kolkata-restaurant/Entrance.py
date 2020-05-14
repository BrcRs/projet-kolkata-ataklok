import string
import kalkota_restaurants
from Strategy import RandomRestau, Tetu, MeanRegression, WrongStochasticChoice, StochasticChoice
# import os

# def cls():
#     os.system('cls' if os.name=='nt' else 'clear')

class Question(object):
    @staticmethod
    def yes_or_no(query, yes=["y"], no=["n"], error_msg="Invalid answer"):
        rep = ""
        while rep not in no and rep not in yes:
            rep = input(query)
            if rep not in yes and rep not in no:
                print(error_msg)
        return rep in yes
    
    @staticmethod
    def get_int(query, error_msg="Invalid answer"):
        rep = ""
        ok = False
        while len(rep) <= 0 or not ok:
            rep = input(query)
            ok = True
            if len(rep) <= 0:
                ok = False
                print(error_msg)
                continue
            for c in rep:
                if c not in string.digits:
                    ok = False
                    print(error_msg)
                    break
            
        return int(rep)

# Cet énorme script immonde est perfectible
# Bien à vous
                            # - Bruce Rose

def main():
    print("\nPlusieurs joueurs (*n*), qui habitent dans le même quartier,\n\
souhaitent se rendre dans un des *k* restaurants du quartier.\n\
Une fois que leur choix est effectué, les joueurs se rendent \n\
dans le restaurant choisi.\n\
* si un joueur est seul dans un restaurant, un plat lui est servi (gain = 1)\n\
* si plusieurs joueurs se trouvent dans un même restaurant, un joueur est \n\
choisi au hasard (de manière uniforme parmi tous les joueurs présents dans\n\
ce restaurant), et est servi (gain = 1). Les autres joueurs ne sont pas \n\
servis (gain = 0).\n\
Le jeu se déroule sur plusieurs itérations (*m*, fixé à l'avance).\n")

    input("Appuyez sur entrer...")

    """ Démo personnalisée ou par défaut ? """

    rep = False
    affirmatif = ["o", "oui", "O", "Oui", "OUI"]
    negatif = ["n", "non", "no", "Non", "NON"]
    # while rep not in negatif and rep not in affirmatif:
    #     rep = input("Voulez-vous lancer une \"partie\" avec paramètres personnalisés ? (o/n)\n >>> ")
    #     if rep not in affirmatif and not in negatif:
    #        print("\nRéponse invalide\n")

    rep = Question.yes_or_no(
        "\nVoulez-vous personnaliser les paramètres de votre partie ? (o/n)\n >>> ",
        affirmatif,
        negatif,
        "\nRéponse invalide\n"
    )

    if not rep:
        print("kalkota_restaurants.main()")
        # kalkota_restaurants.main()
        kalkota_restaurants.main()
    else:
        rep = Question.yes_or_no(
            "\nActiver le mode rapide (téléportation) ? (o/n)\n >>> ",
            affirmatif,
            negatif,
            "\nRéponse invalide\n"
        )
        if rep:
            fastmode=True
        else:
            fastmode=False

        """ Choisir le nombre d'itérations """
        nbIte = -1
        confirmation = False
        while not confirmation:
            nbIte = Question.get_int("\nPour combien d'itérations le jeu tournera (m) ?\
 (Insérez un nombre; nous recommandons 10)\n >>> ", "Réponse invalide")
            confirmation = Question.yes_or_no(
                "Le jeu tournera sur "+str(nbIte)+" itérations. Confirmer ? (o/n)\n >>> ",
                affirmatif,
                negatif,
                "\nRéponse invalide\n"
            )
        """ Choisir la vitesse de jeu """
        vitesse = -1
        vitesses = [5, 60, 240]
        vitesse = Question.get_int("\nVeuillez insérer le chiffre correspondant à une vitesse de jeu (nous recommandons Rapide pour rester éveillé) :\n\
1. Lent\n\
2. Standard\n\
3. Rapide\n\
 >>> ", "Réponse invalide")
        fps = vitesses[vitesse - 1]
        



        """ Choisir carte personnalisée ? """
        rep = not Question.yes_or_no(
            "\nSouhaitez-vous utiliser une carte par défaut ? (o/n)\n >>> ",
            affirmatif,
            negatif,
            "\nRéponse invalide\n"
        )

        nbJoueurs = 20
        nbRestaus = 20
        if rep:
            rep = False
            while not rep:
                fileName = input("\nVeuillez insérer le nom d'un fichier :\n")
                rep = Question.yes_or_no(
                    "Vous avez entré \'" + fileName + "\'\nConfirmer ?(o/n)\n >>> ",
                    affirmatif,
                    negatif,
                    "\nRéponse invalide\n"
                )
            # print("kalkota_restaurants.main(fileName)")
        else:
            nbJoueurs = -1
            """ Choisir le nombre de joueurs """
            while nbJoueurs > 20 or nbJoueurs < 1:
                nbJoueurs = Question.get_int("\nCombien de \"joueurs\" joueront ?\
 (Insérez un nombre entre 1 et 20)\n >>> ", "Réponse invalide")
                if nbJoueurs > 20 or nbJoueurs < 1:
                    print("Veuillez insérer un nombre entre 1 et 20")

            """ Choisir le nombre de restaurants """
            nbRestaus = -1
            while nbRestaus > 20 or nbRestaus < 1 or nbRestaus % 2 != 0:
                nbRestaus = Question.get_int("\nCombien y aura-t-il de restaurants ?\
 (Insérez un nombre entre 2 et 20, les nombres impairs ne sont pas permis)\n >>> ", "Réponse invalide")
                if nbRestaus > 20 or nbRestaus < 2:
                    print("Veuillez insérer un nombre entre 2 et 20")
                if nbRestaus % 2 != 0:
                    print("Veuillez insérer un nombre pair")
            fileName = 'kolkata_' + str(nbRestaus) +'_20'

        """ Choisir les équipes (1 seule, 2, par stratégie) """
        mode = -1
        while mode not in [1, 2]:
            mode = Question.get_int("\nVeuillez sélectionner un mode de jeu à l'aide des chiffres :\n\
1. Par équipes\n\
2. Aléatoire\n\
 >>> ", "Réponse invalide")
            if mode not in [1, 2]:
                print("Réponse invalide")
        nbEquipes = 0
        strats = []
        effectifs_equipes = []
        if mode == 1:
            """ Choisir les stratégies par équipe """
            while nbEquipes > nbJoueurs or nbEquipes < 1:
                nbEquipes = Question.get_int("\nVeuillez indiquer le nombre d'équipes (Pas plus de "+str(nbJoueurs)+") :\n >>> ", "Réponse invalide")
                if nbEquipes > nbJoueurs:
                    print("Veuillez insérer au plus autant d'équipes qu'il n'y a de joueurs")
                if nbEquipes < 1:
                    print("Au moins *une* équipe est requise")

            print("\nVeuillez indiquer le nombre de joueurs pour chaque équipe :")
            nbJoueursRestants = nbJoueurs
            while len(effectifs_equipes) == 0 or 0 in effectifs_equipes:
                for i in range(nbEquipes - 1):
                    if nbJoueursRestants <= 0:
                        break
                    effectif = -1
                    while effectif < 1 or effectif > nbJoueurs:
                        print("\nEquipe", i, ":")
                        effectif = Question.get_int("("+str(nbJoueursRestants)+" joueur(s) restant(s)) >>> ", "Réponse invalide")
                        if effectif < 1:
                            print("Une équipe comporte au moins 1 joueur")
                        if effectif > nbJoueurs:
                            print("Vous n'avez pas assez de joueurs")
                    effectifs_equipes.append(effectif)
                    nbJoueursRestants -= effectif
                print("Equipe", nbEquipes - 1, ":", nbJoueursRestants)
                effectifs_equipes.append(nbJoueursRestants)
                if 0 in effectifs_equipes:
                    print("Une équipe a 0 joueurs. Veuillez recommencer.")
                    effectifs_equipes = []
                    nbJoueursRestants = nbJoueurs



            print("\nVeuillez attribuer à chaque équipe le numéro correspondant à sa stratégie")
            strats_available = [RandomRestau, Tetu, MeanRegression, WrongStochasticChoice, StochasticChoice]
            for i in range(nbEquipes):
                strat_id = -1
                while strat_id < 1 or strat_id > len(strats_available):
                    print("\nEquipe", i,":")
                    strat_id = Question.get_int("Veuillez sélectionner une stratégie à l'aide des chiffres :\n\
1. RandomRestau\n\
2. Tetu\n\
3. MeanRegression\n\
4. WrongStochasticChoice\n\
5. StochasticChoice\n\
 >>> ", "Réponse invalide")
                    if strat_id < 1 or strat_id > len(strats_available):
                        print("Veuillez insérer un chiffre valide")
                strats.append(strats_available[strat_id-1])


        
        kalkota_restaurants.main(nbIte, fileName, nbJoueurs, nbRestaus, nbEquipes, strats, fps, effectifs_equipes, _fastmode=fastmode)




if __name__ == "__main__":
    main()