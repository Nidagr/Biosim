# -*- encoding: utf-8 -*-
__author__ = "Nida Grønbekk and Yuliia Dzihora"
__email__ = 'nida.gronbekk@nmbu.no and yuliia.dzihora@nmbu.no'

from biosim.island import Island
import pytest
from biosim.landscape import Water, Lowland, Highland, Desert


class TestMakeMap:
    """
    This test class consists of tests for the make_map() function of the Island class.
    """

    def test_error_first_line_is_not_water(self):
        """
        On all edges of the map there should be water. Test if the expected ValueError is raised
        when one of the cells of the first row is not water. The test passes if the error is raised.

        :raises ValueError: The first row contains a Highland cell.
        """
        string = """\
                        WHWW
                        WLDW
                        WLDW
                        WWWW"""

        i = Island(string)
        with pytest.raises(ValueError):
            i.make_map()

    def test_error_last_line_is_not_water(self):
        """
        On all edges of the map there should be water. Test if the expected ValueError is raised
        when one of the cells of the last row is not water. The test passes if the error is raised.

        :raises ValueError: The last row contains a Lowland cell.
        """
        string = """\
                                WWWW
                                WLDW
                                WLDW
                                WLWW"""
        i = Island(string)
        with pytest.raises(ValueError):
            i.make_map()

    def test_error_sides_are_not_water(self):
        """
        On all edges of the map there should be water. Test if the expected ValueError is raised,
        when one of the cells on the left and right hand side is not water. The test passes if the
        error is raised.

        :raises ValueError: The left and right hand side contains a Lowland cell.
        """
        string = """\
                                        WWWW
                                        LLDW
                                        WLDL
                                        WWWW"""
        i = Island(string)
        with pytest.raises(ValueError):
            i.make_map()

    def test_error_row_len_is_same(self):
        """
        All of the rows in the island should have the same length, the map is rectangular. Test if
        the expected ValueError is raised when a row differs in length from the rest. The test
        passes when the error is raised.

        :raises ValueError: The first row has a different length than the rest.
        """
        string = """\
                                                WWW
                                                WLDW
                                                WLDW
                                                WWWW"""
        i = Island(string)
        with pytest.raises(ValueError):
            i.make_map()

    def test_error_valid_landscapes(self):
        """
        The make_map function accepts multi-line string input consisting of letters W, H, L and D.
        If a different letter than these four is found, the function should raise ValueError. After
        sending in a multi-line string with an invalid letter as input, the test passes if the
        error is raised.

        :raises ValueError: THe first row contains letter S.
        """
        string = """\
                                                WWWS
                                                WLDW
                                                WLDW
                                                WWWW"""
        i = Island(string)
        with pytest.raises(ValueError):
            i.make_map()

    def test_valid_landscapes(self):
        """
        When the make_map function iterates through the string input, it creates a 2D array of
        objects, where each object is of a landscape type according to the letter in the string, so
        if the letter is W - create a Water object at this spot in the array. Test that the objects
        at spot [row, cell] in the 2D array are of the correct type according to letters in the
        string input.
        """
        string = """\
                                                        WWWW
                                                        WLDW
                                                        WLHW
                                                        WWWW"""
        i = Island(string)
        i.make_map()
        assert type(i.object_map[0, 0]) == Water
        assert type(i.object_map[1, 1]) == Lowland
        assert type(i.object_map[2, 2]) == Highland
        assert type(i.object_map[1, 2]) == Desert

