import os.path
import pygame
import random

pygame.init()

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUN_FRAMES = [pygame.image.load(os.path.join("Sprites/Gumbario/Run", "Run1.png")),
              pygame.image.load(os.path.join("Sprites/Gumbario/Run", "Run2.png")),
              pygame.image.load(os.path.join("Sprites/Gumbario/Run", "Run3.png"))]

JUMP_FRAMES = pygame.image.load(os.path.join("Sprites/Gumbario/Jump", "Jump1.png"))

CLOUD_FRAMES = [pygame.image.load(os.path.join("Sprites/Clouds", "Cloud1.png")),
                pygame.image.load(os.path.join("Sprites/Clouds", "Cloud2.png")),
                pygame.image.load(os.path.join("Sprites/Clouds", "Cloud3.png"))]

GUMBA_RUN_FRAMES = [pygame.image.load(os.path.join("Sprites/Gumba", "Gumba1.png")),
                    pygame.image.load(os.path.join("Sprites/Gumba", "Gumba2.png"))]

GUMBA_DEATH = pygame.image.load(os.path.join("Sprites/Gumba", "Gumba_death.png"))

# goomba

BACKGROUND = pygame.image.load('Sprites/Decorations/Background_full2.png')


class Player:
    x_pos = 100
    y_pos = 530
    JUMP_VEL = 8.5

    def __init__(self):
        self.run_textures = RUN_FRAMES
        self.jump_texture = JUMP_FRAMES

        self.is_jump = False
        self.is_run = True

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_textures[0]
        self.player_rect = self.image.get_rect()

        self.player_rect.x = self.x_pos
        self.player_rect.y = self.y_pos

        self.run_animation_speed = 20

    def update(self, input_keys):
        if self.is_run:
            self.run()
        if self.is_jump:
            self.jump()

        if self.step_index >= 150:
            self.step_index = 0

        if input_keys[pygame.K_w] and not self.is_jump:
            self.is_run = False
            self.is_jump = True
        elif not self.is_jump:
            self.is_run = True
            self.is_jump = False

    def run(self):
        self.image = self.run_textures[self.step_index // 50]
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.x_pos
        self.player_rect.y = self.y_pos
        self.step_index += self.run_animation_speed

    def jump(self):
        self.image = self.jump_texture
        if self.is_jump:
            self.player_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.is_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.player_rect.x, self.player_rect.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type  #
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class Goomba(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 500
        self.animation_index = 0
        self.is_dead = False

    def draw(self, SCREEN):
        if self.animation_index >= 9:
            self.animation_index = 0
        if self.is_dead:
            SCREEN.blit(self.image, self.rect)
        else:
            SCREEN.blit(self.image[self.animation_index // 5], self.rect)
        self.animation_index += 1

    def death(self):
        obstacles.pop()


class SmallObstacle(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super(SmallObstacle, self).__init__(image, self.type)
        self.rect.y = 500


class LargeObstacle(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super(LargeObstacle, self).__init__(image, self.type)
        self.rect.y = 480


class Cloud:
    def __init__(self):
        self.cloud_oscillation_down = 0
        self.cloud_oscillation_up = 0
        self.x = SCREEN_WIDTH + random.randint(500, 700)
        self.y = random.randint(50, 100)
        self.image = CLOUD_FRAMES[random.randint(0, 2)]
        self.width = self.image.get_width()

    def update(self):
        self.x -= 3
        if self.cloud_oscillation_down <= 30:
            self.y += 0.5
            self.cloud_oscillation_down += 0.5
        elif self.cloud_oscillation_up <= 30:
            self.y -= 0.5
            self.cloud_oscillation_up += 0.5
        else:
            self.cloud_oscillation_down = 0
            self.cloud_oscillation_up = 0

        if self.x < -self.width:
            self.image = CLOUD_FRAMES[random.randint(0, 2)]
            self.width = self.image.get_width()
            self.x = SCREEN_WIDTH + random.randint(500, 700)
            self.y = random.randint(0, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Player()
    cloud1 = Cloud()
    game_speed = 15
    x_pos_bg = 0
    y_pos_bg = 0
    points = 0
    font = pygame.font.Font('Sprites/fonts/cd2f1-36d91_sunday.ttf', 28)
    obstacles = []

    def score():
        global points, game_speed

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (980, 40)
        SCREEN.blit(text, text_rect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BACKGROUND.get_width()
        SCREEN.blit(BACKGROUND, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BACKGROUND, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BACKGROUND, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        input_keys = pygame.key.get_pressed()

        background()

        player.draw(SCREEN)
        player.update(input_keys)

        if len(obstacles) == 0:
            obstacles.append(Goomba(GUMBA_RUN_FRAMES))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.player_rect.colliderect(obstacle.rect):
                pygame.draw.rect(SCREEN, (255, 0, 0), player.player_rect, 2)
                obstacle.is_dead = True
                obstacle.image = GUMBA_DEATH
                points += 10
                # game_speed += 1
                # obstacle.death()

        cloud1.draw(SCREEN)
        cloud1.update()

        score()

        clock.tick(30)
        pygame.display.update()


main()
