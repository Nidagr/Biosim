# -*- encoding: utf-8 -*-
__author__ = "Nida Grønbekk and Yuliia Dzihora"
__email__ = 'nida.gronbekk@nmbu.no and yuliia.dzihora@nmbu.no'

from biosim.landscape import Highland, Lowland, Desert, Water
from biosim.fauna import Herbivore, Carnivore
import pytest


@pytest.fixture(scope='function')
def set_params(request):
    """
    Fixture sets parameters on Landscape subclasses Highland, Lowland, Desert and Water.

    The fixture sets Landscape subclasses parameters when called for setup, and resets them when
    called for teardown.
    This ensures that modified  parameters are always reset before leaving a test.

    Based on https://stackoverflow.com/a/33879151

    Parameters
    __________
    request
        Request object automatically provided by pytest.
        request.param is the parameter dictionary to be passed to
        landscape.*.set_params()

        Taken from lecture notes
    """
    Lowland.set_landscape_params(request.param)
    Highland.set_landscape_params(request.param)
    Desert.set_landscape_params(request.param)
    Water.set_landscape_params(request.param)
    Herbivore.set_params(request.param)
    Carnivore.set_params(request.param)

    yield

    Lowland.set_landscape_params(Lowland.default_params)
    Highland.set_landscape_params(Highland.default_params)
    Desert.set_landscape_params(Desert.default_params)
    Water.set_landscape_params(Water.default_params)
    Herbivore.set_params(Herbivore.default_params)
    Carnivore.set_params(Carnivore.default_params)


class TestSetParams:
    """
    This class tests set_landscape_params() for the four different types of landscapes.
    """

    @pytest.mark.parametrize('set_params', [{'f_max': 5}])
    def test_set_landscape_params(self, set_params):
        """
        Four objects are created, each of them an instance of a landscape subclass. For each test
        that when set_landscape_params() is called with input {'f_max': 5}, the new
        default_params['f_max'] is actually 5.

        The test takes set_params as input to make sure that after the test is executed the
        parameters are set back to original default_values.
        """
        w = Water()
        h = Highland()
        l = Lowland()
        d = Desert()
        w.set_landscape_params({'f_max': 5})
        h.set_landscape_params({'f_max': 5})
        l.set_landscape_params({'f_max': 5})
        d.set_landscape_params({'f_max': 5})
        assert w.default_params['f_max'] == 5 and h.default_params['f_max'] == 5 \
               and l.default_params['f_max'] == 5 and d.default_params['f_max'] == 5

    def test_set_landscape_params_negative_f_max(self):
        """
        Four objects are created, each of them an instance of a landscape subclass. For each of the
        four objects test that when set_landscape_params() is called with input {'f_max': -5},
        a ValueError is raised.
        """
        w = Water()
        h = Highland()
        l = Lowland()
        d = Desert()
        with pytest.raises(ValueError):
            w.set_landscape_params({'f_max': -5})
        with pytest.raises(ValueError):
            h.set_landscape_params({'f_max': -5})
        with pytest.raises(ValueError):
            l.set_landscape_params({'f_max': -5})
        with pytest.raises(ValueError):
            d.set_landscape_params({'f_max': -5})

    def test_set_landscape_params_nonexistent(self):
        """
        Four objects are created, each of them an instance of a landscape subclass. For each of the
        four objects test that when set_landscape_params() is called with input {'grass': 3},
        a ValueError is raised as no such parameter exists inside the landscape classes.

        """
        w = Water()
        h = Highland()
        l = Lowland()
        d = Desert()
        with pytest.raises(KeyError):
            w.set_landscape_params({'grass': 3})
        with pytest.raises(KeyError):
            h.set_landscape_params({'grass': 3})
        with pytest.raises(KeyError):
            l.set_landscape_params({'grass': 3})
        with pytest.raises(KeyError):
            d.set_landscape_params({'grass': 3})


def test_landscape_accessible():
    """
    Each subclass of Landscape has a property accessible which is True or False. We make four
    objects, each an instance of one of the subclasses. All landscape types should be
    accessible except for Water. So see if the objects are accessible except from water object.
    """
    w = Water()
    h = Highland()
    l = Lowland()
    d = Desert()
    assert h.accessible and l.accessible and d.accessible and not w.accessible


def test_landscape_annual_f_max():
    """
    Test that available_fodder in landscape is set to f_max after annual_f_max() is called.
    First set available_fodder to 0 and then call annual_f_max to see if it actually changed.
    Make four objects of the four Landscape subclasses and test on them.
    """
    w = Water()
    w.available_fodder = 0
    h = Highland()
    h.available_fodder = 0
    l = Lowland()
    l.available_fodder = 0
    d = Desert()
    d.available_fodder = 0

    w.annual_f_max()
    h.annual_f_max()
    l.annual_f_max()
    d.annual_f_max()

    assert w.available_fodder == w.default_params['f_max']
    assert h.available_fodder == h.default_params['f_max']
    assert l.available_fodder == l.default_params['f_max']
    assert d.available_fodder == d.default_params['f_max']


def test_landscape_update_age_highland():
    """
    Test that all animals residing in a Highland cell gets their ages updated by one year after
    update_age() is called. Need to first make some instances of animals and add to the lists of
    animals in the cell.
    """
    h1 = Herbivore()
    h2 = Herbivore()
    c1 = Carnivore()
    c2 = Carnivore()

    h = Highland()

    h.herbivores.append(h1)
    h.herbivores.append(h2)
    h.carnivores.append(c1)
    h.carnivores.append(c2)

    h.aging()

    for herb in h.herbivores:
        assert herb.get_age() == 1
    for carn in h.carnivores:
        assert carn.get_age() == 1


def test_landscape_update_age_lowland():
    """
    Test that all animals residing in a Lowland cell gets their ages updated by one year after
    update_age() is called. Need to first make some instances of animals and add to the lists of
    animals in the cell.
    """
    h1 = Herbivore()
    h2 = Herbivore()
    c1 = Carnivore()
    c2 = Carnivore()

    l = Lowland()

    l.herbivores.append(h1)
    l.herbivores.append(h2)
    l.carnivores.append(c1)
    l.carnivores.append(c2)

    l.aging()

    for herb in l.herbivores:
        assert herb.get_age() == 1
    for carn in l.carnivores:
        assert carn.get_age() == 1


def test_landscape_update_age_desert():
    """
    Test that all animals residing in a Desert cell gets their ages updated by one year after
    update_age() is called. Need to first make some instances of animals and add to the lists of
    animals in the cell.
    """
    h1 = Herbivore()
    h2 = Herbivore()
    c1 = Carnivore()
    c2 = Carnivore()

    d = Desert()

    d.herbivores.append(h1)
    d.herbivores.append(h2)
    d.carnivores.append(c1)
    d.carnivores.append(c2)

    d.aging()

    for herb in d.herbivores:
        assert herb.get_age() == 1
    for carn in d.carnivores:
        assert carn.get_age() == 1


def test_feed_herbivores():
    """
    Herbivores try to eat an amount F = 10 of fodder. If three herbivores eats the desired amount,
    then available_fodder should be 0 if there was 30 from the beginning.
    """
    land = Highland()
    h1 = Herbivore(10, 10)
    h2 = Herbivore(10, 15)
    h3 = Herbivore(10, 20)
    land.herbivores.append(h1)
    land.herbivores.append(h2)
    land.herbivores.append(h3)
    land.available_fodder = 30
    land.feed_herbivores()
    assert land.available_fodder == 0


def test_sorting_carnivores():
    """
    Test that carnivores actually get sorted by fitness when using function
    sorted(carns, key=fitness, reverse = True).
    """
    c1 = Carnivore()
    c2 = Carnivore(10, 10)
    c3 = Carnivore(15, 25)
    c4 = Carnivore(20, 30)
    r = [c3, c1, c4, c2]
    r.sort(key=lambda x: x.get_fitness(), reverse=True)

    assert r == [c3, c4, c2, c1]


@pytest.mark.parametrize('set_params', [{'DeltaPhiMax': 0.01}])
def test_feed_carnivores_dead_herbivores(set_params):
    """
    If the first herbivore is already dead, then carnivore should skip to the next and try to kill
    this one.
    """
    high = Highland()
    c = Carnivore(15, 25)
    high.carnivores.append(c)
    h1 = Herbivore(2, 5)
    h2 = Herbivore(2, 7)
    high.herbivores.append(h1)
    high.herbivores.append(h2)
    h1.alive = False
    # Make sure carnivore will kill
    c.set_params({'DeltaPhiMax': 0.01})
    high.feed_carnivores()
    c_new_weight = 25 + c.default_params['beta'] * 7
    assert c.get_weight() == c_new_weight and not h2.alive


@pytest.mark.parametrize('set_params', [{'DeltaPhiMax': 0.01, 'F': 10}])
def test_feed_carnivores_many_herbivores(set_params):
    """
    If there are more herbivores than carnivore needs, do not attempt to kill any more.
    Set parameters to ensure kill. Set F = 10 to make test easier, not so many instances
    of herbivores needed.
    """
    high = Highland()
    c = Carnivore(15, 25)
    high.carnivores.append(c)
    # Make sure carnivore will kill
    c.set_params({'DeltaPhiMax': 0.01, 'F': 10})

    h1 = Herbivore(2, 5)
    h2 = Herbivore(2, 5)
    h3 = Herbivore(2, 5)
    high.herbivores.append(h1)
    high.herbivores.append(h2)
    high.herbivores.append(h3)

    high.feed_carnivores()
    c_new_weight = 25 + c.default_params['beta'] * c.default_params['F']
    assert c.get_weight() == c_new_weight
    assert h3.alive and not h1.alive and not h2.alive


def test_loss_of_weight():
    """
    Test that each animal in the cell loses weight after the loss_of_weight() function is called.
    """
    l = Lowland()
    h1 = Herbivore(10, 10)
    h2 = Herbivore(10, 15)
    l.herbivores.append(h1)
    l.herbivores.append(h2)
    c1 = Carnivore(10, 10)
    c2 = Carnivore(10, 12)
    l.carnivores.append(c1)
    l.carnivores.append(c2)

    l.loss_of_weight()
    assert h1.get_weight() < 10 and h2.get_weight() < 15 and c1.get_weight() < 10 \
           and c2.get_weight() < 12


def test_death(mocker):
    """
    Use mocker to make certain the animal will die. Add two animals of each species and check that
    after function death() is applied, the number of herbivores and carnivores in the cell
    should be 0.
    """
    l = Lowland()
    mocker.patch('random.random', return_value=0)
    h1 = Herbivore()
    h2 = Herbivore()
    l.herbivores.append(h1)
    l.herbivores.append(h2)
    c1 = Carnivore()
    c2 = Carnivore()
    l.carnivores.append(c1)
    l.carnivores.append(c2)

    l.death()
    assert len(l.herbivores) == 0 and len(l.carnivores) == 0


def test_procreation(mocker):
    """
    Use mocker to make random.random return 0 so that animal definitely gives birth. Also make
    sure animal weights enough and is old enough for function probability_birth to return an instance
    of the class, not None. Then assert that list of herbivores and carnivores in cell increases
    by one.
    """
    l = Lowland()
    mocker.patch('random.random', return_value=0)
    h = Herbivore(10, 35)
    l.herbivores.append(h)
    c = Carnivore(10, 35)
    l.carnivores.append(c)
    l.procreation(30, 30)

    assert len(l.herbivores) == 2 and len(l.carnivores) == 2
