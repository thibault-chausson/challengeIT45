import json as js

def charge_fichier_csv(dossier):
    """
    Charge le contenue du fichier csv dans les variables globales
    """
    matrice_distance=[]
    intervenants = []
    missions = []
    with open(f"Instances/{dossier}/Distances.csv", 'r') as fichier:
        lignes = fichier.read().split('\n')
        if lignes[-1] == '':
            lignes = lignes[:-1]
        for ligne in lignes:
            matrice_distance.append(list(map(float, ligne.split(','))))

    with open(f"Instances/{dossier}/Intervenants.csv", 'r') as fichier:
        lignes = fichier.read().split('\n')
        if lignes[-1] == '':
            lignes = lignes[:-1]
        for ligne in lignes:
            intervenants.append(ligne.split(','))

    with open(f"Instances/{dossier}/Missions.csv", 'r') as fichier:
        lignes = fichier.read().split('\n')
        if lignes[-1] == '':
            lignes = lignes[:-1]
        for ligne in lignes:
            missions.append(ligne.split(','))

    # Changements des chiffres de types str en type int
    for i in range(len(intervenants)):
        for j in range(len(intervenants[i])):
            try:
                intervenants[i][j] = int(intervenants[i][j])
            except:
                pass

    for i in range(len(missions)):
        for j in range(len(missions[i])):
            try:
                missions[i][j] = int(missions[i][j])
            except:
                pass

    return (matrice_distance, intervenants, missions)


def charger_solution(dossier):
    with open(f"./{dossier}", 'r') as f:
        fich = f.read().split('\n\n')[:-1]
    solutions = [js.loads(i) for i in fich]
    return solutions


def contraintes(solution, Mis, Int, Dis):
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
    for i in range(len(Mis)):
        compteur = 0
        for j in range(len(Int)):
            if solution[j][i] == 1:
                compteur += 1
        # Si une colonne à plus de un 1, alors on s'arrete. (4. La mission est affectée à plusieurs intervenants)
        # Si une colonne n'a pas de 1, alors on s'arrete. (1. La mission n'est pas affectee)
        if compteur != 1:
            return False

    # 2.  Une mission ne peut etre assignee qu’a un intervenant ayant la meme competence (LSF ou LPC)
    for i in range(len(Int)):
        for j in range(len(Mis)):
            if solution[i][j] == 1:
                if Int[i][1] != Mis[j][4]:
                    return False

    # 3.  Chaque Intervenant ne peut realiser qu’une mission a la fois
    for i in range(len(Int)):
        missions = [y for y in range(len(Mis)) if solution[i][y] == 1]
        if len(missions) > 1:
            for j in missions:
                for x in missions:
                    if Mis[j][3] >= Mis[x][2] >= Mis[j][2] and (x != j) and (
                            Mis[j][1] == Mis[x][1]):
                        return False

    # 5.  Accorder a chaque intervenant au moins une heure de pause-midi par jour entre midi et 14h
    # on ignore cette contrainte pour le moment

    # 6.  Respecter les heures maximales a travailler par jour (Temps Plein = 8h/jour, Temps partiel = 6h/jour)
    for i in range(len(Int)):
        temps_travaille = {1:0, 2:0, 3:0, 4:0, 5:0}
        for j in range(len(Mis)):
            if solution[i][j] == 1:
                temps_travaille[Mis[j][1]] += Mis[j][3] - Mis[j][2]
        
        for x in temps_travaille:
            if (temps_travaille[x] > 480 and Int[i][3] == 35) or (temps_travaille[x] > 360 and Int[i][3] == 24):
                return False

    # 7.  Respecter la limite des heures supplementaires autorisees a travailler par les intervenants sur le plan de planification (heures supplementaires = 10h/semaine, 2h/jour)
    # a modifier si on integre le délire de travail a mis temps / plein temps
    for i in range(len(Int)):
        temps_travaille = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for j in range(len(Mis)):
            if solution[i][j] == 1:
                temps_travaille[Mis[j][1]] += Mis[j][3] - Mis[j][2]
        for k in temps_travaille:
            if temps_travaille[k] > 600:
                return False

    # 8.  Respecter l’amplitude de la journee de travail de chaque intervenant (amplitude = 12h)
    for i in range(len(Int)):
        temps_travaille = {1: [2000, 0], 2: [2000, 0], 3: [2000, 0], 4: [2000, 0], 5: [2000, 0]}
        for j in range(len(Mis)):
            if solution[i][j] == 1:
                if Mis[j][2] < temps_travaille[Mis[j][1]][0]:
                    temps_travaille[Mis[j][1]][0] = Mis[j][2]
                if Mis[j][3] > temps_travaille[Mis[j][1]][1]:
                    temps_travaille[Mis[j][1]][1] = Mis[j][3]
        for k in temps_travaille:
            if temps_travaille[k][1] - temps_travaille[k][0] > 720:
                return False


    # print("8 passé")
    # 9.  Un intervenant doit avoir assez de temps pour se deplacer d’une mission a une autre.
    soluce = activites_intervenants(solution, Int, Mis)
    vitesse_deplacement = 833  # exprimée en m/minutes

    for edt in soluce:
        for jour in edt:
            temps_parcouru = -1
            if len(edt[jour]) == 2:
                depart = edt[jour][0] + 1
                arrivee = edt[jour][1] + 1
                temps_parcouru = Dis[depart][arrivee] / vitesse_deplacement
                if temps_parcouru > Mis[edt[jour][1]][2] - Mis[edt[jour][0]][3]:
                    return False

            elif len(edt[jour]) > 2:
                for i in range(len(edt[jour]) - 1):
                    depart = edt[jour][i] + 1
                    arrivee = edt[jour][i + 1] + 1
                    temps_parcouru = Dis[depart][arrivee] / vitesse_deplacement
                    if temps_parcouru > Mis[edt[jour][i + 1]][2] - Mis[edt[jour][i]][3]:
                        return False

    # print("9 passé")

    return True





def activites_intervenants(solution, Int, Mis):
    """
    Renvoie les id des missions effectues par chaque intervenant, rangés dans l'ordre horaire
    """
    miss_intervenants = []
    for i in range(len(Int)):
        missions = {1: [], 2: [], 3: [], 4: [], 5: []}
        edt = {1: [], 2: [], 3: [], 4: [], 5: []}
        for j in range(len(Mis)):
            if solution[i][j] == 1:
                missions[Mis[j][1]].append((j, Mis[j][2]))

        for jour in missions:
            temp = sorted(missions[jour], key=lambda x: x[1])
            edt[jour] = [i[0] for i in temp]

        miss_intervenants.append(edt)

    return miss_intervenants

