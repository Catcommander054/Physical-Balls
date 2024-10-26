import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1920, 1080
FPS = 60
GRAVITY = 9.81  #Притяжение
BALL_RADIUS = 15
BALL_COUNT = 200
CUBE_SIZE = 200  #Размер куба
REPELLING_FORCE = 250  #Сила отталкивания
ATTRACTION_FORCE = 500  #Сила притяжения
REPELLING_RADIUS = 200  #Радиус действия отталкивания
ATTRACTION_RADIUS = 200  #Радиус действия притяжения
FRICTION = 0.995  #Трение

BLUE = (0, 150, 150)
DARKGRAY = (20, 20, 20)
GREEN = (0, 255, 0)
GREY = (120, 120, 120)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = random.uniform(-100, 100)
        self.vx = random.uniform(-100, 100)
        self.radius = BALL_RADIUS

    def update(self, dt):
        self.vy += GRAVITY * dt
        self.y += self.vy * dt
        self.x += self.vx * dt

        self.vx *= FRICTION

        if self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy *= -0.7

        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -0.7
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx *= -0.7

        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= -0.7

        if abs(self.vx) < 1:
            self.vx = 0

    def draw(self, screen):
        for i in range(self.radius):
            color = (0, 150 - i * 2, 150 - i * 2)  #Градиент
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius - i)

    def attract_or_repel(self, mouse_pos, is_attracting):
        dx = self.x - mouse_pos[0]
        dy = self.y - mouse_pos[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance < ATTRACTION_RADIUS:
            if distance > 0:
                nx = dx / distance
                ny = dy / distance
                force = (REPELLING_FORCE if not is_attracting else -ATTRACTION_FORCE) / distance
                self.vx += nx * force
                self.vy += ny * force

        if distance < REPELLING_RADIUS:
            if distance > 0:
                nx = dx / distance
                ny = dy / distance
                force = REPELLING_FORCE / distance
                self.vx += nx * force
                self.vy += ny * force

    def check_collision(self, cube):
        cube_rect = pygame.Rect(cube.x - cube.size // 2, cube.y - cube.size // 2, cube.size, cube.size)
        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

        if ball_rect.colliderect(cube_rect):
            dx = self.x - cube.x
            dy = self.y - cube.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 0:
                nx = dx / distance
                ny = dy / distance

                self.vx += nx * 10000 / distance
                self.vy += ny * 10000 / distance

class Cube:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = CUBE_SIZE

    def draw(self, screen):
        for i in range(0, self.size // 2, 2):
            color = (GREY[0] - i * 0.5, GREY[1] - i * 0.5, GREY[2] - i * 0.5)
            pygame.draw.rect(screen, color, (self.x - self.size // 2 + i, self.y - self.size // 2 + i, self.size - i * 2, self.size - i * 2))

# Основная функция
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    balls = [Ball(WIDTH // 2, HEIGHT // 2) for _ in range(BALL_COUNT)]
    left_cube = Cube(150, HEIGHT // 2)
    right_cube = Cube(WIDTH - 150, HEIGHT // 2)
    center_cube = Cube(WIDTH // 2, HEIGHT // 4)

    running = True
    while running:
        dt = clock.tick(FPS) / 120.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_pos = pygame.mouse.get_pos()
        is_attracting = pygame.mouse.get_pressed()[0]

        for ball in balls:
            ball.attract_or_repel(mouse_pos, is_attracting)
            ball.update(dt)
            ball.check_collision(left_cube)
            ball.check_collision(right_cube)
            ball.check_collision(center_cube)

        screen.fill(DARKGRAY)
        for ball in balls:
            ball.draw(screen)

        left_cube.draw(screen)
        right_cube.draw(screen)
        center_cube.draw(screen)

        pygame.draw.circle(screen, GREEN, mouse_pos, 20)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
