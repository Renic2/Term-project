## Term - Project :: Cannon - Brick game

import turtle as t, math as m, random as r      # Required Library

# Physic constant and initial value
rho = 1.225                                     # air density (kg/m^3)
Cd = 0.47                                       # sphere's drag force 
radius = 0.2                                    # given by professor (m)
density = 7800                                  # iron density (kg/m^3)
mass = (4/3*m.pi*(radius**3))*density           # m = radius * density
gravity = 9.8                                   # gravity acceleration (m/s^2)

area = m.pi * (radius**2)                       # cross-sectional area (m^2)
wind_drag = 0.5 * rho * Cd * area               # wind drag coefficient


# Coding constant
scr_wid = 1000
scr_hei = 800


# Physics
class Physic():
    def __init__(self):
        self.dt = 0.01

    def calculate_position(self, vx, vy, x,y):
        ax = - (wind_drag / mass) * vx
        ay = -gravity - (wind_drag / mass) * vy

        vx += ax * self.dt
        vy += ay * self.dt

        x += vx * self.dt
        y += vy * self.dt

        return vx, vy, x, y
    
    def crash(self,brick_coordinate):
        self.near_x = max(brick_coordinate[0] + Bricks.width/2,min(Cannon_ball.x, brick_coordinate[0] - Bricks.width/2))
        self.near_y = max(brick_coordinate[1] + Bricks.height/2,min(Cannon_ball.y, brick_coordinate[1] - Bricks.height/2))

        self.distance = m.sqrt((self.near_x - Cannon_ball.x)**2 + (self.near_y - Cannon_ball.y)**2)
        if self.distance <= radius:
            return False

        else:
            return True


# Making Cannon 
class Cannon(t.Turtle):
    def __init__(self):                         # Setting First
        super().__init__()
        self.hideturtle()
        self.cannon_pos = [-400,-300]           
        self.angle = 0

        screen.listen()
        screen.onkey(self.increase_angle, "Up")
        screen.onkey(self.decrease_angle, "Down")
        screen.onkey(self.fire, "space")
        
    def pedestal(self,position):
        self.penup()
        self.fillcolor("gray")
        self.pencolor("black")
        self.goto(position[0],position[1])
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

    def launcher(self,length=60):
        self.clear()
        self.cannon_circle(self.cannon_pos)
        self.color("gray")
        self.goto(self.cannon_pos[0]+10, self.cannon_pos[1]+40)
        if 270 < self.angle % 360 < 328:
            self.angle = 327
        elif 213 < self.angle % 360 < 270:
            self.angle = 212
        self.setheading(self.angle-90)
        self.begin_fill()
        for _ in range(2):
            self.forward(10)
            self.left(90)
            self.forward(length)
            self.left(90)
            self.forward(10)
        self.end_fill()
        self.pedestal(self.cannon_pos)
        self.arrow(self.cannon_pos,length,self.angle)

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

    def increase_angle(self):
        self.angle += 5
        self.launcher()
    
    def decrease_angle(self):
        self.angle -= 5
        self.launcher()

    def fire(self):
            ball = Cannon_ball()
            ball.launch()


# Cannon Ball
class Cannon_ball(t.Turtle):
    def __init__(self):
        super().__init__()
        self.position = cannon.cannon_pos
        self.shape("circle")
        self.color("red")
        self.penup()
        self.goto(self.position[0] + 10, self.position[1] + 40)
        self.vx = 100 * m.cos(m.radians(cannon.angle))
        self.vy = 100 * m.sin(m.radians(cannon.angle))
        self.physic = Physic()

    def launch(self):
        while True:
            self.vx, self.vy, self.x, self.y = self.physic.calculate_position(self.vx, self.vy, self.xcor(), self.ycor())
            self.goto(self.x, self.y)
            if self.ycor() <= -290:
                self.hideturtle()
                break
            screen.update()


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
    def __init__(self,brick):
        super().__init__()
        self.width = 80
        self.height = 40
        self.brickcor = brick
        self.hideturtle()
        self.penup()
        self.pencolor("black")
        self.fillcolor("gray")
        self.goto(self.brickcor[0]+self.width/2,self.brickcor[1]+self.height/2)
        self.begin_fill()
        self.setheading(180)
        self.pendown()
        for _ in range(2):
            self.forward(self.width)
            self.left(90)
            self.forward(self.height)
            self.left(90)
        self.end_fill()


# Screen Setting
screen = t.Screen()
screen.setup(scr_wid,scr_hei)
screen.title("Cannon - Brick")
screen.tracer(0)


# Game Start
Background()
cannon = Cannon()
cannon.launcher()
brick1 = Bricks([100,-280])                               #-280 is ground of brick

screen.mainloop()