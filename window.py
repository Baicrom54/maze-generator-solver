from tkinter import Tk, BOTH, Canvas
from basic_entities import Line,Point
import time
import random
class Window:
    def __init__(self,width,height):
        self._root=Tk()
        self._root.title="Maze Generator and Solver"
        self._canv=Canvas(self._root,width=width,height=height)
        self._canv.pack()
        self.is_running=False
        self._root.protocol("WM_DELETE_WINDOW", self.close)
        self._width=width
        self._height=height
    def redraw(self):
        self._root.update_idletasks()
        self._root.update()
    def draw_line(self,line,fill_color):
        line.draw(self._canv,fill_color)

    def wait_to_close(self):
        self.is_running=True
        while self.is_running:
            self.redraw()
    def close(self):
        self.is_running=False


class Cell:
    def __init__(self,t_left_P,b_right_P,win):
        self.right_wall=True
        self.left_wall=True
        self.top_wall=True
        self.bottom_wall=True
        self._t_left=t_left_P
        self._b_right=b_right_P
        self._win=win
        self.color="black"
        self.visited=False

    def draw(self):
        if self.right_wall:
            p1=Point(self._b_right.x,self._t_left.y)
            line=Line(self._b_right,p1)
            self._win.draw_line(line,self.color)

        if self.top_wall:
            p1=Point(self._b_right.x,self._t_left.y)
            line=Line(self._t_left,p1)
            self._win.draw_line(line,self.color)
        
        if self.left_wall:
            p1=Point(self._t_left.x,self._b_right.y)
            line=Line(self._t_left,p1)
            self._win.draw_line(line,self.color)
        
        if self.bottom_wall:
            p1=Point(self._t_left.x,self._b_right.y)
            line=Line(self._b_right,p1)
            self._win.draw_line(line,self.color)


    def draw_move(self,to_cell,undo=False):
        center1=Point((self._b_right.x+self._t_left.x)/2,(self._b_right.y+self._t_left.y)/2)
        center2=Point((to_cell._b_right.x+to_cell._t_left.x)/2,(to_cell._b_right.y+to_cell._t_left.y)/2)
        line=Line(center1,center2)
        if not undo:
            fill_color="red"
            self._win.draw_line(line,fill_color)
        else:
            fill_color="grey"
            self._win.draw_line(line,fill_color)



class Maze:
    def __init__(self,
            x_start,
            y_start,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win,
            seed=None,
        ):
        self._cells=[]
        self.num_rows=num_rows
        self.num_cols=num_cols
        self._win=win
        self._start=Point(x_start,y_start)
        self.cell_size_x=cell_size_x
        self.cell_size_y=cell_size_y
        if x_start+num_cols*cell_size_x>win._width or y_start+num_rows*cell_size_y>win._height:
            raise Exception("Maze too big for the given window")
        self.create_cells()
        self.create_entrance_exit()
        self._seed=None
        self.break_walls()

    

    def create_cells(self):
        for i in range(0,self.num_rows):
            row=[]
            for j in range(0,self.num_cols):
                b_right=Point(self._start.x+(j+1)*self.cell_size_x,self._start.y+(i+1)*self.cell_size_y)
                t_left=Point(self._start.x+j*self.cell_size_x,self._start.y+i*self.cell_size_y)
                cell=Cell(t_left,b_right,self._win)
                row.append(cell)
            self._cells.append(row)


    def draw_cells(self):
        for row in self._cells:
            for cell in row:
                cell.draw()
                self.animate()


    def animate(self):
        self._win.redraw()
        time.sleep(0.01)


    def create_entrance_exit(self):
        self._cells[0][0].left_wall=False
        self._cells[-1][-1].right_wall=False

    def break_walls(self,seed=None):
        if self._seed:
            random.seed(seed)
        self.break_walls_r(0,0)
        self.reset_visited()

    def reset_visited(self):
        for i in range(0,self.num_rows):
            for j in range(0,self.num_cols):
                self._cells[i][j].visited=False
    
    def break_walls_r(self,i,j):
        self._cells[i][j].visited=True
        if i==self.num_rows-1 and j==self.num_cols-1:
            return
        neighbours=[]
        if 0<i<self.num_rows-1:
            neighbours.extend([(self._cells[i-1][j],"top"),(self._cells[i+1][j],"bottom")])
        elif i==0:
            neighbours.append((self._cells[i+1][j],"bottom"))
        else:
            neighbours.append((self._cells[i-1][j],"top"))

        if 0<j<self.num_cols-1:
            neighbours.extend([(self._cells[i][j-1],"left"),(self._cells[i][j+1],"right")])
        elif j==0:
            neighbours.append((self._cells[i][j+1],"right"))
        else:
            neighbours.append((self._cells[i][j-1],"left"))
        random.shuffle(neighbours)
        for neighbour in neighbours:
            if not neighbour[0].visited:
                match neighbour[1]:
                    case "bottom":
                        self._cells[i][j].bottom_wall=False
                        neighbour[0].top_wall=False
                        self.break_walls_r(i+1,j)
                    case "top":
                        self._cells[i][j].top_wall=False
                        neighbour[0].bottom_wall=False
                        self.break_walls_r(i-1,j)
                    case "right":
                        self._cells[i][j].right_wall=False
                        neighbour[0].left_wall=False
                        self.break_walls_r(i,j+1)
                    case "left":
                        self._cells[i][j].left_wall=False
                        neighbour[0].right_wall=False
                        self.break_walls_r(i,j-1)

    def solve(self):
        flag=self.solve_r(0,0)
        return flag
    
    def solve_r(self,i,j):
        self.animate()
        self._cells[i][j].visited=True
        if i==self.num_rows-1 and j==self.num_cols-1:
            return True
        possible_moves=[]
        if not self._cells[i][j].right_wall and j+1<self.num_cols:
            possible_moves.append(("right",self._cells[i][j+1]))
        if not self._cells[i][j].left_wall and j-1>=0:
            possible_moves.append(("left",self._cells[i][j-1]))
        if not self._cells[i][j].top_wall and i-1>=0:
            possible_moves.append(("top",self._cells[i-1][j]))
        if not self._cells[i][j].bottom_wall and i+1<self.num_rows:
            possible_moves.append(("bottom",self._cells[i+1][j]))
        random.shuffle(possible_moves)
        if len(possible_moves)==0:
            return False
        for move in possible_moves:
            if not move[1].visited:
                match move[0]:
                    case "right":
                        self._cells[i][j].draw_move(move[1])
                        flag=self.solve_r(i,j+1)
                        if not flag:
                            self._cells[i][j].draw_move(move[1],undo=True)
                        else:
                            return True
                    case "left":
                        self._cells[i][j].draw_move(move[1])
                        flag=self.solve_r(i,j-1)
                        if not flag:
                            self._cells[i][j].draw_move(move[1],undo=True)
                        else:
                            return True
                    case "bottom":
                        self._cells[i][j].draw_move(move[1])
                        flag=self.solve_r(i+1,j)
                        if not flag:
                            self._cells[i][j].draw_move(move[1],undo=True)
                        else:
                            return True
                    case "top":
                        self._cells[i][j].draw_move(move[1])
                        flag=self.solve_r(i-1,j)
                        if not flag:
                            self._cells[i][j].draw_move(move[1],undo=True)
                        else:
                            return True
        return False




                    








        








