import unittest

from TicTacToe.model.grid_map import GridMap


class TestGridMap(unittest.TestCase):
    """
    Tests the class GridMap and its methods.
    """

    def setUp(self):
        self.width = 3
        self.height = 3
        self.grid = GridMap(self.width, self.height)
        self.grid.set_value_at(0, 0, 1)
        self.grid.set_value_at(0, 1, 2)
        self.grid.set_value_at(2, 2, 1)

    def test_set_value_at(self):
        """
        Tests the method set_value_at() in class GridMap.
        """
        self.grid.set_value_at(0, 0, 2)
        self.grid.set_value_at(0, 1, 1)
        self.grid.set_value_at(2, 2, 2)
        self.grid.set_value_at(0, 0, 3, check_empty=True)
        self.grid.set_value_at(-1, -1, 3, check_range=True)

        self.assertEquals(2, self.grid.grid[0][0])
        self.assertEquals(1, self.grid.grid[0][1])
        self.assertEquals(2, self.grid.grid[2][2])

    def test_get_value_at(self):
        """
        Tests the method get_value_at() in class GridMap.
        """
        self.assertEquals(1, self.grid.get_value_at(0, 0))
        self.assertEquals(2, self.grid.get_value_at(0, 1))
        self.assertEquals(1, self.grid.get_value_at(2, 2))
        self.assertEquals(0, self.grid.get_value_at(2, 0))
        self.assertIsNone(self.grid.get_value_at(-1, -1, check_range=True))

    def test_is_valid_at(self):
        """
        Tests the method is_valid_at() in class GridMap.
        """
        self.assertTrue(self.grid.is_valid_at(0, 0))
        self.assertTrue(self.grid.is_valid_at(0, 1))
        self.assertTrue(self.grid.is_valid_at(2, 0))
        self.assertTrue(self.grid.is_valid_at(2, 2))
        self.assertFalse(self.grid.is_valid_at(-1, -1))

    def test_is_empty_at(self):
        """
        Tests the method is_empty_at() in class GridMap.
        """
        self.assertFalse(self.grid.is_empty_at(0, 0))
        self.assertFalse(self.grid.is_empty_at(0, 1))
        self.assertFalse(self.grid.is_empty_at(2, 2))
        self.assertTrue(self.grid.is_empty_at(2, 0))
        self.assertIsNone(self.grid.is_empty_at(-1, -1, check_range=True))

    def test_is_full(self):
        """
        Tests the method is_full() in class GridMap.
        """
        # Make the grid full of entries
        self.grid.set_value_at(0, 2, 2)
        self.grid.set_value_at(1, 0, 1)
        self.grid.set_value_at(1, 1, 1)
        self.grid.set_value_at(1, 2, 1)
        self.grid.set_value_at(2, 0, 2)
        self.grid.set_value_at(2, 1, 2)
        self.assertTrue(self.grid.is_full())


if __name__ == '__main__':
    unittest.main()
