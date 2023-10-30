# -*- encoding: utf-8 -*-
__author__ = "Nida Grønbekk and Yuliia Dzihora"
__email__ = 'nida.gronbekk@nmbu.no and yuliia.dzihora@nmbu.no'

from .landscape import Landscape, Water, Lowland, Highland, Desert
import numpy as np
import textwrap


class Island:
    """
    Class representing the island on which the simulation will be performed. An island consists
    of cells. Each cell has a landscape type. It is possible to place animals in these cells later
    on (if the landscape type is accessible by animals).
    """

    def __init__(self, string_input):
        """
        The constructor method. Object map (which will represent the island in simulations)
        at the beginning is set to None, but later on is filled accordingly based on dimension and
        landscape types.

        :param string_input: A multi-line string consisting of letters H, L, W, D. Each newline in
        the string represents new row (y-coordinate) of island.
        :type string_input: str

        Every time we make an instance of the island we set row and col coordinate to be 0.
        """
        self.string_input = string_input
        self.object_map = None

        self.row = 0
        self.col = 0

    def make_map(self):
        """
        This function creates a two dimensional list of objects, where each object is a landscape
        type. Decide landscape type for each cell by iterating through our string_input and reading
        the letters.  {'W': Water, 'H': Highland, 'L': Lowland, 'D': Desert}. This list will
        represent the island.

        An island is supposed to have all the border cells of type Water, if not the value error
        will be raised. Since water is not accessible by the animals, it will help to make sure all
        animals stay in the island and do not escape the map. The map should be square or
        rectangular.

        :raises ValueError: The input string contains non-valid letters (no such landscape type
        exist), the rows of the string_input has different length (our map should be rectangular)
        or the edges of the island, (first row, last row, first and last element of each row) are
        not water.
        """
        self.string_input = textwrap.dedent(self.string_input)
        string_map = [list(i) for i in self.string_input.splitlines()]

        for char in string_map[0]:
            if char != 'W':
                raise ValueError('Edges should be of type water.')

        for char in string_map[-1]:
            if char != 'W':
                raise ValueError('Edges should be of type water.')

        for row in range(len(string_map[1:-1])):
            if string_map[row][0] != 'W' or string_map[row][-1] != 'W':
                raise ValueError('Edges should be of type water.')

        for row in string_map:
            if len(row) != len(string_map[0]):
                raise ValueError('All rows do not have the same length, '
                                 'island should be rectangular.')

        valid_letters = Landscape.valid_landscape_types
        self.object_map = np.array(string_map, dtype=object)
        landscapes = {'W': Water, 'D': Desert, 'H': Highland, 'L': Lowland}

        for row in range(self.object_map.shape[0]):
            for cell in range(self.object_map.shape[1]):

                if string_map[row][cell] not in valid_letters:
                    raise ValueError('No such landscape type exists.')
                self.object_map[row, cell] = landscapes[self.object_map[row, cell]]()

    def island_iterator(self):
        """
        Iterate through the cells of the island. Map has coordinates (0,0) in upper left corner when
        following logic of 2d arrays. Everytime while iterating through map, start with coordinates
        (0,0). Variables row and col help to keep track on where we are in the iteration.
        This iterator is useful in all functions in simulation file where we need to iterate through
        the island.
        """
        self.row = 0
        self.col = 0
        while True:
            yield self.object_map[self.row, self.col]
            self.col += 1
            if self.col >= len(self.object_map[0]):
                self.row += 1
                self.col = 0
            if self.row >= len(self.object_map.T[0]):
                return
