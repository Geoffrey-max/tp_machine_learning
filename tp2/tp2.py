import random as rd
import networkx as nx
import matplotlib.pyplot as plt
import time
import numpy as np

from numpy.random import choice

NB_NODE_MAX = 10000
CENTRALISATION_MAX = (NB_NODE_MAX/2)
NB_LONG_MAX = 100
NB_ESSAIS = 100
NB_FOURMI = 2500

# randomisation du point de départ
point_depart = rd.randrange(0, CENTRALISATION_MAX)
# randomisation du point d'arrivée 
point_arrivee = rd.randrange(0, CENTRALISATION_MAX)
# il ne faut pas que le point d'arrivée soit égale au point de départ alors on le randomise tant que point de départ est égale à point d'arrivee
while point_depart == point_arrivee:
    point_arrivee = rd.randrange(0, CENTRALISATION_MAX)
# création du graphique
G = nx.Graph()


# Choisis le point suivant en prenant en paramètre le point en cours et la liste des points que l'on a parcourus (l'historique)
def choisir_Point_Suivant(point_en_cours, point_parcourus):
    total_longueurs = G.degree(point_en_cours, weight='longueur')
    total_pheromones = G.degree(point_en_cours, weight='pheromone')
    probList = []
    points_possibles = []
    if total_longueurs == 0 or total_pheromones == 0:
        return -1
    for point1, point2, data in G.edges(point_en_cours, data=True):
        if point_parcourus.count(point2) <= 0:
            note = (((1-(data['longueur']/total_longueurs)) * 0.1) + (data['pheromone']/total_pheromones * 0.9))
            probList.append(note)
            points_possibles.append(point2)
    if len(points_possibles) == 0:
        return -1
    probList = np.array(probList)
    probList /= probList.sum()
    point = choice(points_possibles, size=1, p=probList)[0]
    return point


# Dépose les phéromones sur les longueurs entre les points parcourus par la fourmi
def depotPheromone(points_parcourus):
    taille_graph = G.size(weight='longueur')
    distance = 0
    iterpoints = iter(points_parcourus)
    precedent_point = next(iterpoints)
    for n in iterpoints:
        distance += G[precedent_point][n]['longueur']
        precedent_point = n
    nb_a_poser = taille_graph/distance
    iterpoints = iter(points_parcourus)
    precedent_point = next(iterpoints)
    for n in iterpoints:
        G[precedent_point][n]['pheromone'] += round(nb_a_poser)
        precedent_point = n


# évaporation des phéromones présentes sur les chemins avec un taux de 0,03% 
def evaporationPheromone():
    for point1, point2 in G.edges:
        G[point1][point2]['pheromone'] = round(G[point1][point2]['pheromone']*0.03)


# calcul du parcours le plus cours et retourne le chemin qui est considéré comme le plus optimal
def calcul_parcours_le_plus_court():
    chemin = [point_arrivee]
    point = point_arrivee
    nb_essai = 0
    while point != point_depart:
        maximum = 0
        nb_essai += 1
        if nb_essai > NB_ESSAIS:
            print('Le chemin n a pas été trouvé !')
            print(chemin)
            return None
        for point1, point2, data in G.edges(point, data=True):
            if data['pheromone'] > maximum and point2 not in chemin:
                maximum = data['pheromone']
                point = point2
        chemin.append(point)
    print(f'parcours le plus court en {nb_essai} coups :')
    print(chemin)


# algorithme ACO
def init():
    for x in range(NB_NODE_MAX):
        G.add_edge(rd.randrange(0, CENTRALISATION_MAX), rd.randrange(0, CENTRALISATION_MAX), longueur=rd.randrange(0, NB_LONG_MAX), pheromone=1)
    nx.draw(G, with_labels=True, font_weight='bold')
    start_time = time.time()
    print(f'point de départ : {point_depart}')
    print(f'point d arrivee : {point_arrivee}')
    for i in range(NB_ESSAIS):
        for j in range(NB_FOURMI):
            point_en_cours = point_depart
            point_parcourus = [point_depart]
            while point_en_cours != point_arrivee:
                point_en_cours = choisir_Point_Suivant(point_en_cours, point_parcourus)
                if point_en_cours == -1:
                    break
                point_parcourus.append(point_en_cours)
            if point_en_cours == point_arrivee:
                depotPheromone(point_parcourus)
        evaporationPheromone()
    calcul_parcours_le_plus_court()
    print(f"l'algorithme s'est fini en {(time.time() - start_time)} secondes !")
    plt.show()


if __name__ == "__main__":
    init()
    