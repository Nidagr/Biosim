# -*- encoding: utf-8 -*-
__author__ = "Nida Grønbekk and Yuliia Dzihora"
__email__ = 'nida.gronbekk@nmbu.no and yuliia.dzihora@nmbu.no'

from biosim.simulation import BioSim
import textwrap

"""
Example where predators that were introduced in the simulation was way stronger: introduced with 
higher parameters and therefore higher fitness as well as they have lower death rate, and high
killing rate. They also thy to eat a lot (200 compare to the 50 as a default. Also, herbivores
have a bit higher death rate.

This was done to simulate how one specie dominates over another with consequential decline of 
own specie, due to the absence of food. 
"""

if __name__ == '__main__':

    geogr = """\
               WWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWHWWWWLLLLLLLW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHHHHHWWLLLLLLWWW
               WHHHHHLLLLLLLLLLLLWWW
               WHHHHHLLLDDLLLHLLLWWW
               WHHLLLLLDDDLLLHHHHWWW
               WWHHHHLLLDDLLLHWWWWWW
               WHHHLLLLLDDLLLLLLLWWW
               WHHHHLLLLDDLLLLWWWWWW
               WWHHHHLLLLLLLLWWWWWWW
               WWWHHHHLLLLLLLWWWWWWW
               WWWWWWWWWWWWWWWWWWWWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (10, 10),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(500)]}]
    ini_carns = [{'loc': (10, 10),
                  'pop': [{'species': 'Carnivore',
                           'age': 15,
                           'weight': 20}
                          for _ in range(200)]}]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs,
                 seed=123456, total_years=100, ymax_animals=10000)

    sim.set_animal_parameters('Herbivore', {'zeta': 3.2, 'xi': 1.8,
                                            'omega': 0.4})
    sim.set_animal_parameters('Carnivore', {'a_half': 70, 'phi_age': 0.5,
                                            'mu': 1, 'F': 200,
                                            'omega': 0.1, 'gamma': 10,
                                            'DeltaPhiMax': 9.})
    sim.set_landscape_parameters('L', {'f_max': 1000})
    sim.set_landscape_parameters('H', {'f_max': 500})

    sim.simulate(num_years=30, vis_years=1)
    sim.add_population(population=ini_carns)
    sim.simulate(num_years=70, vis_years=1)