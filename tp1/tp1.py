import math
import numpy as np
import random as rd
import matplotlib.pyplot as plt

from statistics import mean

CONST_GRAVITE_TERRE = 9.81
CONST_GRAVITE_LUNE = 1.62
CONST_GRAVITE_JUPITER = 24.80
NB_POPULATION_GENERE = 50
PROB_MUTATION = 0.1
DISTANCE_VOULU = 200

class Scorpion:
    def __init__(self, longueur_bras, base_bras, hauteur_bras, longueur_corde, module_young, poisson_ratio, angle, gravite, masse_volumique, base_fleche, hauteur_fleche, longueur_fleche):
        self._longueur_bras = longueur_bras
        self._base_bras = base_bras
        self._hauteur_bras = hauteur_bras
        self._longueur_corde = longueur_corde
        self._module_young = module_young
        self._poisson_ratio = poisson_ratio
        self._angle = angle
        self._gravite = gravite
        self._masse_volumique = masse_volumique
        self._longueur_fleche = longueur_fleche
        self._base_fleche = base_fleche
        self._hauteur_fleche = hauteur_fleche
        self._fitness = self.set_fitness()
        
    
    # Ressort K (en N/m)
    def const_ressort(self):
        young_modules = self._module_young
        poisson_ratio = self._poisson_ratio 
        if poisson_ratio != 0.5:
            k = (1 / 3) * young_modules / (1 - 2 * poisson_ratio)
            return k
        return -1

    
    # Longueur à vide (en m) Lv
    def longueur_vide(self):
        lb = self._longueur_bras
        lc = self._longueur_corde
        lv = (1 / 2) * (lb ** 2 - lc ** 2) ** (1/2)
        return lv


    # Longueur du déplacement (en m) Ld
    def longueur_deplacement(self):
        lf = self._longueur_fleche
        lv = self.longueur_vide()
        ld = lf - lv
        return ld


    # Masse du projectile (en kg)
    def masse_projectile(self):
        return self._masse_volumique * self._base_fleche * self._hauteur_fleche * self._longueur_fleche


    # Velocite (en m.s^-1) V
    def velocite(self):
        k = self.const_ressort()
        dist = self.longueur_deplacement()
        masse = self.masse_projectile()
        if masse > 0:         
            v = (k * dist ** 2 / masse) ** (1/2)
            return v
        return -1


    # Portée P (en m)
    def portee_scorpion(self):
        g = self._gravite
        velocite = self.velocite()
        angle = self._angle
        if g != 0 and 0 <= angle <= 90:
            radian_angle = math.radians(angle)
            p = (velocite ** 2 / g) * math.sin(2 * radian_angle)
            return p
        return -1

    
    # Energie d'impact (en joules), assimilée à la force cinétique transformée à l'impact Ec
    def energie_cinetique(self):
        masse = self.masse_projectile()
        velocite = self.velocite()
        ec = (1 / 2) * masse * velocite ** 2
        return ec


    # Equivalence Joule et gramme de TNT
    def energie_joule(self, ec):
        energie_tnt = ec / 4184
        return energie_tnt


    # Moment quadratique du bras I (en m^4)
    def moment_quadratique(self):
        b = self._base_bras
        h = self._hauteur_bras
        i = (b * h ** 3)/12
        return i

    
    # Force de traction F (en N)
    def force_traction(self):
        k = self.const_ressort()
        ld = self.longueur_deplacement()
        f = k * ld
        return f


    # Flèche du bras f max
    def fleche_bras_fmax(self):
        f = self.force_traction
        lb = self._longueur_bras
        e = self._module_young
        i = self.moment_quadratique()
        if ((48 * e * i) != 0):
            fmax = (f * lb ** 3) / (48 * e * i)
            return fmax
        return -1
    

    # Fonction est_tirable (pour savoir si il est possible de tirer) -> renvoie vrai ou faux
    def est_tirable(self):
        return self.longueur_vide() < self._longueur_fleche and self._longueur_corde < self._longueur_bras and self.longueur_deplacement() < self.fleche_bras_fmax()


    # assignation de la fitness pour le scorpion (plus la valeur est grande plus on s'approche du but)
    def set_fitness(self):
        return (100/((DISTANCE_VOULU - self.longueur_deplacement())+1)) * 100
      

class Materiau:
    def __init__(self, nom, masse, module_young, poisson_ratio):
        self._nom = nom
        self._masse = masse
        self._module_young = module_young
        self._poisson_ratio = poisson_ratio



# ------------------------------------------------------------------------------------------
MATERIAUX_POSSIBLE = [
    Materiau('acier', 7850, 210, 0.27),
    Materiau('aluminum', 2700, 62, 0.29),
    Materiau('argent', 10500, 78, 0),
    Materiau('bois', 800, 12, 0),
    Materiau('bamboo', 0, 20, 0),
    Materiau('bronze', 8740, 110, 0),
    Materiau('diamant', 3517, 1220, 0),
    Materiau('fer', 7860, 208, 0.25),
    Materiau('or', 18900, 78, 0.42),
    Materiau('platine', 21450, 170, 0),
    Materiau('titane', 4500, 114, 0.34)
]

# tableaux contenant la population créée par la génération de population
populations = []


# génération de la population de scorpion avec des nombres aléatoires
def generate_population():
    print("Population en génération ...")
    for i in range(NB_POPULATION_GENERE):
        materiau = rd.choice(MATERIAUX_POSSIBLE)
        print(materiau)
        populations.append(
            Scorpion(rd.randrange(0, 100, 1), rd.randrange(0, 100, 1), rd.randrange(0, 100, 1), rd.randrange(0, 100, 1), materiau._module_young, materiau._poisson_ratio, rd.randrange(0, 90, 1), CONST_GRAVITE_TERRE, materiau._masse, rd.randrange(0, 100, 1), rd.randrange(0, 100, 1), rd.randrange(0, 100, 1))
            )
    print("La population vient d'être générer !")



# On utilise la fitness pour pouvoir les trier et ensuite on tire au sort n/2 couples 
def selection():
    populations.sort(key=lambda x: x._fitness, reverse=True)
    return populations[: round(NB_POPULATION_GENERE/2)]
    # for x in range(round(NB_POPULATION_GENERE / 2), NB_POPULATION_GENERE - 1):
    #     del populations[round(NB_POPULATION_GENERE / 2)]


# On implémente le croisement simple entre deux scorpions pour pouvoir l'utiliser dans la prochaine fonction croisements
def croisement(scorpion1, scorpion2):
    return Scorpion(scorpion1._longueur_bras, scorpion2._base_bras, scorpion2._hauteur_bras, scorpion1._longueur_corde, scorpion1._module_young, scorpion1._poisson_ratio, scorpion1._angle, scorpion1._gravite, scorpion1._masse_volumique, scorpion2._base_fleche, scorpion2._hauteur_fleche, scorpion2._longueur_fleche)



def croisements():
    notes = [i._fitness for i in populations]
    notes /= np.sum(notes)
    populations_croise = []
    for scorpion in populations:
        scorpion2 = np.random.choice(populations, p=notes)
        scorpion_enfant = croisement(scorpion, scorpion2)
        populations_croise.append(scorpion_enfant)
        scorpion_enfant2 = croisement(scorpion2, scorpion)
        populations_croise.append(scorpion_enfant2)
    return populations_croise


def mutations():
    for i in range(0, len(populations)-1):
        if(rd.random() <= 0.5):
            populations[i]._longueur_corde = populations[i]._longueur_corde + populations[i]._longueur_corde * PROB_MUTATION
            populations[i]._longueur_bras = populations[i]._longueur_bras + populations[i]._longueur_bras * PROB_MUTATION
            populations[i]._angle = populations[i]._angle + populations[i]._angle * PROB_MUTATION
            populations[i]._base_fleche = populations[i]._base_fleche + populations[i]._base_fleche * PROB_MUTATION
            populations[i]._hauteur_fleche = populations[i]._hauteur_fleche + populations[i]._hauteur_fleche * PROB_MUTATION
            populations[i]._longueur_fleche = populations[i]._longueur_fleche + populations[i]._longueur_fleche * PROB_MUTATION
        else:
            populations[i]._longueur_corde = populations[i]._longueur_corde - populations[i]._longueur_corde * PROB_MUTATION
            populations[i]._longueur_bras = populations[i]._longueur_bras - populations[i]._longueur_bras * PROB_MUTATION
            populations[i]._angle = populations[i]._angle - populations[i]._angle * PROB_MUTATION
            populations[i]._base_fleche = populations[i]._base_fleche - populations[i]._base_fleche * PROB_MUTATION
            populations[i]._hauteur_fleche = populations[i]._hauteur_fleche - populations[i]._hauteur_fleche * PROB_MUTATION
            populations[i]._longueur_fleche = populations[i]._longueur_fleche - populations[i]._longueur_fleche * PROB_MUTATION


def init():
    generate_population()
    reussi = None
    i = 0
    while not reussi or i < NB_POPULATION_GENERE :
        populations = selection()
        populations = croisements()
        mutations()
        print(len(populations))

        



if __name__ == "__main__":
    init()