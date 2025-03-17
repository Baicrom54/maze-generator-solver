import unittest
from window import Maze,Window

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 100
        num_rows = 100
        win=Window(900,900)
        m1 = Maze(50,50,num_rows, num_cols, 25,25,win)
        self.assertEqual(
            len(m1._cells),
            num_rows,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_cols,
        )


if __name__ == "__main__":
    unittest.main()

