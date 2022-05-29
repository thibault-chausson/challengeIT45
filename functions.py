import random

MATRICE_DISTANCE = []
INTERVENANTS = []
MISSIONS = []

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
    
    # fonctionne jusqu'ici.

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

    print("7 passé")
    # 8.  Respecter l’amplitude de la journee de travail de chaque intervenant (amplitude = 12h)
    for i in range(len(INTERVENANTS)):
        missions = [y for y in range(len(MISSIONS)) if solution[i][y] == 1]
        debut = [MISSIONS[y][2] for y in missions]
        fin = [MISSIONS[y][3] for y in missions]
        if max(fin) - min(debut) > 720:
            return False
    with open("res.txt", "a") as fichier:
        fichier.write(f"8:\n{str(solution)}\n\n")
    
    print("8 passé")
    # 9.  Un intervenant doit avoir assez de temps pour se deplacer d’une mission a une autre.
    # a voir car il nous faut une vitesse de déplacement.

    return True


def cree_solution_initiale():
    """
    Cree une solution initiale aléatoirement
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



def intervenant_libre(missions, mission):
    """
    Renvoies True si l'intervenant est libre pour la mission, False sinon
    vérifies actuellement les contraintes 1, 2, 3, 4, 7, 8 (9 a faire plus tard)
    """
    for i in range(len(missions)):
        if missions[i] == 1:
            last_i = i
            date_fin = MISSIONS[i][3]
    
    # LIGNE IMPORTANTE POUR LA CONTRAINTE 9, ON PEUT FAIRE date_fin + temps_deplacement
    if MISSIONS[mission][2] <= date_fin and MISSIONS[mission][1] == MISSIONS[last_i][1]:
        return False
    return True


def nouvelle_solution():
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
    
    return solution



def main():
    alors = int(input("Choisissez parmis les options suivantes :\n1: 45-4\n2: 96-6\n3: 100-10\nchoix: "))

    if alors == 1:
        charge_fichier_csv("45-4")
    elif alors == 2:
        charge_fichier_csv("96-6")
    elif alors == 3:
        charge_fichier_csv("100-10")
    else:
        print("Erreur de saisie, fin du programme.")
        return

    sol = nouvelle_solution()
    contraintes(sol)
    print("\nSolution:")
    for i in sol:
        print(i)
    
if __name__ == "__main__":
    main()

# idées: faire les croisements uniquement entre intervenants de la meme compétence.
