## Term - Project :: Cannon - Brick game

import turtle as t, math as m, random as r      # Required Library

# Constants
scr = (1000, 800)
rho = 1.225  # air density [kg/m^3]
Cd = 0.47    # drag coefficient for sphere
radius = 0.2 # sphere radius [m]
density = 1000  # [kg/m^3]
gravity = 9.8  # gravity [m/s^2]

mass = (4/3) * m.pi * (radius**3) * density
area = m.pi * (radius**2)
drag_coefficient = 0.5 * rho * Cd * area

class Background(t.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.speed(0)
        self.draw_sky()
        self.draw_ground()

    def draw_sky(self):
        self.color("skyblue")
        self.penup()
        self.goto(-scr[0]//2, -scr[1]//2 + 100)
        self.pendown()
        self.begin_fill()
        for _ in range(2):
            self.forward(scr[0])
            self.left(90)
            self.forward(scr[1] - 100)
            self.left(90)
        self.end_fill()

    def draw_ground(self):
        self.color("green")
        self.penup()
        self.goto(-scr[0]//2, -300)
        self.pendown()
        self.begin_fill()
        for _ in range(2):
            self.forward(scr[0])
            self.right(90)
            self.forward(100)
            self.right(90)
        self.end_fill()

class Cannon(t.Turtle):
    def __init__(self, position):
        super().__init__()
        self.cannon_pos = position
        self.angle = 45
        self.ball_fired = False
        self.create_cannon()

        # 키보드 입력 설정
        screen.listen()
        screen.onkey(self.increase_angle, "Up")
        screen.onkey(self.decrease_angle, "Down")
        screen.onkey(self.fire, "space")

    def create_cannon(self):
        self.clear()
        self.penup()
        self.goto(self.cannon_pos[0], self.cannon_pos[1])
        self.setheading(0)

        # 대포 받침대
        self.color("gray")
        self.begin_fill()
        for _ in range(2):
            self.forward(20)
            self.left(90)
            self.forward(40)
            self.left(90)
        self.end_fill()

        # 대포 포신
        self.hideturtle()
        self.pendown()
        self.begin_fill()
        self.goto(self.cannon_pos[0]+10, self.cannon_pos[1]+40)
        self.setheading(self.angle-90)
        for _ in range(2):
            self.forward(10)
            self.left(90)
            self.forward(60) #포신 길이 60
            self.left(90)
            self.forward(10)
        self.end_fill()
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

        # 대포와 포신 사이 구
        self.penup()
        self.color("gray")
        self.goto(self.cannon_pos[0]+10, self.cannon_pos[1]+40)
        self.pendown()
        self.setheading(0)
        self.begin_fill()
        self.dot(50) #대포 원형 몸통

    def increase_angle(self):
        if self.angle < 80:
            self.angle += 5
        self.create_cannon()


    def decrease_angle(self):
        if self.angle > 10:
            self.angle -= 5
        self.create_cannon()

    def fire(self):
        if not self.ball_fired:
            self.ball_fired = True
            cannon_ball = CannonBall(self.angle, self.cannon_pos, game_manager)
            cannon_ball.launch()

    def reset_fire(self):
        self.ball_fired = False

class Brick(t.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.color("red")
        self.penup()
        self.goto(x, y)
        self.shape("square")
        self.shapesize(stretch_wid=2, stretch_len=4)
        self.visible = True

    def hide(self):
        self.visible = False
        self.hideturtle()

    def reset(self, x, y):
        self.visible = True
        self.goto(x, y)
        self.showturtle()

class CannonBall(t.Turtle):
    def __init__(self, angle, position, manager):
        super().__init__()
        self.v0 = 200
        self.angle = m.radians(angle)
        self.position = position
        self.manager = manager  
        self.speed_x = self.v0 * m.cos(self.angle)
        self.speed_y = self.v0 * m.sin(self.angle)
        self.x = position[0] + 10 + 60 * m.cos(self.angle)
        self.y = position[1] + 35 + 60 * m.sin(self.angle)
        self.physic = Physic()

        self.hideturtle()
        self.color("blue")
        self.penup()
        self.goto(self.x, self.y)
        self.dot(20)

    def launch(self):
        while True:
            self.clear()
            ax, ay = self.physic.get_acceleration(self.speed_x, self.speed_y)  # 가속도 계산
            self.manager.update_physics_display(ax, ay)  # 가속도 출력 업데이트
            self.speed_x, self.speed_y, self.x, self.y = self.physic.cal_pos(self.speed_x, self.speed_y, self.x, self.y)
            self.goto(self.x, self.y)
            self.dot(20)

            # 벽돌과 충돌 검사
            if self.manager.check_brick_collision(self):
                self.clear()
                cannon.reset_fire()
                break

            # 화면 바깥으로 나가거나 지면에 닿았을 때 멈춤
            if self.y <= -300 or self.x > scr[0]//2 or self.x < -scr[0]//2:
                self.clear()
                cannon.reset_fire()
                break
            screen.update()

    def check_collision(self, brick):
        # 벽돌의 중심 좌표와 크기
        brick_center_x, brick_center_y = brick.xcor(), brick.ycor()
        brick_half_width = 40
        brick_half_height = 20

        # 공의 중심 좌표와 반지름
        ball_x, ball_y = self.xcor(), self.ycor()
        ball_radius = 10

        # 충돌 여부 계산
        nearest_x = max(brick_center_x - brick_half_width, min(ball_x, brick_center_x + brick_half_width))
        nearest_y = max(brick_center_y - brick_half_height, min(ball_y, brick_center_y + brick_half_height))
        distance = m.sqrt((ball_x - nearest_x)**2 + (ball_y - nearest_y)**2)
        return distance <= ball_radius

class Physic:
    def __init__(self):
        self.dt = 0.01

    def get_acceleration(self, vx, vy):
        v = m.sqrt(vx**2 + vy**2)
        if v == 0:
            ax, ay = 0, -gravity
        else:
            ax = -(drag_coefficient * v * vx) / mass
            ay = -(drag_coefficient * v * vy) / mass - gravity
        return ax, ay

    def cal_pos(self, vx, vy, x, y):
        ax, ay = self.get_acceleration(vx, vy)
        vx += ax * self.dt
        vy += ay * self.dt
        x += vx * self.dt
        y += vy * self.dt
        return vx, vy, x, y

class Obstacle(t.Turtle):
    def __init__(self, x, y, range_y):
        super().__init__()
        self.penup()
        self.goto(x, y)
        self.color("brown")
        self.shape("square")
        self.shapesize(stretch_wid=6, stretch_len=1)  # 세로로 길게 설정
        self.speed(0)
        self.range_y = range_y
        self.direction = 1  # 1: 위로, -1: 아래로

    def move(self):
        new_y = self.ycor() + 5 * self.direction
        if new_y > self.range_y[1] or new_y < self.range_y[0]:
            self.direction *= -1  # 방향 전환
        self.goto(self.xcor(), new_y)
        screen.update()

    def hide(self):
        self.visible = False
        self.hideturtle()

    def check_collision(self, ball):
        # 장애물의 중심 좌표와 크기
        obstacle_center_x, obstacle_center_y = self.xcor(), self.ycor()
        obstacle_half_width = 10
        obstacle_half_height = 60

        # 공의 중심 좌표와 반지름
        ball_x, ball_y = ball.xcor(), ball.ycor()
        ball_radius = 10

        # 충돌 여부 계산
        nearest_x = max(obstacle_center_x - obstacle_half_width, min(ball_x, obstacle_center_x + obstacle_half_width))
        nearest_y = max(obstacle_center_y - obstacle_half_height, min(ball_y, obstacle_center_y + obstacle_half_height))
        distance = m.sqrt((ball_x - nearest_x)**2 + (ball_y - nearest_y)**2)
        return distance <= ball_radius

class GameManager:
    def __init__(self):
        self.score = 0
        self.bricks = []
        self.obstacles = []
        self.time_left = 60  # 게임 시간 60초
        self.create_bricks()
        self.create_obstacles()
        self.display_score()
        self.display_timer()
        self.display_physics()
        self.update_timer()
        self.move_obstacles()

    def create_obstacles(self):
        self.obstacles = []
        positions = [(-100, 0), (100, -100)]  # 장애물의 초기 위치
        for x, y in positions:
            self.obstacles.append(Obstacle(x, y, (-200, 200)))
        screen.update()

    def move_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.move()
        screen.ontimer(self.move_obstacles, 50)  # 50ms 간격으로 움직임

    def create_bricks(self):
        self.bricks = []
        positions = []
        while len(self.bricks) < 5:
            x = r.randint(200, scr[0]//2 - 50)
            y = r.randint(-250, -100)
            if not any(m.sqrt((x - bx)**2 + (y - by)**2) < 100 for bx, by in positions):
                positions.append((x, y))
                self.bricks.append(Brick(x, y))
        screen.update()

    def display_score(self):
        if hasattr(self, "score_display"):
            self.score_display.clear()
        else:
            self.score_display = t.Turtle()
            self.score_display.hideturtle()
            self.score_display.penup()
            self.score_display.goto(-scr[0]//2 + 50, scr[1]//2 - 50)
        self.score_display.write(f"Score: {self.score}", font=("Arial", 16, "bold"))

    def display_timer(self):
        if hasattr(self, "timer_display"):
            self.timer_display.clear()
        else:
            self.timer_display = t.Turtle()
            self.timer_display.hideturtle()
            self.timer_display.penup()
            self.timer_display.goto(scr[0]//2 - 150, scr[1]//2 - 50)
        self.timer_display.write(f"Time: {self.time_left}", font=("Arial", 16, "bold"))

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.display_timer()
            screen.ontimer(self.update_timer, 1000)
        else:
            self.end_game()

    def display_physics(self):
        if hasattr(self, "physics_display"):
            self.physics_display.clear()
        else:
            self.physics_display = t.Turtle()
            self.physics_display.hideturtle()
            self.physics_display.penup()
            self.physics_display.goto(-scr[0]//2 + 50, scr[1]//2 - 80)
        self.physics_display.write(f"Ax: 0.0, Ay: 0.0", font=("Arial", 16, "bold"))

    def update_physics_display(self, ax, ay):
        if hasattr(self, "physics_display"):
            self.physics_display.clear()
        self.physics_display.write(f"Ax: {ax:.2f}, Ay: {ay:.2f}", font=("Arial", 16, "bold"))

    def check_brick_collision(self, ball):
        for brick in self.bricks:
            if brick.visible and ball.check_collision(brick):
                brick.hide()
                screen.update()
                self.score += 10
                self.display_score()

                # 벽돌이 모두 사라지면 새로 생성
                if all(not brick.visible for brick in self.bricks):
                    self.create_bricks()
                return True

        # 장애물과의 충돌 검사
        for obstacle in self.obstacles:
            if obstacle.check_collision(ball):
                self.score -= 5
                self.display_score()
                return True
        return False

    def reset_bricks(self):
        self.create_bricks()

    def end_game(self):
        # 게임 종료 처리
        screen.clear()
        end_message = t.Turtle()
        end_message.hideturtle()
        end_message.penup()
        end_message.goto(0, 0)
        end_message.write(f"게임 종료!\n당신의 점수는: {self.score}", align="center", font=("Arial", 24, "bold"))
        screen.update()

# Main program
if __name__ == "__main__":
    screen = t.Screen()
    screen.setup(scr[0], scr[1])
    screen.title("Cannon Ball with Obstacles")
    screen.tracer(0)

    # Draw background
    background = Background()

    # Create cannon and game manager
    cannon = Cannon((-400, -300))
    game_manager = GameManager()

    screen.update()
    screen.mainloop()