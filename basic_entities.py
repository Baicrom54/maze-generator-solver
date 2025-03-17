from tkinter import Tk, BOTH, Canvas

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Line:
    def __init__(self,P1,P2):
        self.P1=P1
        self.P2=P2
    
    def draw(self,canvas,fill_color):
        canvas.create_line(self.P1.x,self.P1.y,self.P2.x,self.P2.y,fill=fill_color,width=2)