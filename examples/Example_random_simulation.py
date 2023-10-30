# -*- encoding: utf-8 -*-
__author__ = "Nida Grønbekk and Yuliia Dzihora"
__email__ = 'nida.gronbekk@nmbu.no and yuliia.dzihora@nmbu.no'

from biosim.simulation import BioSim
import numpy as np
import random

"""
Example of the randomly generated island with randomly distributed animals, that
have random properties (age, weight), where a random quantity of animals is placed with 
maximum of 5 animals per cell is generated.

Note that because animals are randomly placed, sometimes they get placed in water and valueError is 
raised. 
"""

if __name__ == '__main__':

    rows = 20
    columns = 20
    random.seed(123)
    def random_map_gen(rows, columns, option='2'):
        if option == '1':
            ecosystems = ['W', 'H', 'L', 'D']
        elif option == '2':
            ecosystems = ['H', 'L', 'D']

        top_bottom_arr = 'W' * columns + '\n'
        arrays = ''
        for i in range(rows - 2):
            array = 'W' + ''.join(
                (random.choice(ecosystems) for x in range(columns - 2))) + 'W' + '\n'
            arrays += array
        arrays = top_bottom_arr + arrays + top_bottom_arr
        return arrays

    geogr = random_map_gen(rows, columns)

    def add_spes_to_map(geogr, rows, columns, specie, start_loc=None):
        n = 1
        m = 1
        lits = []
        for l in geogr:
            if l == 'W':
                lits.append((n, m))
            m += 1
            if m - 1 == columns:
                n += 1
                m = 0

        number = np.random.randint(5, size=(rows, columns))
        if start_loc is not None:
            (s, p) = start_loc
        for i in range(1, rows + 1):
            for j in range(1, columns + 1):
                if (i, j) == start_loc:
                    continue
                elif (i, j) in lits:
                    continue

                if specie == 'Herbivore':
                    ini_anim = [{'loc': (i, j),
                                 'pop': rand_pop('Herbivore', number[i - 1, j - 1])}]
                elif specie == 'Carnivore':
                    ini_anim = [{'loc': (i, j),
                                 'pop': rand_pop('Carnivore', number[i - 1, j - 1])}]

                sim.add_population(population=ini_anim)

    def rand_pop(species, number):
        population = []
        bdict = {}
        age = np.random.randint(5, high=40, size=number)
        weight = 0.1 + np.random.sample(number) * 40
        for i in range(number):
            bdict["dct{0}".format(i)] = {}
            bdict["dct{0}".format(i)]['species'] = species
            bdict["dct{0}".format(i)]['age'] = age[i]
            bdict["dct{0}".format(i)]['weight'] = weight[i]
            population.append(bdict["dct{0}".format(i)])

        return population

    ini_herbs = [{'loc': (10, 10),
                  'pop': rand_pop('Herbivore', 150)}]
    ini_carns = [{'loc': (10, 10),
                  'pop': rand_pop('Carnivore', 150)}]


    
    sim = BioSim(island_map=geogr, ini_pop=ini_herbs,
                 seed=123456, ymax_animals=25000, img_base='image'
                 # hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                 #             'age': {'max': 60.0, 'delta': 2},
                 #             'weight': {'max': 60, 'delta': 2}},
                 )

    sim.set_animal_parameters('Herbivore', {'zeta': 3.2, 'xi': 1.8})
    sim.set_animal_parameters('Carnivore', {'a_half': 70, 'phi_age': 0.5,
                                            'omega': 0.3, 'F': 65,
                                            'DeltaPhiMax': 9.})
    sim.set_landscape_parameters('L', {'f_max': 700})
    add_spes_to_map(geogr, rows, columns, specie='Herbivore', start_loc=(10, 10))
    sim.simulate(num_years=50, vis_years=1, img_years=1)
    # sim.add_population(population=ini_carns)
    add_spes_to_map(geogr, rows, columns, specie='Carnivore')
    sim.simulate(num_years=200, vis_years=1, img_years=1)
    sim.make_movie()