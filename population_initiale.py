import functions as fc
import time
import random as rd






def contrainte2(solution, Intervenant, Mission):
    # 2.  Une mission ne peut etre assignee qu’a un intervenant ayant la meme competence (LSF ou LPC)
    for i in range(len(Intervenant)):
        for j in range(len(Mission)):
            if solution[i][j] == 1:
                if Intervenant[i][1] != Mission[j][4]:
                    return False
    return True


def contrainte3(solution, Intervenant, Mission):
    # 3.  Chaque Intervenant ne peut realiser qu’une mission a la fois
    for i in range(len(Intervenant)):
        missions = [y for y in range(len(Mission)) if solution[i][y] == 1]
        if len(missions) > 1:
            for j in missions:
                for x in missions:
                    if Mission[j][3] >= Mission[x][2] >= Mission[j][2] and (x != j) and (
                            Mission[j][1] == Mission[x][1]):
                        return False
    return True


def contrainte7(solution, Intervenant, Mission):
    # 7.  Respecter la limite des heures supplementaires autorisees a travailler par les intervenants sur le plan de planification (heures supplementaires = 10h/semaine, 2h/jour)
    # a modifier si on integre le délire de travail a mis temps / plein temps
    for i in range(len(Intervenant)):
        temps_travaille = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for j in range(len(Mission)):
            if solution[i][j] == 1:
                temps_travaille[Mission[j][1]] += Mission[j][3] - Mission[j][2]
        for k in temps_travaille:
            if temps_travaille[k] > 600:
                return False
    return True


def contrainte8(solution, Intervenant, Mission):
    # 8.  Respecter l’amplitude de la journee de travail de chaque intervenant (amplitude = 12h)
    for i in range(len(Intervenant)):
        temps_travaille = {1: [2000, 0], 2: [2000, 0], 3: [2000, 0], 4: [2000, 0], 5: [2000, 0]}
        for j in range(len(Mission)):
            if solution[i][j] == 1:
                if Mission[j][2] < temps_travaille[Mission[j][1]][0]:
                    temps_travaille[Mission[j][1]][0] = Mission[j][2]
                if Mission[j][3] > temps_travaille[Mission[j][1]][1]:
                    temps_travaille[Mission[j][1]][1] = Mission[j][3]
        for k in temps_travaille:
            if temps_travaille[k][1] - temps_travaille[k][0] > 720:
                return False
    return True


def contrainte9(solution, mat_dis, Mission, Inter):
    # 9.  Un intervenant doit avoir assez de temps pour se deplacer d’une mission a une autre.
    soluce = fc.activites_intervenants(solution, Inter, Mission)
    vitesse_deplacement = 833  # exprimée en m/minutes
    for edt in soluce:
        for jour in edt:
            temps_parcouru = -1
            if len(edt[jour]) == 2:
                depart = edt[jour][0] + 1
                arrivee = edt[jour][1] + 1
                temps_parcouru = mat_dis[depart][arrivee] / vitesse_deplacement
                if temps_parcouru > Mission[edt[jour][1]][2] - Mission[edt[jour][0]][3]:
                    return False

            elif len(edt[jour]) > 2:
                for i in range(len(edt[jour]) - 1):
                    depart = edt[jour][i] + 1
                    arrivee = edt[jour][i + 1] + 1
                    temps_parcouru = mat_dis[depart][arrivee] / vitesse_deplacement
                    if temps_parcouru > Mission[edt[jour][i + 1]][2] - Mission[edt[jour][i]][3]:
                        return False
    return True


def verif_contraintes(solution, Inter, Miss, mat_dis):
    """
    Ne vérifie pas toutes les contraintes car certaines contraintes ont besoin d'une solution finalisée pour etre validé.
    """
    if not contrainte2(solution, Inter, Miss):
        return False
    if not contrainte3(solution, Inter, Miss):
        return False
    if not contrainte7(solution, Inter, Miss):
        return False
    if not contrainte8(solution, Inter, Miss):
        return False
    if not contrainte9(solution, mat_dis, Miss, Inter):
        return False
    return True


def individu(i, j, Miss, Inter, mat_dis):
    """
    Renvoie une solution aléatoire.
    """

    solution = [[0 for i in range(len(Miss))] for j in range(len(Inter))]

    # pour une raison que j'ignore, laisser ce bloc permet de générer plus de solutions uniques, mais c'est aléatoire
    immuable = [rd.randint(0, len(Inter) - 1), rd.randint(0, len(Miss) - 1)]
    solution[immuable[0]][immuable[1]] = 1
    missions_assignees = [immuable[1]]

    immuable.append((i, j))
    solution[i][j] = 1
    missions_assignees.append(j)

    if not contrainte2(solution, Inter, Miss):
        return False

    for i in range(len(Inter)):
        for j in range(len(Inter)):
            if (i, j) not in immuable and j not in missions_assignees:
                solution[i][j] = 1
                if not verif_contraintes(solution, Inter, Miss, mat_dis):
                    solution[i][j] = 0
                else:
                    missions_assignees.append(j)

    for i in range(len(Miss)):
        if i not in missions_assignees:
            for j in range(len(Inter)):
                solution[j][i] = 1
                if not verif_contraintes(solution, Inter, Miss, mat_dis):
                    solution[j][i] = 0
                else:
                    missions_assignees.append(i)
                    break

    if not fc.contraintes(solution, Miss, Inter, mat_dis):
        return False

    # print("solution trouvée")
    return solution


def gen_n_solutions_uniques(n, Inter, Miss, mat_dis):
    """
    Génère n solutions aléatoires.
    Retourne une liste des n solutions.
    """
    toutes_les_solutions = []
    while len(toutes_les_solutions) < n:
        solutions = []
        for i in range(len(Inter)):
            for j in range(len(Miss)):
                res = individu(i, j, Miss, Inter, mat_dis)
                if res != False and res not in solutions:
                    solutions.append(res)
        for i in solutions:
            if i not in toutes_les_solutions:
                toutes_les_solutions.append(i)

    rd.shuffle(toutes_les_solutions)
    return toutes_les_solutions[:n]


def fichier_sol(nbIndividu, matrice_distance, intervenants, missions):
    start_time = time.time()
    solutions = gen_n_solutions_uniques(nbIndividu, intervenants, missions, matrice_distance)
    print("Temps d'execution: {} secondes pour {} solutions".format(time.time() - start_time, len(solutions)))

    with open("solutions.txt", "w") as f:
        for i in solutions:
            f.write(str(i) + "\n\n")


