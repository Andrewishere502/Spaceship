import pygame

from space import Space


class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((width, height))

        pygame.display.set_caption('Spaceship')
        return

    def clear(self):
        self.win.fill((0, 0, 0))
        return

    def blit(self, surf, pos):
        self.win.blit(surf, pos)
        return


FPS = 60 # Maximum frames per second

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

pygame.init()
pygame.font.init()

# Create an instance of the clock class to help control maximum frame rate
clock = pygame.time.Clock()

display = Display(SCREEN_WIDTH, SCREEN_HEIGHT)
space = Space(SCREEN_WIDTH, SCREEN_HEIGHT)
space.reset_game()

pause = False
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                space.reset_game()
            elif event.key == pygame.K_p:
                if pause:
                    pause = False
                else:
                    pause = True
            elif event.key == pygame.K_e:
                space.spaceship.next_weapon()
            elif event.key == pygame.K_q:
                space.spaceship.prev_weapon()
            elif event.key == pygame.K_SPACE:
                if space.spaceship.is_alive:
                    space.spaceship_shoot()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if space.spaceship.is_alive:
                buttons_down = pygame.mouse.get_pressed()
                if buttons_down[0]:
                    space.spaceship_shoot()

    display.clear()
    if space.spaceship.is_alive:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:  # move spaceship up
            space.spaceship.accelerate((0, 0.3))
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  # move spaceship down
            space.spaceship.accelerate((0, -0.3))
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # move spaceship left
            space.spaceship.accelerate((-0.3, 0))
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # move spaceship right
            space.spaceship.accelerate((0.3, 0))
        
        if not pause:
            mouse_pos = pygame.mouse.get_pos()
            space.point_spaceship(mouse_pos)
            space.tick()

        space.clear()
        space.draw_all()

    display.blit(space, (0, 0))
    pygame.display.update()

    # Cap the frame rate to FPS frames per second. Frames can take longer
    # if the frame takes a long time to compute.
    clock.tick(FPS)
pygame.quit()
