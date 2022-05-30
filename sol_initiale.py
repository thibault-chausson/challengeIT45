# Fichier proposant des fonctions pour créer des solutions initiales
import random


def cree_solution_initiale(INTERVENANTS, MISSIONS):
    """
    vérifie aucune contrainte = nulle a chier
    """
    # Créer une matrice de 0
    solution = []
    for i in range(len(INTERVENANTS)):
        solution.append([0 for i in range(len(MISSIONS))])

    # Remplissage de la matrice avec des 1, signifiant que l'intervenant est affecté à la mission
    for i in range(len(MISSIONS)):
        intervenant = random.randint(0, len(INTERVENANTS) - 1)
        solution[intervenant][i] = 1
    
    return solution


def cree_solution_initiale_2(INTERVENANTS, MISSIONS):
    """
    vérifie une seule contrainte = pourrie
    """
    a=[[0,0,0,1], [0,0,1,0], [0,1,0,0], [1,0,0,0]] # a tester, idée de création d'une solution initiale
    solution = []
    for i in range(len(MISSIONS)):
        solution.append(a[i%4])
    random.shuffle(solution)
    transpose = list(map(list, zip(*solution)))

    return transpose

def cree_solution_initiale(INTERVENANTS, MISSIONS):
    """
    marche pas vraiment je crois
    """
    a = []
    solution = []
    lpc = [i for i in range(len(INTERVENANTS)) if INTERVENANTS[i][1] == "LPC"]
    lsf = [i for i in range(len(INTERVENANTS)) if INTERVENANTS[i][1] == "LSF"]

    for i in range(len(INTERVENANTS)):
        a.append([0 for j in range(len(INTERVENANTS))])
        a[i][i] = 1

    jour = -1
    tourniquet_lpc = lpc.index(random.choice(lpc))
    tourniquet_lsf = lsf.index(random.choice(lsf))
    for i in range(len(MISSIONS)):
        if MISSIONS[i][1] != jour:
            jour = MISSIONS[i][1]
            if MISSIONS[i][4] == "LPC":
                choix = random.choice(lpc)
                solution.append(a[choix])
                tourniquet_lpc = lpc.index(choix)
            else:
                choix = random.choice(lsf)
                solution.append(a[choix])
                tourniquet_lsf = lsf.index(choix)
        else:
            if MISSIONS[i][4] == "LPC":
                tourniquet_lpc += 1
                solution.append(a[lpc[tourniquet_lpc % (len(INTERVENANTS)//2)]])
            else:
                tourniquet_lsf += 1
                solution.append(a[lsf[tourniquet_lsf % (len(INTERVENANTS)//2)]])

    transpose = list(map(list, zip(*solution)))
    
    return transpose


def cree_vrai_aleatoire(INTERVENANTS, MISSIONS):
    """
    vérifie les contraintes 1, 2, 3, 4 et est assez rapide.
    """
    sol = []
    a=[[0,0,0,1], [0,0,1,0], [0,1,0,0], [1,0,0,0]]
    for i in range(len(MISSIONS)):
        if MISSIONS[i][4] == 'LPC':
            sol.append(a[random.choice([0,2])])
        else:
            sol.append(a[random.choice([1,3])])

    return list(map(list, zip(*sol)))


def nouvelle_solution(INTERVENANTS, MISSIONS):
    """
    vérifies actuellement les contraintes 1, 2, 3, 4, 7, 8 (9 a faire plus tard)
    pas aléatoire, purement algorithmique
    """
    ban_list = []
    solution = []
    
    for i in range(len(INTERVENANTS)):
        missions_a_faire = []
        for j in range(len(MISSIONS)):
            if j not in ban_list and (INTERVENANTS[i][1] == MISSIONS[j][4]): # Vérification de la contrainte 2 et 4
                if missions_a_faire == [] or 1 not in missions_a_faire:
                    missions_a_faire.append(1)
                    ban_list.append(j)
                elif intervenant_libre(missions_a_faire, j): # Vérification de la contrainte 3 et peut-etre 9 (plus tard)
                    missions_a_faire.append(1)
                    ban_list.append(j)
                else:
                    missions_a_faire.append(0)
            else:
                missions_a_faire.append(0)
        solution.append(missions_a_faire)
    
    print("Longueur ban_list:", len(ban_list))
    if len(ban_list) != len(MISSIONS):
        print("Pas toutes les missions sont attribuées :(")
        return None