# -*- encoding: utf-8 -*-
__author__ = "Nida Grønbekk and Yuliia Dzihora"
__email__ = 'nida.gronbekk@nmbu.no and yuliia.dzihora@nmbu.no'

from biosim.simulation import BioSim
from biosim.fauna import Carnivore, Herbivore
from biosim.landscape import Lowland, Highland, Desert, Water
import pytest


"""
In this file we will test functions from the BioSim class. Note that
for us to actually test the functions, we need to make an instance of the BioSim class, 
hence a multiline-string, an initial list of animals and a call to BioSim with this string,
list of animals and a seed is necessary.
"""


class TestAddPopulation:
    """
    This class contains tests for the add_population() function in class BioSim.
    """

    def test_add_population(self):
        """
        Test that animals actually gets added to the island when calling add_population().
        Make sure they were added by checking that the length of the lists of carnivores
        and list of herbivores are as expected. And check that the type of the animals
        in these lists are correct (Herbivore or Carnivore).
        """
        string = """\
                                                                WWWW
                                                                WLDW
                                                                WLHW
                                                                WWWW"""
        ini_herbs = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20},
                      {'species': 'Herbivore', 'age': 6, 'weight': 25}]}]
        sim = BioSim(string, ini_pop=ini_herbs, seed=1234)
        ini_carns = [{'loc': (2, 3), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20},
                     {'species': 'Carnivore', 'age': 6, 'weight': 25}]}]
        sim.add_population(ini_carns)
        assert len(sim.object_map[1, 1].herbivores) == 2 and \
               len(sim.object_map[1, 2].carnivores) == 2

        for animal in sim.object_map[1, 1].herbivores:
            assert type(animal) == Herbivore
        for animal in sim.object_map[1, 2].carnivores:
            assert type(animal) == Carnivore


    def test_add_population_correct_age_and_weight(self):
        """
        When adding animals to a cell we give the age and weight as arguments (or give none).
        Add carnivores and herbivores to the map and check if their age and weight are as expected.
        """
        string = """\
                                                                        WWWW
                                                                        WLDW
                                                                        WLHW
                                                                        WWWW"""
        ini_herbs = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}]
        sim = BioSim(string, ini_pop=ini_herbs, seed=1234)
        ini_carns = [{'loc': (2, 3), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}]}]
        sim.add_population(ini_carns)
        herb = sim.object_map[1, 1].herbivores[0]
        carn = sim.object_map[1, 2].carnivores[0]
        assert herb.get_age() == 5 and herb.get_weight() == 20
        assert carn.get_age() == 5 and carn.get_weight() == 20


    def test_add_population_water(self):
        """
        Test that when trying to add animals to a water cell a ValueError is raised.
        """
        string = """\
                                                                        WWWW
                                                                        WLDW
                                                                        WLHW
                                                                        WWWW"""
        ini_herbs = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20},
                      {'species': 'Herbivore', 'age': 6, 'weight': 25}]}]
        sim = BioSim(string, ini_pop=ini_herbs, seed=1234)
        ini_carns = [{'loc': (2, 1), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}]},
                     {'loc': (1, 2), 'pop': [{'species': 'Carnivore', 'age': 6, 'weight': 25}]}]
        with pytest.raises(ValueError):
            sim.add_population(ini_carns)

    def test_add_population_col_out_of_bounds(self):
        """
        Test that when trying to add animals to a location with column value not in our map, a
        ValueError is raised.
        """
        string = """\
                                                                                WWWW
                                                                                WLDW
                                                                                WLHW
                                                                                WWWW"""
        ini_herbs = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20},
                     {'species': 'Herbivore', 'age': 6, 'weight': 25}]}]
        sim = BioSim(string, ini_pop=ini_herbs, seed=1234)
        ini_carns = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}]},
                     {'loc': (1, 5), 'pop': [{'species': 'Carnivore', 'age': 6, 'weight': 25}]}]
        with pytest.raises(ValueError):
            sim.add_population(ini_carns)

    def test_add_population_row_out_of_bounds(self):
        """
        Test that when trying to add animals to a location with row value not in our map, a
        ValueError is raised.
        """
        string = """\
                                                                                WWWW
                                                                                WLDW
                                                                                WLHW
                                                                                WWWW"""
        ini_herbs = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20},
                      {'species': 'Herbivore', 'age': 6, 'weight': 25}]}]
        sim = BioSim(string, ini_pop=ini_herbs, seed=1234)
        ini_carns = [{'loc': (5, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20},
                     {'species': 'Carnivore', 'age': 6, 'weight': 25}]}]
        with pytest.raises(ValueError):
            sim.add_population(ini_carns)

    def test_add_population_illegal_age(self):
        """
        Test that if we try to add an animal with an age less than 0 then our function
        add_population raises a ValueError.
        """
        string = """\
                                                                                       WWWW
                                                                                       WLDW
                                                                                       WLHW
                                                                                       WWWW"""
        ini_herbs = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20},
                     {'species': 'Herbivore', 'age': 6, 'weight': 25}]}]
        sim = BioSim(string, ini_pop=ini_herbs, seed=1234)
        ini_carns = [{'loc': (2, 3), 'pop': [{'species': 'Carnivore', 'age': -5, 'weight': 20},
                      {'species': 'Carnivore', 'age': -6, 'weight': 25}]}]
        with pytest.raises(ValueError):
            sim.add_population(ini_carns)

    def test_add_population_illegal_weight(self):
        """
        Test that if we try to add an animal with a weight less than or equal to 0 then our function
        add_population raises a ValueError.
        """
        string = """\
                                                                                       WWWW
                                                                                       WLDW
                                                                                       WLHW
                                                                                       WWWW"""
        ini_herbs = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20},
                     {'species': 'Herbivore', 'age': 6, 'weight': 25}]}]
        sim = BioSim(string, ini_pop=ini_herbs, seed=1234)
        ini_carns_zero = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 0}]}]

        ini_carns_neg = [{'loc': (2, 3), 'pop': [{'species': 'Carnivore', 'age': 6, 'weight': -2}]}]
        with pytest.raises(ValueError):
            sim.add_population(ini_carns_zero)
        with pytest.raises(ValueError):
            sim.add_population(ini_carns_neg)


@pytest.fixture(scope='function')
def set_params(request):
    """
    Fixture sets parameters on Herbivores, Carnivores, Lowland, Highland, Desert and Water.

    The fixture sets the classes parameters when called for setup, and resets them when called for
    teardown.
    This ensures that modified  parameters are always reset before leaving a test.

    Based on https://stackoverflow.com/a/33879151

    Parameters
    __________
    request
        Request object automatically provided by pytest.
        request.param is the parameter dictionary to be passed to
        *.set_params()

        Taken from lecture notes
    """
    Herbivore.set_params(request.param)
    Carnivore.set_params(request.param)
    Lowland.set_landscape_params(request.param)
    Highland.set_landscape_params(request.param)
    Desert.set_landscape_params(request.param)
    Water.set_landscape_params(request.param)

    yield

    Herbivore.set_params(Herbivore.default_params)
    Carnivore.set_params(Carnivore.default_params)
    Lowland.set_landscape_params(Lowland.default_params)
    Highland.set_landscape_params(Highland.default_params)
    Desert.set_landscape_params(Desert.default_params)
    Water.set_landscape_params(Water.default_params)


class TestSetAnimalParameters:
    """
    This class contains tests for the set_animal_parameters() function in BioSim.
    """

    @pytest.mark.parametrize('set_params', [{'w_half': 15}])
    def test_set_animal_parameters_herbivores(self, set_params):
        """
        Test if parameters of Herbivore class is changed when calling set_animal_parameters.
        We make an instance of class Herbivore. We send 'H' and {'w_half': 15} as input
        to set_animal_parameter() and then assert if the herbivore objects default_params['w_half']
        is equal to 15.

        The test takes set_params as input to make sure that after the test is executed the
        parameters are set back to original default_values.
        """
        string = """\
                                                                        WWWW
                                                                        WLDW
                                                                        WLHW
                                                                        WWWW"""
        ini_herbs = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}]
        sim = BioSim(string, ini_pop=ini_herbs, seed=1234)
        herb = sim.object_map[1, 1].herbivores[0]
        sim.set_animal_parameters('Herbivore', {'w_half': 15})
        assert herb.default_params['w_half'] == 15

    @pytest.mark.parametrize('set_params', [{'w_birth': 7}])
    def test_set_animal_parameters_carnivores(self, set_params):
        """
        Test if parameters of Carnivore class is changed when calling set_animal_parameters.
        We make an instance of class Carnivore. We send 'C' and {'w_birth': 7} as input
        to set_animal_parameter() and then assert if the carnivore objects default_params['w_birth']
        is equal to 7.

        The test takes set_params as input to make sure that after the test is executed the
        parameters are set back to original default_values.
        """
        string = """\
                                                                            WWWW
                                                                            WLDW
                                                                            WLHW
                                                                            WWWW"""
        ini_carns = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}]}]
        sim = BioSim(string, ini_pop=ini_carns, seed=1234)
        carn = sim.object_map[1, 1].carnivores[0]
        sim.set_animal_parameters('Carnivore', {'w_birth': 7})
        assert carn.default_params['w_birth'] == 7

    def test_set_animal_parameters_nonexistent_species(self):
        """
        Test that set_animal_parameters() raises ValueError when a non-existent species is sent as
        input. We sen 'Sheep' as argument, which is a nonexistent species.
        """
        string = """\
                                                                                    WWWW
                                                                                    WLDW
                                                                                    WLHW
                                                                                    WWWW"""
        ini_carns = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}]}]
        sim = BioSim(string, ini_pop=ini_carns, seed=1234)
        with pytest.raises(ValueError):
            sim.set_animal_parameters('Sheep', {'wool': 7})


class TestLandscapeParameters:
    """
    In this class we test the BioSim function set_landscape_parameters().
    """

    @pytest.mark.parametrize('set_params', [{'f_max': 100}])
    def test_set_landscape_parameters_highland(self, set_params):
        """
        We want to test if the parameter f_max of class Highland is changed to 100 when
        set_landscape_parameters() is called with input 'H' and {'f_max': 100}. Test this
        by checking the default_params['f_max'] of a cell in the map that is of type Highland.

        The test takes set_params as input to make sure that after the test is executed the
        parameters are set back to original default_values.
        """
        string = """\
                                                                                    WWWW
                                                                                    WLDW
                                                                                    WLHW
                                                                                    WWWW"""
        ini_carns = [{'loc': (3, 3), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}]}]
        sim = BioSim(string, ini_pop=ini_carns, seed=1234)
        sim.set_landscape_parameters('H', {'f_max': 100})
        assert sim.object_map[2, 2].default_params['f_max'] == 100

    @pytest.mark.parametrize('set_params', [{'f_max': 10}])
    def test_set_landscape_parameters_lowland(self, set_params):
        """
        We want to test if the parameter f_max of class Lowland is changed to 10 when
        set_landscape_parameters() is called with input 'L' and {'f_max': 10}. Test this
        by checking the default_params['f_max'] of a cell in the map that is of type Lowland.

        The test takes set_params as input to make sure that after the test is executed the
        parameters are set back to original default_values.
        """
        string = """\
                                                                                    WWWW
                                                                                    WLDW
                                                                                    WLHW
                                                                                    WWWW"""
        ini_carns = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}]}]
        sim = BioSim(string, ini_pop=ini_carns, seed=1234)
        sim.set_landscape_parameters('L', {'f_max': 10})
        assert sim.object_map[1, 1].default_params['f_max'] == 10

    @pytest.mark.parametrize('set_params', [{'f_max': 1000}])
    def test_set_landscape_parameters_desert(self, set_params):
        """
        We want to test if the parameter f_max of class Desert is changed to 1000 when
        set_landscape_parameters() is called with input 'D' and {'f_max': 1000}. Test this
        by checking the default_params['f_max'] of a cell in the map that is of type Desert.

        The test takes set_params as input to make sure that after the test is executed the
        parameters are set back to original default_values.
        """

        string = """\
                                                                                        WWWW
                                                                                        WLDW
                                                                                        WLHW
                                                                                        WWWW"""
        ini_carns = [{'loc': (2, 3), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}]}]
        sim = BioSim(string, ini_pop=ini_carns, seed=1234)
        sim.set_landscape_parameters('D', {'f_max': 1000})
        assert sim.object_map[1, 2].default_params['f_max'] == 1000

    def test_set_landscape_parameters_nonexistent(self):
        """
        Test that if nonexistent type of landscape is sent as argument to set_landscape_types() a
        ValueError is raised. Here we send 'X' and {'f_max': 100} as input
        to set_landscape_parameters() which will raise a ValueError since 'X' is not defined.
        """
        string = """\
                                                                                        WWWW
                                                                                        WLDW
                                                                                        WLHW
                                                                                        WWWW"""
        ini_carns = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}]}]
        sim = BioSim(string, ini_pop=ini_carns, seed=1234)
        with pytest.raises(ValueError):
            sim.set_landscape_parameters('X', {'f_max': 100})


class TestMigration:

    def test_migrate_animals_in_map_legal_move_north(self, mocker):
        """
        Change animal parameter 'mu' to high value 10 to make sure the animal probability to move
        is 1. That way we ensure that fauna.migration() returns a direction, not None.
        Then use mocker to make that direction that is returned to be 'north'. Place a carnivore
        in a cell in the map where north cell is not water (legal to move), and then check that
        the length of lists of carnivores in the north cell is 1 after migration, and 0 in old cell.
        Also check that there is a carnivore type object in the new cell.

        """
        mocker.patch("random.choice", return_value=(1, 1))
        string = """\
                                WWWW
                                WLDW
                                WLHW
                                WWWW"""
        ini_carns = [{'loc': (3, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}]}]
        sim = BioSim(string, ini_carns, 1234)
        sim.set_animal_parameters('Carnivore', {'mu': 10})
        sim.migration_cycle()

        assert len(sim.object_map[2, 1].carnivores) == 0 and \
               len(sim.object_map[1, 1].carnivores) == 1
        assert type(sim.object_map[1, 1].carnivores[0]) == Carnivore

    def test_migrate_animals_in_map_illegal_move(self, mocker):
        """
        If animal chooses to move to a cell of type water, it should not move. Make the situation
        so that the animal would guaranteed move north had it not been water. The test passes if
        the animal stayed in the same position.
        """
        mocker.patch("random.choice", return_value=(0, 1))
        string = """\
                                        WWWW
                                        WLDW
                                        WLHW
                                        WWWW"""
        ini_carns = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}]}]
        sim = BioSim(string, ini_carns, 1234)
        sim.set_animal_parameters('Carnivore', {'mu': 10})
        sim.migration_cycle()
        assert len(sim.object_map[1, 1].carnivores) == 1 and \
               len(sim.object_map[0, 1].carnivores) == 0
        assert type(sim.object_map[1, 1].carnivores[0]) == Carnivore

    def test_migrate_animals_in_map_legal_move_east(self, mocker):
        """
        Change animal parameter 'mu' to high value 10 to make sure the animal probability to move
        is 1. That way we ensure that fauna.migration() returns a direction, not None.
        Then use mocker to make that direction that is returned to be 'east'. Place a carnivore
        in a cell in the map where east cell is not water (legal to move), and then check that
        the length of lists of carnivores in the east cell is 1 after migration, and 0 in old cell.
        Also check that there is a carnivore type object in the new cell.
        """
        mocker.patch("random.choice", return_value=(1, 2))
        string = """\
                                WWWW
                                WLDW
                                WLHW
                                WWWW"""
        ini_carns = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}]}]
        sim = BioSim(string, ini_carns, 1234)
        sim.set_animal_parameters('Carnivore', {'mu': 10})
        sim.migration_cycle()
        assert len(sim.object_map[1, 1].carnivores) == 0 and \
            len(sim.object_map[1, 2].carnivores) == 1
        assert type(sim.object_map[1, 2].carnivores[0]) == Carnivore

    def test_migrate_animals_in_map_legal_move_west(self, mocker):
        """
        Change animal parameter 'mu' to high value 10 to make sure the animal probability to move
        is 1. That way we ensure that fauna.migration() returns a direction, not None.
        Then use mocker to make that direction that is returned to be 'west'. Place a carnivore
        in a cell in the map where west cell is not water (legal to move), and then check that
        the length of lists of carnivores in the west cell is 1 after migration, and 0 in old cell.
        Also check that there is a carnivore type object in the new cell.
        """
        mocker.patch("random.choice", return_value=(1, 1))
        string = """\
                                WWWW
                                WLDW
                                WLHW
                                WWWW"""
        ini_carns = [{'loc': (2, 3), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}]}]
        sim = BioSim(string, ini_carns, 1234)
        sim.set_animal_parameters('Carnivore', {'mu': 10})
        sim.migration_cycle()
        assert len(sim.object_map[1, 2].carnivores) == 0 and \
            len(sim.object_map[1, 1].carnivores) == 1
        assert type(sim.object_map[1, 1].carnivores[0]) == Carnivore

    def test_migrate_animals_in_map_legal_move_south(self, mocker):
        """
        Change animal parameter 'mu' to high value 10 to make sure the animal probability to move
        is 1. That way we ensure that fauna.migration() returns a direction, not None.
        Then use mocker to make that direction that is returned to be 'south'. Place a carnivore
        in a cell in the map where south cell is not water (legal to move), and then check that
        the length of lists of carnivores in the south cell is 1 after migration, and 0 in old cell.
        Also check that there is a carnivore type object in the new cell.
        """
        mocker.patch("random.choice", return_value=(2, 1))
        string = """\
                                WWWW
                                WLDW
                                WLHW
                                WWWW"""
        ini_carns = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}]}]
        sim = BioSim(string, ini_carns, 1234)
        sim.set_animal_parameters('Carnivore', {'mu': 10})
        sim.migration_cycle()
        assert len(sim.object_map[1, 1].carnivores) == 0 and \
            len(sim.object_map[2, 1].carnivores) == 1
        assert type(sim.object_map[2, 1].carnivores[0]) == Carnivore

    def test_migrate_animals_in_map_twice(self, mocker):
        """
        When we are done moving all the animals in map once, try to move again next year. Should be
        possible. Test this by moving north twice.
        """
        mocker.patch("random.choice", return_value=(1, 1))
        string = """\
                                        WWWW
                                        WLDW
                                        WLHW
                                        WLLW
                                        WWWW"""
        ini_carns = [{'loc': (4, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}]}]
        sim = BioSim(string, ini_carns, 1234)
        sim.set_animal_parameters('Carnivore', {'mu': 10})
        sim.migration_cycle()  # move north
        sim.migration_cycle() # move north again
        assert len(sim.object_map[3, 1].carnivores) == 0 and\
               len(sim.object_map[1, 1].carnivores) == 1
        assert type(sim.object_map[1, 1].carnivores[0]) == Carnivore


def test_aging_cycle():
    """
    After calling the function aging_cycle() in BioSim, the age of all the animals in the cells
    should have increased by one year.
    """
    string = """\
                                            WWWW
                                            WLDW
                                            WWWW"""
    ini_carns = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20},
                                         {'species': 'Carnivore', 'age': 5, 'weight': 20}]}]
    sim = BioSim(string, ini_carns, 1234)
    ini_herbs = [{'loc': (2, 3), 'pop': [{'species': 'Herbivore', 'age': 6, 'weight': 10},
                                         {'species': 'Herbivore', 'age': 6, 'weight': 10}]}]
    sim.add_population(ini_herbs)
    sim.aging_cycle()
    for cell in sim.island.island_iterator():
        if len(cell.carnivores) > 0:
            for i in range(len(cell.carnivores)-1):
                assert cell.carnivores[i].get_age() == 6
        if len(cell.herbivores) > 0:
            for i in range(len(cell.herbivores)-1):
                assert cell.herbivores[i].get_age() == 7


def test_feeding_cycle_regrowth():
    """
    If no animals, the amount of available fodder in each cell should be f_max. Set to 0 first to
    see that regrowth actually happens when feeding cycle is called.
    """
    string = """\
                                                WWWW
                                                WLDW
                                                WWWW"""
    ini_carns = []
    sim = BioSim(string, ini_carns, 1234)
    for cell in sim.island.island_iterator():
        cell.available_fodder = 0
        assert cell.available_fodder == 0
    # Call feeding cycle()
    sim.feeding_cycle()
    for cell in sim.island.island_iterator():
        assert cell.available_fodder == cell.default_params['f_max']
