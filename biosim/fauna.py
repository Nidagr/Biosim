# -*- encoding: utf-8 -*-
__author__ = "Nida Grønbekk and Yuliia Dzihora"
__email__ = 'nida.gronbekk@nmbu.no and yuliia.dzihora@nmbu.no'


import random
import math


class Fauna:
    """
    Class Fauna is a super class and includes certain characteristics that herbivores and carnivores
    have in common. Each animal has it's own age, weight and fitness that is calculated from the
    first 2 parameters. If no input argument is given for age or weight, age by default is set to 0
    and weight is drawn randomly from Gaussian distribution with mean w_birth and standard
    deviation sigma_birth. The default values for these parameters is given inside the subclasses.

    All default parameters are stored as a dictionary (default_params) and is set to Nones in the
    parent class and different values are set in the subclasses.
    """

    default_params = {'w_birth': None, 'sigma_birth': None, 'beta': None,
                      'eta': None, 'F': None, 'phi_age': None, 'a_half': None,
                      'phi_weight': None, 'w_half': None, 'xi': None,
                      'zeta': None, 'gamma': None, 'omega': None, 'DeltaPhiMax': None,
                      'seed': None, 'mu': None}

    @classmethod
    def set_params(cls, new_params):
        """
        Function that allows you to set/overwrite parameters. A dictionary with parameter names and
        values should be sent in as input. Some of the parameters have specified limits which
        this function will ensure is held.

        :param new_params: Set of parameters for animals.
        :type new_params: dict

        w_birth: mean weight of a newborn animal;
        sigma_birth: standard deviation from w_birth for a newborn;
        beta: coefficient for weight increase by feeding;
        eta: coefficient of annual weight decrease;
        F: amount of fodder (amount of food animal wants to eat in a year);
        phi_age: age coefficient for fitness calculation;
        a_half: half-age coefficient for fitness calculation;
        phi_weight: weight coefficient for fitness calculation;
        w_half: half-weight coefficient for fitness calculation;
        xi: coefficient of weight decrease, while giving birth;
        zeta: coefficient for comparison of weight of mother and a possible offspring;
        gamma: coefficient for calculation of probability of giving birth;
        omega: coefficient for calculation of probability of dying;
        DeltaPhiMax: maximum fitness, which influences the probability of killing herbivore by
        carnivore;
        mu: coefficient for calculation of probability of migration.

        :raises KeyError: Invalid parameter name, name is not in the list of legal keys.
        :raises ValueError: Value does not meet requirements, eta should be less than 1 and greater
        than 0.
                ValueError: Value does not meet requirements, DeltaPhiMax should be greater than 0.
                ValueError: Value does not meet requirements, key value should be greater or equal
                to 0.
                ValueError: raised if age is less then 0.
                ValueError: raised if weight is negative.
        """

        for key in new_params:
            if key not in cls.default_params:
                raise KeyError('Invalid parameter name: ' + key)

        for key in new_params:
            if key in cls.default_params:
                if key == 'eta' and new_params[key] > 1:
                    raise ValueError('Eta must be in [0, 1].')
                if key == 'DeltaPhiMax' and new_params[key] <= 0:
                    raise ValueError('DeltaPhiMax must be greater than 0.')

                if not new_params[key] >= 0:
                    raise ValueError('{} must be greater or equal to 0.'.format(key))
                cls.default_params[key] = new_params[key]

    def __init__(self, age=None, weight=None):
        """
        Constructor method. If no input arguments are given, age is 0 and weight is randomly drawn.
        Set fitness to 0 and then calculate it.
        """
        self._age = age if age is not None else 0
        if self._age < 0:
            raise ValueError('Age must be positive.')
        self._weight = weight if weight is not None else \
            random.gauss(self.default_params['w_birth'], self.default_params['sigma_birth'])
        if self._weight < 0:
            raise ValueError('Weight should not be negative.')

        self.alive = True

        self._fitness = 0
        self.calculate_fitness()

    def get_age(self):
        """
        Function gets current age of the animal.

        :return: Current age.
        :rtype: int
        """
        return self._age

    def update_age(self):
        """
        When the simulation starts a new year, this function is called and will increase the age by
        1 year. Fitness is re-calculated right after age update, since age affects the fitness of an
        animal.
        """
        self._age += 1
        self.calculate_fitness()

    def get_weight(self):
        """
        Function gets current weight of the animal.

        :return: Current weight.
        :rtype: float
        """
        return self._weight

    def decrease_weight(self):
        """
        Each year that passes, animals loose certain weight that is increased by age. It is defined
        by multiplication of weight of the animal by the parameter 'eta'. Also, since the weight
        changes, the fitness is updated right after.
        """
        self._weight -= self.default_params['eta'] * self._weight
        self.calculate_fitness()

    def weight_decrease_birth(self, weight_child):
        """
        If gives_birth() returns an instance of the class it also calls this function to decrease
        the weight of the mother after giving birth. Thereafter, since an animal changed the weight
        the fitness is re-calculated right after.

        :parameter weight_child: Weight of the newborn animal.
        :type weight_child: float
        """
        self._weight -= self.default_params['xi'] * weight_child
        self.calculate_fitness()

    def calculate_fitness(self):
        """
        The overall state of the animal is described by its fitness, which is calculated from the
        age and the weight of the animal. Therefore every time animal changes any of those
        values, fitness should be re-calculated. If the weight of the animal is 0, animal fitness is
        set to 0.

        To calculate fitness the following parameters are used: phi_age, a_half, phi_weigh, w_half
        """
        if self._weight <= 0:
            self._fitness = 0
        else:
            var_1 = 1 / (1 + math.exp(self.default_params['phi_age'] *
                                      (self._age - self.default_params['a_half'])))
            var_2 = 1 / (1 + math.exp(-self.default_params['phi_weight'] *
                                      (self._weight - self.default_params['w_half'])))
            self._fitness = var_1 * var_2

    def get_fitness(self):
        """
        Function gets current fitness of the animal.

        :return: Current fitness.
        :rtype: int
        """
        return self._fitness

    def migration(self, row, col):
        """
        Function decides whether animal tries to move and if so, return the coordinates of the cell
        it wants to move into. The animal moves if its fitness multiplied by parameter mu is higher
        than a randomly drawn number from the uniform distribution [0, 1). If it tries to move,
        the random.choice function draws a random element from the dictionary, which contains
        coordinates of the immediately adjacent cells.

        :param row: row coordinate of cell animal is in
        :type row: int
        :param col: col coordinate of cell animal is in
        :type col: int

        :return: Coordinates of direction animal wants to move, if it moves.
        :rtype: tuple of ints
        """
        p_migration = self.default_params['mu'] * self._fitness
        r = random.random()
        if r < p_migration:
            move_options = {"north": (row - 1, col), "south": (row + 1, col),
                            "west": (row, col - 1), "east": (row, col + 1)}
            return random.choice(list(move_options.values()))

    def probability_birth(self, num_animals_cell):
        """
        Animals mate, if there are at least 2 animals of the same species in the cell (landscape).
        For each animal in the cell the probability of giving birth is 0 if weight of the animals
        is less than value calculated by the formula: zeta * (w_birth + sigma_birth).

        Otherwise, probability is calculated and if the calculated value is higher, than a randomly
        drawn number from uniformly distributed range [0, 1), the animal will give birth (return
        True).

        :param num_animals_cell: How many animals of this species are in this cell.
        :type num_animals_cell: int

        :return: Answer whether event happens or not.
        :rtype: bool
        """
        if (num_animals_cell < 2) or (self._weight < self.default_params['zeta'] *
                                      (self.default_params['w_birth'] +
                                       self.default_params['sigma_birth'])):
            return False
        else:
            p_birth = min(1, self.default_params['gamma'] * self._fitness * (num_animals_cell - 1))
            r = random.random()
            return r < p_birth

    def give_birth(self, num_animals_cell):
        """
        If the weight of the child multiplied by parameter xi is less than weight of the animal
        that gives birth, then animal actually gives birth and returns an instance of a child of
        same type as mother.

        :param num_animals_cell: Number of animals of the same type in the cell of island.
        :type num_animals_cell: int

        :return: None or instance of a child
        :rtype: None or object of type(self)
        """
        boolean = self.probability_birth(num_animals_cell)
        weight_child = random.gauss(self.default_params['w_birth'],
                                    self.default_params['sigma_birth'])
        if self._weight > self.default_params['xi'] * weight_child and boolean:
            self.weight_decrease_birth(weight_child)
            return self.__class__(0, weight_child)
        else:
            return None

    def dies(self):
        """
        Each animal can die with certain probability that is calculated by following formula:
        omega * (1-fitness). After calculating the probability, it is compared with a randomly drawn
        value from uniformly distributed range [0, 1) and if the probability is higher than the
        random number the event happens. Also, if weight of animal reaches 0 the animal dies.

        Function updates status of the animal from .alive = True to .alive = False if animal dies,
        otherwise it remains the same.
        """
        p_death = self.default_params['omega'] * (1 - self._fitness)
        r = random.random()
        if r < p_death or self._weight == 0:
            self.alive = False


class Herbivore(Fauna):
    """
    Class that inherits all the functions from super class Fauna and also describes characteristics
    of the Herbivores. Herbivore class has different set of default_params. Also, they do not have
    parameter DeltaPhiMax so it stays set to None from super class settings.
    """

    default_params = {'w_birth': 8, 'sigma_birth': 1.5, 'beta': 0.9,
                      'eta': 0.05, 'F': 10, 'phi_age': 0.6, 'a_half': 40,
                      'phi_weight': 0.1, 'w_half': 10, 'xi': 1.2,
                      'zeta': 3.5, 'gamma': 0.2, 'omega': 0.4, 'DeltaPhiMax': None,
                      'seed': 12345, 'mu': 0.25}

    def __init__(self, age=None, weight=None):
        """
        Constructor method. Stays the same as in the super class Fauna.
        """
        super().__init__(age, weight)

    def feeding(self, available_fodder):
        """
        The function increases the weight of the Herbivore according to the amount of food that is
        consumed by the animal.
        The maximum amount of fodder eaten by the herbivore is defined by the parameter F (which is
        the amount of fodder herbivores tries to eat each year). After the herbivore ate, the amount
        of available fodder should be updated, and the fitness of the animal is recalculated due to
        the change of weight. The function returns the amount of available fodder to make sure the
        cell is updated.

        :param available_fodder: Amount of fodder available for herbivores to eat.
        :type available_fodder: float

        :return available_fodder: How much fodder is left in the cell after the herbivore is
        finished eating.
        :rtype: float
        """

        if available_fodder >= self.default_params['F']:
            self._weight += self.default_params['beta'] * self.default_params['F']
            self.calculate_fitness()
            available_fodder -= self.default_params['F']
            return available_fodder

        else:
            self._weight += self.default_params['beta'] * available_fodder
            self.calculate_fitness()
            available_fodder = 0
            return available_fodder


class Carnivore(Fauna):
    """
    Class that inherits all the functions from super class Fauna and also describes characteristics
    of the Carnivores. Carnivore class has different set of default_params.
    """

    default_params = {'w_birth': 6, 'sigma_birth': 1, 'beta': 0.75,
                      'eta': 0.125, 'F': 50, 'phi_age': 0.3, 'a_half': 40,
                      'phi_weight': 0.4, 'w_half': 4, 'xi': 1.1, 'zeta': 3.5,
                      'gamma': 0.8, 'omega': 0.8, 'DeltaPhiMax': 10, 'mu': 0.4}

    def __init__(self, age=None, weight=None):
        """
        Constructor method. Stays the same as in super class Fauna.
        """
        super().__init__(age, weight)

    def kills_herbivore(self, prey):
        """
        This method allows us to make a decision whether a carnivore kills its prey or not. If it
        does kill, change the status of the prey to .alive == False. The outcome depends on
        multiple factors. Carnivore has a chance to kill if its fitness is higher than fitness
        of the prey. If the fitness of the carnivore is higher then the fitness of the prey, it
        checks if the value obtained by subtraction of herbivore fitness from carnivore fitness
        falls in range from 0 to parameter DeltaPhiMax. If that is the case, we calculate the
        probability of killing. If it is higher than a randomly drawn number from uniformly
        distributed range [0, 1) the event happens. If the fitness difference between carnivore and
        herbivore is higher than DeltaPhiMax, then carnivore kills the herbivore as well.

        :param prey: instance of the herbivore that the carnivore attempts to kill.
        :type prey: object Herbivore
        """
        prey_fit = prey.get_fitness()

        if self._fitness > prey_fit:
            if 0 < (self._fitness - prey_fit) < self.default_params['DeltaPhiMax']:
                p_kill = (self._fitness - prey_fit) / self.default_params['DeltaPhiMax']
                r = random.random()
                if r < p_kill:
                    prey.alive = False
            else:
                prey.alive = False

    def feeding(self, list_of_herbs):
        """
        We start by iterating through the sorted list of herbivores. They are sorted by fitness in
        ascending order (weakest to strongest). If it is still alive we call the function
        kills_herbivore() which decides whether the Carnivore kills or not. If it does, increase the
        weight of the carnivore by beta * weight of prey. Iterate through the list of herbivores
        and attempt to kill until the Carnivore has eaten the desired amount F, or until it has
        tried to kill everyone (and failed at getting full).

        If the herbivore getting killed weighs more than what the carnivore needs, the carnivore
        only eats the desired amount and the leftovers from the herbivore are going to waste.

        :param list_of_herbs: sorted list of herbivores (by their fitness in ascending order)
        :type list_of_herbs: lst
        """
        eaten_food = 0
        for h in list_of_herbs:
            if h.alive:
                self.kills_herbivore(h)
                if h.alive is False:
                    if eaten_food < self.default_params['F']:
                        if h.get_weight() >= self.default_params['F'] - eaten_food:
                            self._weight += self.default_params['beta'] * (self.default_params['F']
                                                                           - eaten_food)
                            self.calculate_fitness()
                            return
                        else:
                            self._weight += self.default_params['beta'] * h.get_weight()
                            self.calculate_fitness()
                            eaten_food += h.get_weight()
