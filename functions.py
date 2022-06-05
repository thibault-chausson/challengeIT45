import random
import json
import numpy as np
import copy


MATRICE_DISTANCE = []
INTERVENANTS = []
MISSIONS = []
SOLUTIONS = []

def charge_fichier_csv(dossier):
    """
    Charge le contenue du fichier csv dans les variables globales
    """
    with open(f"Instances/{dossier}/Distances.csv", 'r') as fichier:
        lignes = fichier.read().split('\n')
        if lignes[-1] == '':
            lignes = lignes[:-1]
        for ligne in lignes:
            MATRICE_DISTANCE.append(list(map(float, ligne.split(','))))

    with open(f"Instances/{dossier}/Intervenants.csv", 'r') as fichier:
        lignes = fichier.read().split('\n')
        if lignes[-1] == '':
            lignes = lignes[:-1]
        for ligne in lignes:
            INTERVENANTS.append(ligne.split(','))
    
    with open(f"Instances/{dossier}/Missions.csv", 'r') as fichier:
        lignes = fichier.read().split('\n')
        if lignes[-1] == '':
            lignes = lignes[:-1]
        for ligne in lignes:
            MISSIONS.append(ligne.split(','))
    
    # Changements des chiffres de types str en type int
    for i in range(len(INTERVENANTS)):
        for j in range(len(INTERVENANTS[i])):
            try:
                INTERVENANTS[i][j] = int(INTERVENANTS[i][j])
            except:
                pass

    for i in range(len(MISSIONS)):
        for j in range(len(MISSIONS[i])):
            try:
                MISSIONS[i][j] = int(MISSIONS[i][j])
            except:
                pass

    return (MATRICE_DISTANCE, INTERVENANTS, MISSIONS)

def stats_heures(solution):
    """
    Renvoies des informations sur le nombre d'heures travaillées par les intervenants
    """
    inters = len(INTERVENANTS)
    nb_heuresTravaille = np.zeros(inters)
    nb_heuresNonTravaille = np.zeros(inters)
    nb_heureSup = np.zeros(inters)

    for i in range(inters):
        for j in range(len(MISSIONS)):
            if solution[i][j] == 1:
                nb_heuresTravaille[i] += (MISSIONS[j][3] - MISSIONS[j][2]) / 60

        tps = nb_heuresTravaille[i] - INTERVENANTS[i][3]
        if tps < 0:
            nb_heuresNonTravaille[i] += abs(tps)
        else:
            nb_heureSup[i] = abs(tps)
    
    return nb_heuresTravaille, nb_heuresNonTravaille, nb_heureSup


def contraintes(solution):
    """
    Vérifie si la solution est valide
    1.  Toutes les missions doivent etre affectees
    2.  Une mission ne peut etre assignee qu’a un intervenant ayant la meme competence
    3.  Chaque Intervenant ne peut realiser qu’une mission a la fois
    4.  Une mission est realisee par un et un seul Intervenant
    5.  Accorder a chaque intervenant au moins une heure de pause-midi par jour entre midi et 14h
    6.  Respecter les heure  maximales a travailler par jour (Temps Plein = 8h/jour, Temps partiel = 6h/jour)
    7.  Respecter la limite des heures supplementaires autorisees a travailler par les intervenants sur le plan de planification (heures supplementaires = 10h/semaine, 2h/jour)
    8.  Respecter l’amplitude de la journee de travail de chaque intervenant (amplitude = 12h)
    9.  Un intervenant doit avoir assez de temps pour se deplacer d’une mission a une autre.
    """

    # 1.  Toutes les missions doivent etre affectees
    # 4.  Une mission est realisee par un et un seul Intervenant
    for i in range(len(MISSIONS)):
        compteur = 0
        for j in range(len(INTERVENANTS)):
            if solution[j][i] == 1:
                compteur += 1
        # Si une colonne à plus de un 1, alors on s'arrete. (4. La mission est affectée à plusieurs intervenants)
        # Si une colonne n'a pas de 1, alors on s'arrete. (1. La mission n'est pas affectee)
        if compteur != 1:
            return False

    # 2.  Une mission ne peut etre assignee qu’a un intervenant ayant la meme competence (LSF ou LPC)
    for i in range(len(INTERVENANTS)):
        for j in range(len(MISSIONS)):
            if solution[i][j] == 1:
                if INTERVENANTS[i][1] != MISSIONS[j][4]:
                    return False

    # 3.  Chaque Intervenant ne peut realiser qu’une mission a la fois
    for i in range(len(INTERVENANTS)):
        missions = [y for y in range(len(MISSIONS)) if solution[i][y] == 1]
        if len(missions) > 1:
            for j in missions:
                for x in missions:
                    if MISSIONS[j][3] >= MISSIONS[x][2] >= MISSIONS[j][2] and (x != j) and (MISSIONS[j][1] == MISSIONS[x][1]):
                        return False


    # 5.  Accorder a chaque intervenant au moins une heure de pause-midi par jour entre midi et 14h
    # on ignore cette contrainte pour le moment

    # 6.  Respecter les heures maximales a travailler par jour (Temps Plein = 8h/jour, Temps partiel = 6h/jour)
    """ Contrainte bizarre, a éclaircir.
    for i in range(len(INTERVENANTS)):
        temps_travaille = {1:0, 2:0, 3:0, 4:0, 5:0}
        for j in range(len(MISSIONS)):
            if solution[i][j] == 1:
                temps_travaille[MISSIONS[j][1]] += MISSIONS[j][3] - MISSIONS[j][2]
        for k in temps_travaille:
            if not (360 < temps_travaille[k] < 480):
                return False
    """
    
    # 7.  Respecter la limite des heures supplementaires autorisees a travailler par les intervenants sur le plan de planification (heures supplementaires = 10h/semaine, 2h/jour)
    # a modifier si on integre le délire de travail a mis temps / plein temps
    for i in range(len(INTERVENANTS)):
        temps_travaille = {1:0, 2:0, 3:0, 4:0, 5:0}
        for j in range(len(MISSIONS)):
            if solution[i][j] == 1:
                temps_travaille[MISSIONS[j][1]] += MISSIONS[j][3] - MISSIONS[j][2]
        for k in temps_travaille:
            if temps_travaille[k] > 600:
                return False

    # 8.  Respecter l’amplitude de la journee de travail de chaque intervenant (amplitude = 12h)
    for i in range(len(INTERVENANTS)):
        temps_travaille = {1:[2000, 0], 2:[2000, 0], 3:[2000, 0], 4:[2000, 0], 5:[2000, 0]}
        for j in range(len(MISSIONS)):
            if solution[i][j] == 1:
                if MISSIONS[j][2] < temps_travaille[MISSIONS[j][1]][0]:
                    temps_travaille[MISSIONS[j][1]][0] = MISSIONS[j][2]
                if MISSIONS[j][3] > temps_travaille[MISSIONS[j][1]][1]:
                    temps_travaille[MISSIONS[j][1]][1] = MISSIONS[j][3]
        for k in temps_travaille:
            if temps_travaille[k][1] - temps_travaille[k][0] > 720:
                return False


    with open("res.txt", "a") as fichier:
        fichier.write(f"8:\n{str(solution)}\n\n")
    
    #print("8 passé")
    # 9.  Un intervenant doit avoir assez de temps pour se deplacer d’une mission a une autre.
    soluce = activites_intervenants(solution)
    vitesse_deplacement = 833 # exprimée en m/minutes

    for edt in soluce:
        for jour in edt:
            temps_parcouru = -1
            if len(edt[jour]) == 2:
                depart = edt[jour][0] + 1
                arrivee = edt[jour][1] + 1
                temps_parcouru = MATRICE_DISTANCE[depart][arrivee] / vitesse_deplacement
                if temps_parcouru > MISSIONS[edt[jour][1]][2] - MISSIONS[edt[jour][0]][3]:
                    return False

            elif len(edt[jour]) > 2:
                for i in range(len(edt[jour])-1):
                    depart = edt[jour][i] + 1
                    arrivee = edt[jour][i+1] + 1
                    temps_parcouru = MATRICE_DISTANCE[depart][arrivee] / vitesse_deplacement
                    if temps_parcouru > MISSIONS[edt[jour][i + 1]][2] - MISSIONS[edt[jour][i]][3]:
                        return False
    
    #print("9 passé")
    
    return True


def read_sols(fichier):
    with open("TRUE_res.txt", 'r') as f:
        fich = f.read().split('\n\n')[:-1]
    for i in fich:
        SOLUTIONS.append(json.loads(i))

    return SOLUTIONS


def activites_intervenants(solution):
    """
    Renvoie les id des missions effectues par chaque intervenant, rangés dans l'ordre horaire
    """
    miss_intervenants = []
    for i in range(len(INTERVENANTS)):
        missions = {1:[], 2:[], 3:[], 4:[], 5:[]}
        edt = {1:[], 2:[], 3:[], 4:[], 5:[]}
        for j in range(len(MISSIONS)):
            if solution[i][j] == 1:
                missions[MISSIONS[j][1]].append((j, MISSIONS[j][2]))

        for jour in missions:
            temp = sorted(missions[jour], key=lambda x: x[1])
            edt[jour] = [i[0] for i in temp]

        miss_intervenants.append(edt)
    
    return miss_intervenants


def choixParents(fitness): #fonction qui choisit les parents à partir de leur fitness (decroissante) et renvoie les indices des parents
    """
    Choix par roulette des parents
    """
    nbSol = len(fitness)
    ponde = np.zeros(nbSol)
    aux = np.zeros(nbSol)
    for i in range(nbSol):
        aux[i] = 1 / fitness[i]
    for i in range(nbSol):
        ponde[i] = (aux[i] / np.sum(aux))
    Parent1 = random.choices(range(nbSol), weights=ponde, k=1)
    ponde[Parent1[0]] = 0
    Parent2 = random.choices(range(nbSol), weights=ponde, k=1)
    return (Parent1[0], Parent2[0])




def reproduction(solution1, solution2, ligDebut, ligFin, colDebut, colFin): #fonction qui realise la reproduction entre deux solutions
    """
    Retourne la solution fille
    Attention : la ligne de fin et col de fin a eu un +1 pour palier au range qui fait -1
    """
    nblig = len(solution1)
    nbcol = len(solution1[0])
    fille = copy.deepcopy(solution1)
    for i in range(ligDebut, ligFin+1):
        for j in range(colDebut, colFin+1):
            fille[i][j] = solution2[i][j]
    return fille


def tri_langage(Mission):
    """
    Tri les missions par le langage des étudiants
    """
    LPC = []
    LSF= []
    for i in range(len(Mission)):
        if Mission[i][4] == "LPC":
            LPC.append(Mission[i])
        else:
            LSF.append(Mission[i])
    return LPC, LSF


def mutation(solution):
    """
    Retourne la solution mutée
    """
    nblig = len(solution)
    nbcol = len(solution[0])
    rdLine1 = random.randint(0, nblig-1)
    rdCol = random.randint(0, nbcol-1)
    rdLine2 = random.randint(0, nblig-1)
    (solution[rdLine1][rdCol], solution[rdLine2][rdCol]) = (solution[rdLine2][rdCol], solution[rdLine1][rdCol])
    return solution

