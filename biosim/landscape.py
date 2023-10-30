# -*- encoding: utf-8 -*-
__author__ = "Nida Grønbekk and Yuliia Dzihora"
__email__ = 'nida.gronbekk@nmbu.no and yuliia.dzihora@nmbu.no'


class Landscape:
    """
    Landscape is the parent class for all types of landscape: Water, Highland, Lowland and Desert.
    An instance of a landscape subclass represents a single cell of the island that is to be
    simulated. Each landscape type has the parameter f_max, which represents the maximum amount of
    fodder growing in the cell. Each year the available amount of fodder in the cell regrows to
    f_max. Set it to 0 as a default value and give it a new value in the subclasses, where fodder
    grows. Initiate value available_fodder to be None, when instance of class is created. This
    variable includes the information of how much fodder is left after an animal has eaten. Will be
    updated by functions later on. Initiate empty lists for storing the carnivores and herbivores
    residing in this cell in the constructor.

    The cell will also include lists incoming_carnivores and incoming_herbivores which is of
    convenience when migrating animals in the BioSim class. They will be updated multiple times from
    there.
    """

    default_params = {'f_max': 0}
    valid_landscape_types = ['W', 'H', 'L', 'D']

    @classmethod
    def set_landscape_params(cls, new_params):
        """
        This is a function for setting the parameters of this class to a new value.

        :param new_params: dictionary with parameter names as keys and their new values as values.
            Legal keys: 'f_max' - maximum amount of fodder in landscape cell, the amount of fodder
            we have at the beginning of each year. Must be positive.
        :type new_params: dictionary
        ...
        : raises KeyError: Invalid parameter name given.
        : raises ValueError: Invalid value for parameter given. Here: <0.
        """
        for key in new_params:
            if key not in cls.default_params:
                raise KeyError('Invalid parameter name: ' + key)

        for key in new_params:
            if key in cls.default_params:
                if not new_params[key] >= 0:
                    raise ValueError('{} must be greater than or equal to 0.'.format(key))
                cls.default_params[key] = new_params[key]

    def __init__(self):
        """
        The constructor method.
        """
        self.carnivores = []
        self.herbivores = []
        self.available_fodder = None
        self.incoming_carnivores = []
        self.incoming_herbivores = []

    @property
    def accessible(self):
        """
        Check if cell is accessible.

        :return: True if this cell is accessible for animals. False otherwise. True as default,
        overwrite with False in landscape types where it is not accessible.
        :rtype: bool
        """
        return True

    def annual_f_max(self):
        """
        Set the amount of available fodder back to f_max.
        Each year the fodder regrows to f_max , before animals eat.
        """
        self.available_fodder = self.default_params['f_max']

    def feed_herbivores(self):
        """
        The function iterates through the list of herbivores in the cell and applies the feeding
        function from the Herbivore class. The function returns the amount of fodder left after each
        herbivore has eaten, update self.available_fodder according to this each time a Herbivore
        eats.
        """
        for h in self.herbivores:
            leftover = h.feeding(self.available_fodder)
            self.available_fodder = leftover

    def feed_carnivores(self):
        """
        The function first sorts animals by their fitness to ensure that the carnivores with the
        highest fitness are hunting first and that they hunt herbivores in ascending order (so the
        strongest carnivore will attempt to hunt the weakest herbivore).

        After sorting, the feeding function is applied (if carnivore kills, it updates the weight
        and fitness of carnivore, tags herbivore as .alive = False). Carnivore keeps hunting till
        it either ate enough or failed to kill the herbivore, then the next carnivore tries.

        After all the carnivores has tried to eat, we overwrite the list of herbivores in this
        cell to only contain the ones that were not killed (.alive = True)
        """
        self.carnivores.sort(key=lambda c: c.get_fitness(), reverse=True)
        self.herbivores.sort(key=lambda h: h.get_fitness(), reverse=False)
        for c in self.carnivores:
            c.feeding(self.herbivores)

        self.herbivores = [h for h in self.herbivores if h.alive]

    def procreation(self, num_herbs, num_carns):
        """
        If animal gives birth, the function will generated a new object (child) of type(self)
        (mother) and will append the child to the list of the animals in the cell.

        :param num_herbs: number of herbivores in the cell
        :type num_herbs: int

        :param num_carns: number of carnivores in the cell
        :type num_carns: int
        """

        for h in self.herbivores:
            outcome = h.give_birth(num_herbs)
            if outcome is not None:
                self.herbivores.append(outcome)

        for c in self.carnivores:
            outcome = c.give_birth(num_carns)
            if outcome is not None:
                self.carnivores.append(outcome)

    def aging(self):
        """
        Increase the age of each animal residing in this cell by one year by calling the update_age
        function from inside the Fauna class for each animal in the lists carnivores and herbivores.
        """
        for h in self.herbivores:
            h.update_age()
        for c in self.carnivores:
            c.update_age()

    def loss_of_weight(self):
        """
        When a year has passed we call this function. The weight of an animal should decrease by
        eta * weight every year. Iterate through the lists of herbivores and carnivores in the cell
        and call the decrease_weight() function from inside the Fauna class for each of them.
        """
        for h in self.herbivores:
            h.decrease_weight()
        for c in self.carnivores:
            c.decrease_weight()

    def death(self):
        """
        Call this function at the end of the year to update the lists of herbivores and carnivores
        in the cell to only contain the ones that survived. First call the dies() function from
        inside the Fauna class which decides whether animal dies or not based on probability. Then
        overwrite the lists of herbivores and carnivores in the cell to only contain the ones
        that are still alive after this call.
        """
        for h in self.herbivores:
            h.dies()
        self.herbivores = [h for h in self.herbivores if h.alive]

        for c in self.carnivores:
            c.dies()
        self.carnivores = [c for c in self.carnivores if c.alive]


class Lowland(Landscape):
    """
    Subclass of Landscape. Class representing a cell with landscape type Lowland. This type of
    landscape has fodder growing here, and is accessible for both carnivores and herbivores.
    Give f_max a new value, default value is 800. Set variable available_fodder to
    be f_max, when initiating an instance of this class.
    """

    default_params = {'f_max': 800}

    def __init__(self):
        """
        Constructor method. Only available_fodder is changed from the super class.
        """
        super().__init__()
        self.available_fodder = self.default_params['f_max']


class Highland(Landscape):
    """
    Subclass of Landscape. Class representing a cell with landscape type Highland. There is
    fodder growing here, and the cell is accessible for both carnivores and herbivores. Initiate
    available_fodder to be f_max when instance of this class is made, which has chosen default
    value 300.
    """

    default_params = {'f_max': 300}

    def __init__(self):
        """
        Constructor method. Only available_fodder is changed from the superclass.
        """
        super().__init__()
        self.available_fodder = self.default_params['f_max']


class Desert(Landscape):
    """
    Subclass of Lowland. Class represents a cell of landscape type Desert. No fodder grows here,
    No need to change f_max or available_fodder. Accessible for herbivores and carnivores.
    """
    def __init__(self):
        """
        Constructor method, no change from super class.
        """
        super().__init__()


class Water(Landscape):
    """
    Subclass of Landscape. Class representing cell of landscape type Water. No fodder here, do not
    need to update f_max or available_fodder. This cell type is not accessible for herbivores or
    carnivores, override the accessible property function to return False.
    """

    def __init__(self):
        """
        Constructor method. Identical to super class.
        """
        super().__init__()

    @property
    def accessible(self):
        """
        Override the accessible property as this type of landscape is not accessible for animals.

        :return: False
        :rtype: bool
        """
        return False
