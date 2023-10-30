# -*- encoding: utf-8 -*-
__author__ = "Nida Grønbekk and Yuliia Dzihora"
__email__ = 'nida.gronbekk@nmbu.no and yuliia.dzihora@nmbu.no'

from biosim.fauna import Herbivore, Carnivore
import pytest
from scipy.stats import chisquare


@pytest.fixture(scope='function')
def set_params(request):
    """
    Fixture sets parameters on Herbivores and Carnivores.

    The fixture sets Herbivores/ Carnivores parameters when called for setup, and resets them when
    called for teardown. This ensures that modified parameters are always reset before leaving a
    test.

    Based on https://stackoverflow.com/a/33879151

    Parameters
    __________
    request
        Request object automatically provided by pytest.
        request.param is the parameter dictionary to be passed to
        fauna.set_params()

        Taken from lecture notes
    """
    Herbivore.set_params(request.param)
    Carnivore.set_params(request.param)

    yield

    Herbivore.set_params(Herbivore.default_params)
    Carnivore.set_params(Carnivore.default_params)


class TestSetParams:
    """
    This class contains different tests for the set_params function of the Fauna class. We make sure
    that the expected errors are raised when an invalid key is given, or the value of the keys are
    given an invalid value.
    """

    def test_key_error(self):
        """
        A test that checks if set_params raises a KeyError when non-existent key names are given.
        Test passes when error is raised.
        """
        h = Herbivore()
        with pytest.raises(KeyError):
            h.set_params({'imaginary_value': 5})

        c = Carnivore()
        with pytest.raises(KeyError):
            c.set_params({'fantasy_value': 6})

    def test_value_error_eta(self):
        """
        The test checks that the expected ValueError is raised when parameter 'eta' is given and
        invalid value. Eta should be in the interval [0,1]. Test passes when error is raised.
        """
        h = Herbivore()
        with pytest.raises(ValueError):
            h.set_params({'eta': 1.5})
        with pytest.raises(ValueError):
            h.set_params({'eta': -1.5})

        c = Carnivore()
        with pytest.raises(ValueError):
            c.set_params({'eta': 1.5})
        with pytest.raises(ValueError):
            c.set_params({'eta': -1.5})

    def test_value_error_DeltaPhiMax(self):
        """
        This test checks if the expected ValueError is raised when parameter DeltaPhiMax is given an
        invalid value. DeltaPhiMax should be strictly positive (> 0). Test passes when error is
        raised.
        """
        h = Herbivore()
        with pytest.raises(ValueError):
            h.set_params({'DeltaPhiMax': 0})
        with pytest.raises(ValueError):
            h.set_params({'DeltaPhiMax': -0.3})

        c = Carnivore()
        with pytest.raises(ValueError):
            c.set_params({'DeltaPhiMax': 0})
        with pytest.raises(ValueError):
            c.set_params({'DeltaPhiMax': -0.3})


    def test_value_error_other_params(self):
        """
        This test checks if the expected ValueError is raised for the remaining parameters of the
        Fauna class. They have one condition in common, which is that all of them should be greater
        than or equal to zero (>= 0). Test passes when error is raised.
        """
        h = Herbivore()
        c = Carnivore()
        keys = ['w_birth', 'sigma_birth', 'beta', 'F', 'phi_age', 'a_half',
                'phi_weight', 'w_half', 'xi', 'zeta', 'gamma', 'omega']
        for key in keys:
            with pytest.raises(ValueError):
                h.set_params({key: -1})
            with pytest.raises(ValueError):
                c.set_params({key: -1})


class TestInit:
    """
    A class for testing that the constructor of the Herbivore and Carnivore classes do what they are
    supposed to do. When no arguments are given when creating a class, is age set to 0 and weight
    drawn from the normal distribution. When weight and age is given as input, is the age and weight
    of the animal the same as the input. When invalid values of age and weight are given, is the
    ValueError raised.
    """

    def test_error_age(self):
        """
        Test that checks if the expected ValueError is raised when an invalid age is given as input.
        Age should be a positive number. Test passes when error is raised.
        """
        a = -1
        with pytest.raises(ValueError):
            Herbivore(age=a)
        with pytest.raises(ValueError):
            Carnivore(age=a)

    def test_error_weight(self):
        """
        The test checks if the expected ValueError is raised, when an invalid weight is given as
        input. The weight should be positive (> 0). The test passes if the error is raised.
        """
        w = -1
        with pytest.raises(ValueError):
            Herbivore(weight=w)
        with pytest.raises(ValueError):
            Carnivore(weight=w)

    def test_default_age(self):
        """
        Test that when we create animals without arguments then age should be set to 0 by default.
        """
        h = Herbivore()
        c = Carnivore()
        assert h.get_age() == 0 and c.get_age() == 0

    def test_default_weight(self):
        """
        The test checks if the default weight given to herbivores and carnivores are indeed from
        the normal distribution. Do this by creating 500 herbivores and 500 carnivores,
        then see if the distribution of the 500 weights of each animal are normally distributed.


        We run a hypothesis test to decide if distribution is normal.
        Use the Chi-Squared test. The test hypothesis says that distribution is normal/Gaussian.
        If the calculated p-value is less than limit (we chose 0.05), then we reject the hypothesis,
        assume distribution is not normal. If p-value is greater than limit 0.05 we fail to reject
        the hypothesis, the distribution is probably gaussian.

        """
        weights_h = []
        weights_c = []

        for _ in range(500):
            h = Herbivore()
            c = Carnivore()
            weights_h.append(h.get_weight())
            weights_c.append(c.get_weight())

        statistic_h, p_val_h = chisquare(weights_h)
        statistic_c, p_val_c = chisquare(weights_c)

        assert p_val_h > 0.05 and p_val_c > 0.05

    def test_correct_age_and_weight(self):
        """
        The test checks if the weight and age of the animals are the same as the input values
        we gave for age and weight, considering they are valid values.
        """
        a = 5
        w = 7
        h = Herbivore(a, w)
        c = Carnivore(a, w)
        assert h.get_age() == a and c.get_age() == a
        assert h.get_weight() == w and c.get_weight() == w


def test_aging():
    """
    The test checks whether after each call to update_age() the age of the animal is increased by
    1 year.
    """
    h = Herbivore()
    c = Carnivore()
    for i in range(10):
        h.update_age()
        c.update_age()
        assert h.get_age() == i + 1
        assert c.get_age() == i + 1


class TestChangeWeight:
    """
    This class consists of tests for change in weight. That is, test that the weight of the animal
    is changed when the functions are called.
    """

    def test_annual_weight_decrease(self):
        """
        Each year the animals loose weight, weight = weight - eta * weight. Test that the weight of
        the animal is decreased when decrease_weight() is called.
        """
        h = Herbivore()
        weight_old = h.get_weight()
        h.decrease_weight()
        weight_new = h.get_weight()

        c = Carnivore()
        c_old_w = c.get_weight()
        c.decrease_weight()
        c_weight_new = c.get_weight()

        assert weight_old > weight_new
        assert c_old_w > c_weight_new

    def test_weight_decrease_after_birth(self):
        """
        After an animal gives birth, the mother looses weight, she looses xi*(weight of child).
        Test that mother animal looses the expected amount of weight when giving birth to new child.
        """
        h_mother = Herbivore(10, 35)  # values that give certain birth
        h_child = Herbivore()
        h_expected = h_mother.get_weight() - h_mother.default_params['xi'] * h_child.get_weight()
        h_mother.weight_decrease_birth(h_child.get_weight())

        c_mother = Carnivore(10, 35)
        c_child = Carnivore()
        c_expected = c_mother.get_weight() - c_mother.default_params['xi'] * c_child.get_weight()
        c_mother.weight_decrease_birth(c_child.get_weight())

        assert h_mother.get_weight() == h_expected
        assert c_mother.get_weight() == c_expected


class TestCalculateFitness:
    """
    The class contains two tests for the fitness of the animal.
    """

    def test_calculate_fitness_0_weight(self):
        """
        The test checks if the fitness of an animal with weight 0 is 0, that is, when the animal
        is dead. Create Herbivore and Carnivore instances with weight 0 to achieve this.
        """
        h = Herbivore(10, 0)
        c = Carnivore(10, 0)

        assert h.get_fitness() == 0
        assert c.get_fitness() == 0

    @pytest.mark.parametrize('set_params', [{'phi_age': None, 'a_half': None, 'phi_weight': None,
                                             'w_half': None}])
    def test_calculate_fitness_correctly(self, set_params):
        """
        When giving specific values for the parameters used to calculate fitness for an animal, test
        if calculate_fitness() changes the fitness to the expected value (calculated by equation (3)
        and (4) from project description). In order to reset the parameters to their default values
        after the test is executed, we send the pytest fixture set_params as input to this test.

        The test takes set_params as input to make sure that after the test is executed the
        parameters are set back to original default_values.
        """
        h = Herbivore(5, 5)
        h.set_params({'phi_age': 0.6, 'a_half': 40.0, 'phi_weight': 0.1, 'w_half': 10.0})
        h.calculate_fitness()
        assert h.get_fitness() == 0.3775406685118729

        c = Carnivore(10, 10)
        c.set_params({'phi_age': 0.3, 'a_half': 40.0, 'phi_weight': 0.4, 'w_half': 4.0})
        c.calculate_fitness()
        assert c.get_fitness() == 0.9167141719897088


class TestGivesBirth:
    """
    This test class perform several tests to see if the give_birth() function performs as expected.
    """

    def test_not_enough_animals(self):
        """
        An animal can only give birth if there is at least two animals of the same species
        in the cell. Test that the give_birth() function returns None when the number of
        animals in the cell is 1.
        """
        h = Herbivore()
        c = Carnivore()
        for _ in range(100):
            assert h.give_birth(1) is None
            assert c.give_birth(1) is None

    def test_weight_less_than_enough(self):
        """
        When the weight of the animal is less than zeta*(w_birth + sigma_birth), the probability
        of giving birth is 0, hence the give_birth() function should return None.
        For the default values of the parameters, this equation is equal to
        33.25 for herbivores and 24.5 for carnivores. Make instances of Herbivore and Carnivore
        with weights less than these to make sure give_birth returns None. Number of animals in cell
        is given a large enough value to make sure that this is not the reason why give_birth()
        returns None.
        """
        h = Herbivore(10, 30)
        c = Carnivore(10, 20)
        assert h.give_birth(10) is None and c.give_birth(10) is None

    def test_weight_of_child_higher_than_mother(self):
        """
        If the weight of the animal is less than xi*(weight of child) where xi > 1, the animal
        should not give birth, give_birth() should return None. This is the case when the animal is
        newborn (age 0), and weight is drawn from gaussian distribution (which a potential child
        weight would be).
        """
        h = Herbivore()
        c = Carnivore()
        assert h.give_birth(10) is None and c.give_birth(10) is None

    def test_certain_birth(self):
        """
        When the animal has good/high fitness, weights enough and there are several animals of the
        same species in the cell, it should give birth. give_birth() should return an instance
        of the animals class (not None).
        """
        h = Herbivore(10, 35)
        c = Carnivore(10, 35)

        assert h.give_birth(10) is not None
        assert c.give_birth(10) is not None

    def test_creates_an_instance(self):
        """
        When the animals give birth, an instance of the animals class (child) should be returned
        from give_birth() function. Make sure that a herbivore gives birth to a herbivore, and a
        carnivore gives birth to a carnivore.
        """
        h = Herbivore(10, 35)
        c = Carnivore(10, 35)

        child_h = h.give_birth(10)
        child_c = c.give_birth(10)
        assert type(h) == type(child_h) and type(c) == type(child_c)


class TestMigration:
    """
    Test class performs multiple test on migration() function.
    """

    def test_does_not_migrate(self, mocker):
        """
        For testing that animal does not migrate we use a mocker to make random.random return 1,
        the calculated probability of migration can not be greater than 1.
        """
        mocker.patch('random.random', return_value=1)

        h = Herbivore()
        assert h.migration(1, 2) is None

        c = Carnivore()
        assert c.migration(1, 2) is None

    @pytest.mark.parametrize('set_params', [{'mu': 1}])
    def test_migration(self, set_params, mocker):
        """
        To tests that animals with good fitness (age and weight given as input) do migrate
        (probability is high when parameter mu is high) and a coordinate for adjacent neighbor cell
        is returned, we use a mocker to make random.random return 0 (probability of moving is
        greater than 0), and make random.choice return coordinate tuple (4, 4) when starting point
        of animal is (5, 4).

        The test takes set_params as input to make sure that after the test is executed the
        parameters are set back to original default_values.
        """
        mocker.patch('random.random', return_value=0)
        mocker.patch('random.choice', return_value=(4, 4))

        h = Herbivore(15, 35)
        h.set_params({'mu': 1})
        assert h.migration(5, 4) == (4, 4)

        c = Carnivore(10, 35)
        c.set_params({'mu': 1})
        assert c.migration(5, 4) == (4, 4)


class TestDies:
    """
    This class contains tests for the dies() function of the Fauna (and therefore Herbivore and
    Carnivore) class.
    """

    def test_certain_death(self):
        """
        If the weight of the animal is 0, the animal is considered dead ( no probability even
        considered). We create two animals (Herbivore and Carnivore) with weight 0 and assert that
        they do actually die. If animal dies its status is updated and .alive is set to False.
        """
        h = Herbivore(0, 0)
        h.dies()
        assert h.alive is False

        c = Carnivore(0, 0)
        c.dies()
        assert c.alive is False

    def test_certain_survival(self, mocker):
        """
        When the animals are of good health and still young they should not die, dies() should not
        update the status of the animal so .alive should remain True. We use a mocker to make sure
        random.random returns 1, that way probability of dying can not be greater than random number
        1.
        """
        mocker.patch('random.random', return_value=1)

        h = Herbivore(10, 10)
        h.dies()
        assert h.alive is True

        c = Carnivore(10, 10)
        c.dies()
        assert c.alive is True


class TestKillsHerbivore:
    """
    This test class contains several tests for the kills_herbivore() function in the Carnivore
    class.
    """

    def test_fitness_too_low(self):
        """
        If the fitness of the carnivore is less than or equal to the fitness of the herbivore it
        tries to kill, kills_herbivore() should return False. Test this by making instances of
        Herbivore and Carnivore where carnivore has low fitness and herbivore has high fitness.
        """
        h = Herbivore(10, 10)
        assert h.alive is True
        c = Carnivore(1, 1)
        c.kills_herbivore(h)
        assert h.alive is True

    @pytest.mark.parametrize('set_params', [{'DeltaPhiMax': 0.01}])
    def test_certain_kill(self, set_params):
        """
        If the fitness of the carnivore is higher than the fitness of the herbivore, and the
        difference between herbivore and carnivore fitness is higher then DeltaPhiMax, the carnivore
        has a successful hunt and herbivore will be tagged with h.alive = False.

        The test takes set_params as input to make sure that after the test is executed the
        parameters are set back to original default_values.
        """

        h = Herbivore(2, 5)
        c = Carnivore(20, 35)
        c.set_params({'DeltaPhiMax': 0.01})
        c.kills_herbivore(h)
        assert h.alive is False

    def test_certain_kill_with_prob_calc(self, mocker):
        """
        If the fitness of the carnivore is higher than the fitness of the herbivore and the
        difference of their fitness values falls in range between 0 and DeltaPhiMax then the
        probability of the successful hunt is calculated and if it is higher than a randomly drawn
        number from [0,1) (which by using a mocker was set to 0) then it should set the h.alive
        to False.
        """
        mocker.patch('random.random', return_value=0)

        h = Herbivore(2, 6)
        c = Carnivore(15, 20)
        c.kills_herbivore(h)
        assert h.alive is False


class TestFeeding:
    """
    This class tests that the feeding functions in the animal classes work.
    """

    def test_herb_enough_food(self):
        """
        If the amount of available fodder in the cell is greater than what the herbivore
        desires (F), a single call to feeding() should make the herbivore eat amount F and
        weight should be increased by beta * F.
        """
        h = Herbivore(10, 10)
        weight_old = h.get_weight()
        h.feeding(available_fodder=20)
        weight_new = h.get_weight()
        assert weight_new == weight_old + h.default_params['F'] * h.default_params['beta']

    def test_herb_not_enough_food(self):
        """
        If the amount of fodder in cell is less than what herbivore desires, the herbivore will
        eat all of the fodder and weight should increase by beta * available fodder.
        """
        h = Herbivore(10, 10)
        weight_old = h.get_weight()
        available_fodder = 9
        h.feeding(available_fodder)
        weight_new = h.get_weight()

        assert weight_new == weight_old + available_fodder * h.default_params['beta']

    def test_herb_available_food_updated(self):
        """
        Test that available fodder is updated correctly. Make herbivore who desires amount F = 10
        of fodder eat where available fodder is 15 and check that remaining fodder is 5.
        """
        h = Herbivore(10, 10)
        available_fodder = 15
        remaining = h.feeding(available_fodder)
        assert remaining == 5

    def test_herb_fitness_updated(self):
        """
        Test that the fitness of herbivore is increased after it has eaten, hence gained weight.
        """
        h = Herbivore(10, 10)
        fitness_old = h.get_fitness()
        h.feeding(20)
        fitness_new = h.get_fitness()
        assert fitness_new > fitness_old

        h.feeding(10)
        fitness_latest = h.get_fitness()
        assert fitness_latest > fitness_new > fitness_old

    @pytest.mark.parametrize('set_params', [{'DeltaPhiMax': 0.01}])
    def test_carn_feed_less_than_F(self, set_params):
        """
        When we make sure the carnivore has good enough fitness and probability of killing
        herbivores. Send in a list of herbivores who weigh less than what he desires to eat in a
        year. Make sure weight of carnivore only increases by beta*weight of pray. And check that
        the two herbivores are dead after the function is called. Ensure certain kill by setting
        DeltaPhiMax to 0.1.
        """
        h1 = Herbivore(2, 5)
        h2 = Herbivore(2, 3)
        herbivores = [h1, h2]
        c = Carnivore(20, 35)

        c.set_params({'DeltaPhiMax': 0.01})
        c.feeding(herbivores)
        expected_weight_carnivore = 35 + c.default_params['beta'] * 5 + c.default_params['beta'] * 3

        assert c.get_weight() == expected_weight_carnivore
        assert not h1.alive and not h2.alive

    @pytest.mark.parametrize('set_params', [{'DeltaPhiMax': 0.01, 'F': 10}])
    def test_carn_feed_F(self, set_params):
        """
        If the weight of the prey weights more than desired amount F the weight of the carnivore
        will not increase by more than beta*F. We set F to be 10, and DeltaPhiMax to 0.1 to ensure
        certain kill.
        """
        h1 = Herbivore(2, 5)
        h2 = Herbivore(2, 6)
        herbivores = [h1, h2]
        c = Carnivore(20, 35)
        c.set_params({'DeltaPhiMax': 0.01, 'F': 10})
        c.feeding(herbivores)
        expected_weight_carnivore = 35 + c.default_params['beta'] * 10
        assert c.get_weight() == expected_weight_carnivore
        assert not h1.alive and not h2.alive

    @pytest.mark.parametrize('set_params', [{'DeltaPhiMax': 0.01, 'F': 10}])
    def test_carn_feed_herbivore_survives(self, set_params):
        """
        If the carnivore gets full after killing the first two herbivores, the last one should not
        get killed. Set DeltaPhiMax to 0.01 to ensure certain kill. Set F to 10 to easier test the
        function (do not need to send a lot of herbivores in the list).
        """
        h1 = Herbivore(2, 5)
        h2 = Herbivore(2, 6)
        h3 = Herbivore(2, 5)
        herbivores = [h1, h2, h3]
        c = Carnivore(20, 35)
        c.set_params({'DeltaPhiMax': 0.01, 'F': 10})
        c.feeding(herbivores)
        expected_weight_carnivore = 35 + c.default_params['beta'] * 10
        assert c.get_weight() == expected_weight_carnivore
        assert not h1.alive and not h2.alive and h3.alive
