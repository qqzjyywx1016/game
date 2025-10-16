import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 定义常量
WIDTH = 720
HEIGHT = 480
GRID_SIZE = 20
SPEED = 8

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 初始化游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇")

# 游戏时钟
clock = pygame.time.Clock()

# 方向控制
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.body = [(WIDTH / 2, HEIGHT / 2)]  # 初始位置
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False

    def move(self):
        """控制蛇的移动"""
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = ((head_x + dx * GRID_SIZE) % WIDTH,
                    (head_y + dy * GRID_SIZE) % HEIGHT)

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_dir):
        """改变移动方向（禁止反向移动）"""
        if (new_dir[0] + self.direction[0], new_dir[1] + self.direction[1]) != (0, 0):
            self.direction = new_dir

    def check_collision(self):
        """检查自我碰撞"""
        return self.body[0] in self.body[1:]

    def draw(self):
        """绘制蛇"""
        for segment in self.body:
            pygame.draw.rect(screen, GREEN,
                             (segment[0], segment[1], GRID_SIZE - 1, GRID_SIZE - 1))


class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        """生成随机食物位置"""
        while True:
            x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
            y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
            if (x, y) not in snake.body:  # 确保不在蛇身上生成
                return (x, y)

    def draw(self):
        """绘制食物"""
        pygame.draw.rect(screen, RED,
                         (self.position[0], self.position[1], GRID_SIZE - 1, GRID_SIZE - 1))


# 游戏初始化
snake = Snake()
food = Food()
score = 0

# 游戏主循环
running = True
while running:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.change_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(RIGHT)

    # 游戏逻辑
    snake.move()

    # 碰撞检测
    if snake.body[0] == food.position:
        snake.grow = True
        food = Food()
        score += 1

    if snake.check_collision():
        running = False

    # 绘制画面
    screen.fill(BLACK)
    snake.draw()
    food.draw()

    # 显示分数
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(SPEED)

# 游戏结束
pygame.quit()
sys.exit()