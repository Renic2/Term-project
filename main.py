## Term - Project :: Cannon - Brick game

import turtle as t, math as m, random as r      # Required Class


# Physic constant and initial value
rho = 1.225                                     # air density (kg/m^3)
Cd = 0.47                                       # sphere's drag force 
radius = 0.2                                    # given by professor (m)
density = 7800                                  # iron density (kg/m^3)
mass = (4/3*m.pi*(radius**3))*density     # m = radius * density
gravity = 9.8                                   # gravity acceleration (m/s^2)

area = m.pi * (radius**2)                       # cross-sectional area (m^2)
wind_drag = 0.5 * rho * Cd * area               # wind drag coefficient


# Coding constant
scr_wid = 1000
scr_hei = 800
cannon_pos = [-400,-300]

# Making Cannon 
class Cannon(t.Turtle):
    def __init__(self,position):  # Setting First
        super().__init__()
        self.hideturtle()
        self.cannon_circle(position)
        self.pedestal(position)
        
    def pedestal(self,position):
        self.penup()
        self.fillcolor("gray")
        self.pencolor("black")
        self.goto(position)
        self.pendown()
        self.setheading(0)
        self.begin_fill()
        for _ in range(2):
            self.forward(20)
            self.left(90)
            self.forward(40)
            self.left(90)
        self.end_fill()
    
    def cannon_circle(self,position):
        self.penup()
        self.color("gray")
        self.goto(position[0]+10, position[1]+40)
        self.pendown()
        self.setheading(0)
        self.begin_fill()
        self.dot(50)
        self.end_fill()

    def launcher(self,position,length,ang):
        self.color("gray")
        self.goto(position[0]+10, position[1]+40)
        if ang%360 < -33:
            ang = -32
        elif ang%360 > 213:
            ang = 212
        self.setheading(ang-90)
        self.begin_fill()
        for _ in range(2):
            self.forward(10)
            self.left(90)
            self.forward(length)
            self.left(90)
            self.forward(10)
        self.end_fill()
        self.pedestal(position)
        self.arrow(position,length,ang)

    def arrow(self,position,length,ang):
        self.penup()
        self.goto(position[0]+10, position[1]+40)
        self.setheading(ang)
        self.forward(length+10)
        self.pencolor("red")
        self.pensize(2)
        self.pendown()
        self.forward(20)
        self.left(135)
        self.forward(10)
        self.left(180)
        self.forward(10)
        self.right(90)
        self.forward(10)
        self.penup()
        self.pensize(1)


# Background
class Background(t.Turtle):
    def __init__(self):
        super().__init__()
        self.turtle1 = t.Turtle()
        self.turtle2 = t.Turtle()

        self.setting(self.turtle1,"green",200)
        self.setting(self.turtle2,"skyblue",800)

    def draw_back(self,turtle_obj,turtle_height):
        for _ in range(2):
            turtle_obj.forward(1000)
            if turtle_height == 800:
                turtle_obj.left(90)
            else:
                turtle_obj.right(90)
            turtle_obj.forward(turtle_height)
            if turtle_height == 800:
                turtle_obj.left(90)
            else:
                turtle_obj.right(90)

    def setting(self,turtle_obj,turtle_color,turtle_height):
        turtle_obj.hideturtle()
        turtle_obj.color(turtle_color)
        turtle_obj.speed(10)
        turtle_obj.penup()
        turtle_obj.goto(-500, -300)
        turtle_obj.pendown()
        turtle_obj.setheading(0)
        turtle_obj.begin_fill()
        self.draw_back(turtle_obj,turtle_height)
        turtle_obj.end_fill()


# Bricks
class Bricks(t.Turtle):
    def __init__(self,sx,sy):
        self.width = 30
        self.height = 10
        


# Screen Setting
screen = t.Screen()
screen.setup(scr_wid,scr_hei)
screen.title("Cannon - Brick")
screen.tracer(0)

Background()
cannon = Cannon(cannon_pos)
cannon.launcher(cannon_pos,60,30)

screen.update()