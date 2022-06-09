import sys
import population_initiale
import genetique
import fitnessSESSAD
import fitnessEmployes
import argparse

from functions import *


"""
demander fichier à utiliser
demander taille popu initiale
demander quel algorithme utiliser
génétique tout court, variable : nbGeneration, probaMutation, probaMissionEmpire, type_fit
genetique cascade, variable :  nbGeneration, probaMutation, probaMissionEmpire, nbTour
genetique pareto, variable :  nbGeneration, probaMutation,  probaMissionEmpire
genetique moyenne, variable :  nbGeneration, probaMutation,  probaMissionEmpire
genetique moyenne normalisée :  nbGeneration, probaMutation, probaMissionEmpire
"""


#TODO: faire un menu pour choisir l'algorithme
#TODO: faire une fonction pour enrgistrer le meilleur résultat et le planing dans un fichier



def main():
    parser = argparse.ArgumentParser(description='Projet IT45')
    parser.add_argument('-d', '--dossier', type=str, help='Dossier contenant les fichiers csv')
    parser.add_argument('-g', '--generations', type=int, help='Nombre de générations')
    parser.add_argument('-p', '--population', type=int, help='Nombre d\'individus dans la population')
    parser.add_argument('-m', '--mutation', type=float, help='Probabilité de mutation')
    parser.add_argument('-n', '--nbTour', type=int, help='Nombre d\'éxecutions de l\'algorithme génétique en cascade, 0 par défaut')
    parser.add_argument('-f', '--fitness', type=str, help='Type de fitness, argument nécessaire en cas de --type=classique')
    parser.add_argument('-e', '--empire', type=float, help='Probabilité de garder un individu, même s\'il réduit la fitness')
    parser.add_argument('-r', '--remplace', action='store_true', help='Choisir si l\'on remplace la moitiée de la population en cas de blocage ou non, par défaut à False')
    parser.add_argument('-t', '--type', type=str, help='Type d\'algorithme utilisé: classique / cascade / pareto / moyenne / moyenne_normalisee')
    
    args = parser.parse_args()

    nbGeneration = args.generations
    probaMutation = args.mutation
    nbPopInitiale = args.population 
    probaMissionEmpire = args.empire
    dossier = args.dossier
    remplace = args.remplace
    type_algo = args.type
    type_fit = args.fitness
    nbTour = 0 if args.nbTour is None else args.nbTour

    MATRICE_DISTANCE, INTERVENANTS, MISSIONS = charge_fichier_csv(dossier)

    print("Génération de la population initiale...")
    pop_initiale = population_initiale.gen_n_solutions_uniques(nbPopInitiale, INTERVENANTS, MISSIONS, MATRICE_DISTANCE)
    
    
    if type_algo == "classique":
        pop_resultante = genetique.genetique(pop_initiale, nbGeneration, probaMutation, MATRICE_DISTANCE, INTERVENANTS, MISSIONS, probaMissionEmpire, type_fit, remplace)
    elif type_algo == "cascade":
        pop_resultante = genetique.genetiqueCascade(pop_initiale, nbGeneration, probaMutation, MATRICE_DISTANCE, INTERVENANTS, MISSIONS, probaMissionEmpire, nbTour, remplace)
    elif type_algo == "pareto":
        pop_resultante = genetique.genetiquePareto(pop_initiale, nbGeneration, probaMutation, MATRICE_DISTANCE, INTERVENANTS, MISSIONS, probaMissionEmpire)
    elif type_algo == "moyenne":
        pop_resultante = genetique.genetiqueMoyenne(pop_initiale, nbGeneration, probaMutation, MATRICE_DISTANCE, INTERVENANTS, MISSIONS, probaMissionEmpire, remplace)
    elif type_algo == "normalisee":
        pop_resultante = genetique.genetiqueMoyenneNorma(pop_initiale, nbGeneration, probaMutation, MATRICE_DISTANCE, INTERVENANTS, MISSIONS, probaMissionEmpire, remplace)
    else:
        print("Erreur: type d'algorithme non reconnu")
        sys.exit(1)

    """
    print("\nRésultat final:")
    print("Fitness SESSAD:", str(best_fitness))
    for i in best_solution:
        print(i)
    """


if __name__ == "__main__":
    main()