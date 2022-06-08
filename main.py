import sys
import population_initiale
import genetique
import fitnessSESSAD
import fitnessEmployes

from functions import *

def main():
    if len(sys.argv) != 6:
        print("")
        print("Utilisation: python main.py <nbGeneration> <probaMutation> <nbPopInitiale> <probaMissionEmpire> <dossier>")
        print("<nbGeneration>: nombre de générations à faire dans l'algorithme génétique") 
        print("<probaMutation>: probabilité qu'un individu soit muté; prend une valeur entre 0 et 1")
        print("<nbPopInitiale>: nombre d'individus dans la population initiale; min=50, max=250")
        print("<probaMissionEmpire>: probabilite qu'un individu soit conservé après une mutation, même s'il empire la fitness; prend une valeur entre 0 et 1")
        print("<dossier>: dossier contenant les fichiers de donnees; ex: 45-4")
        print("")
        sys.exit(1)
    
    nbGeneration = int(sys.argv[1])
    probaMutation = float(sys.argv[2])
    nbPopInitiale = int(sys.argv[3])
    probaMissionEmpire = float(sys.argv[4])
    dossier = sys.argv[5]

    MATRICE_DISTANCE, INTERVENANTS, MISSIONS = charge_fichier_csv(dossier)

    print("Génération de la population initiale...")
    pop_initiale = population_initiale.gen_n_solutions_uniques(nbPopInitiale, MATRICE_DISTANCE, INTERVENANTS, MISSIONS)
    pop_resultante = genetique.genetiqueCascade(pop_initiale, nbGeneration, probaMutation, MATRICE_DISTANCE, INTERVENANTS, MISSIONS, probaMissionEmpire)

    best_solution, best_fitness = pick_best(pop_resultante, MATRICE_DISTANCE, INTERVENANTS, MISSIONS)

    print("\nRésultat final:")
    print("Fitness SESSAD:", str(best_fitness))
    for i in best_solution:
        print(i)
    

def pick_best(pop_resultante, MATRICE_DISTANCE, INTERVENANTS, MISSIONS):
    distance = fitnessEmployes.distance_employe(activites_intervenants(pop_resultante[0], MATRICE_DISTANCE, INTERVENANTS, MISSIONS), MATRICE_DISTANCE, INTERVENANTS, MISSIONS)
    best_fitness = fitnessSESSAD.fitnessSESSAD(MISSIONS, INTERVENANTS, pop_resultante[0], distance, MATRICE_DISTANCE)
    best_solution = pop_resultante[0]
    for individu in pop_resultante:
        distance = fitnessEmployes.distance_employe(activites_intervenants(individu, MATRICE_DISTANCE, INTERVENANTS, MISSIONS), MATRICE_DISTANCE, INTERVENANTS, MISSIONS)
        fitness = fitnessSESSAD.fitnessSESSAD(MISSIONS, INTERVENANTS, individu, distance, MATRICE_DISTANCE)
        if fitness < best_fitness:
            best_fitness = fitness
            best_solution = individu
    
    return best_solution, best_fitness

if __name__ == "__main__":
    main()