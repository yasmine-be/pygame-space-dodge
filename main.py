import pygame
import time
import random

pygame.font.init()
pygame.init()

WIDTH, HEIGHT = 1000, 600
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 3

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("space Dodge")
bg = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))


def draw(player, elapsed_time, stars):
    screen.blit(bg, (0, 0))
    pygame.draw.rect(screen, (255, 0, 0), player)
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, (255, 255, 255))
    screen.blit(time_text, (10, 10))
    for star in stars:
        pygame.draw.rect(screen, "white", star)
    pygame.display.update()


def main():
    running = True

    player = pygame.Rect(500, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    start_time = time.time()
    elapsed_time = 0

    star_add = 2000
    star_count = 0

    stars = []
    hit = False

    clock = pygame.time.Clock()  

    while running:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star_y = -STAR_HEIGHT
                stars.append(pygame.Rect(star_x, star_y, STAR_WIDTH, STAR_HEIGHT))
            star_add = max(200, star_add - 50)
            star_count = 0

        for event in pygame.event.get():  # get events
            if event.type == pygame.QUIT:
                running = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + player.height <= HEIGHT:
            player.y += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL  
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You Lost!", True, "white")
            screen.blit(
                lost_text,
                (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2),
            )
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars)

    pygame.quit()


if __name__ == "__main__":
    main()
