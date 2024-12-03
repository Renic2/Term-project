## Term - Project :: Cannon - Brick game

import turtle as t, math as m, random as r      # Required Library
import time

# Coding constant
scr = (1000,800)
screen = t.Screen()
screen.setup(scr[0],scr[1])
screen.title("Term-Project: Cannon-Brick")
screen.tracer(0)

# Physic constants
rho = 1.225    # air density [kg/m^3]
Cd = 0.47      # sphere's drag force
radius = 0.2   # sphere's radius [m]
density = 7800 # iron density [kg/m^3] / 대포의 구는 쇠공으로 가정한다.
gravity = 9.8  # Earth's gravity [m/s^2]

position = (0, 0, 0, 0)
# position = (vx, vy, x, y)
mass = (4/3*m.pi*(radius**3)*density)
# mass = radius * density
area = m.pi*(radius**2)
# cross-sectional area
wind_drag = 0.5*rho*Cd*area
# wind drag cofficient

''' 
Physic   -> 1. 속도, 위치 계산 후 출력 
            (Input: Ball(vx, vy, x, y), Output: Ball'(vx, vy, x, y))
            2. 공과 벽돌의 충돌 판정 
            (Input: Ball(x, y), Brick(x,y,wid,hei) Output: T/F)
'''

class Physic():
    def __init__(self):  # physic constant generate
        self.dt = 0.01  # delta t [s]

    def cal_pos(self, vx, vy, x, y):  # calculate position
        speed = m.sqrt(vx**2 + vy**2)  # 공의 속도 크기
        drag_force_x = -(wind_drag * speed * vx) / mass
        drag_force_y = -(wind_drag * speed * vy) / mass

        ax = drag_force_x  # x축 가속도 (공기저항 반영)
        ay = drag_force_y - gravity  # y축 가속도 (중력 및 공기저항 반영)

        vx += ax * self.dt
        vy += ay * self.dt

        x += vx * self.dt
        y += vy * self.dt

        self.position = (vx, vy, x, y)
        return self.position
        # 공 내부에 정보 저장과 동시에 값을 출력

    def crash_ball(self, ball_pos, brick_pos): # 충돌 판정
        self.near_x = max(brick_pos[0]+brick_pos[2]/2, min(ball_pos[0], brick_pos[0]-brick_pos[2]))
        self.near_y = max(brick_pos[1]+brick_pos[3]/2, min(ball_pos[1], brick_pos[1]-brick_pos[3]))
        # brick_pos = (x,y,width,height), ball_pos = (x,y)

        self.distance = m.sqrt((self.near_x - ball_pos[0])**2+(self.near_y - ball_pos[1])**2)
        # 공과 벽돌 사이의 거리를 공에 저장

        if self.distance <= self.radius:
            self.crash = True
        else:
            self.crash = False
        # 충돌 여부를 저장

'''
Cannon ->   대포 생성 (받침대, 포신)
            Input = Cannon_Position / Output = Graphics
            fire 명령 입력시 대포알 발사
'''

class Cannon(t.Turtle):
    def __init__(self, position): # 대포의 위치 지정
        super().__init__()
        self.cannon_pos = position # (x, y)
        self.angle = 0 # 초기 위치와 각도 설정

        screen.listen()
        screen.onkey(self.increase_angle, "Up")
        screen.onkey(self.decrease_angle, "Down")
        screen.onkey(self.fire, "space")

    def pedestal(self): # 받침대 생성
        self.hideturtle()
        self.penup()
        self.fillcolor("gray")
        self.pencolor("black")
        self.goto(self.cannon_pos[0],self.cannon_pos[1])
        self.pendown()
        self.setheading(0)
        self.begin_fill()
        for _ in range(2): #가로 20, 세로 40인 받침대 생성
            self.forward(20)
            self.left(90)
            self.forward(40)
            self.left(90)
        self.end_fill()
    
    def arrow(self): # 방향 표시
        self.hideturtle()
        self.penup()
        self.goto(self.cannon_pos[0]+10, self.cannon_pos[1]+40)
        self.setheading(self.angle)
        self.forward(70)
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

    def Cannon(self): # 대포 생성
        self.clear() # 화면 초기화 (대포)
        self.penup()
        self.color("gray")
        self.goto(self.cannon_pos[0]+10, self.cannon_pos[1]+40)
        self.pendown()
        self.setheading(0)
        self.begin_fill()
        self.dot(50) #대포 원형 몸통

        if 270 < self.angle % 360 < 328: #대포의 포신이 바닥에 닿지 않게함, 포신 생성
            self.angle = 327
        elif 213 < self.angle % 360 < 270:
            self.angle = 212

        self.setheading(self.angle-90)
        for _ in range(2):
            self.forward(10)
            self.left(90)
            self.forward(60) #포신 길이 60
            self.left(90)
            self.forward(10)
        self.end_fill()
        self.pedestal()
        self.arrow()

    def increase_angle(self):
        self.angle += 5
        self.Cannon()
    
    def decrease_angle(self):
        self.angle -= 5
        self.Cannon()

    def fire(self):
            ball = Cannon_ball()
            ball.launch()

'''
Cannon Ball  -> Cannon 클래스에서 fire를 통해 제어
                Ball을 생성하고, 위치를 옮김
'''

class Cannon_ball(t.Turtle):
    def __init__(self):
        super().__init__()
        self.v0 = 100  # initial velocity
        angle_rad = m.radians(cannon.angle)  # 각도를 라디안으로 변환
        self.location = (self.v0 * m.cos(angle_rad),
                         self.v0 * m.sin(angle_rad),
                         cannon.cannon_pos[0] + 10 + 60 * m.cos(angle_rad),
                         cannon.cannon_pos[1] + 40 + 60 * m.sin(angle_rad))
        # 위치 정보와 속도 정보 저장

        self.hideturtle()
        self.color("Blue")
        self.penup()
        self.goto(self.location[2], self.location[3])
        self.pendown()
        self.dot(20)  # 크기 20으로 설정
        self.physic = Physic()

    def launch(self):
        while True:
            self.clear()
            self.location = self.physic.cal_pos(self.location[0], 
                                                self.location[1], 
                                                self.xcor(), 
                                                self.ycor())
            self.goto(self.location[2], self.location[3])
            self.dot(20)
            
            # 화면 바깥으로 나가거나 땅에 닿았을 때 멈춤
            if self.ycor() <= -292 or self.xcor() > scr[0] // 2 or self.xcor() < -scr[0] // 2:
                time.sleep(0.2)
                self.clear()
                break

            screen.update()

# Background >> 개선 예정 
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

# Game Start
Background()
cannon = Cannon((-400,-300))
cannon.Cannon()

screen.mainloop()