from window import Window,Cell,Maze
from basic_entities import Point,Line
import sys


def main():
    sys.setrecursionlimit(10000)  # Or some larger number
    win=Window(800,800)
    maze=Maze(50,50,60,60,10,10,win)
    maze.draw_cells()
    flag=maze.solve()
    print(flag)
    win.wait_to_close()


if __name__=="__main__":
    main()