import pygame
import random
import time


# Initialize Pygame
pygame.init()
pygame.font.init()

# Define window dimensions
WIDTH, HEIGHT = 1100, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE WAR")

# Load and scale background image
BG = pygame.transform.scale(pygame.image.load("IMAGE.jpg"), (WIDTH, HEIGHT))

# Define player dimensions and velocity
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

# Initialize font
FONT = pygame.font.SysFont("comicsans", 50)

# Function to draw the game elements on the window
def draw(player, elapsed_time, stars, won):
    WIN.blit(BG, (0, 0))

    # Render and display the elapsed time
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    # Draw the player rectangle
    pygame.draw.rect(WIN, "yellow", player)

    for star in stars:
        pygame.draw.rect(WIN, "orange", star)
    
    # Check if player has won
    if won:
        win_text = FONT.render("YOU WON", 1, "green")
        WIN.blit(win_text, (WIDTH / 2 - win_text.get_width() / 2, HEIGHT / 2 - win_text.get_height() / 2))

    pygame.display.update()

# Main game loop
def main():
    run = True

    # Create the player rectangle
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False
    won = False

    while run:
        star_count += clock.tick(70)
        elapsed_time = time.time() - start_time
        if elapsed_time >= 100:
            won = True

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Key handling for player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("GAME OVER", 1, "red")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        # Draw the game elements
        draw(player, elapsed_time, stars, won)

        if won:
            pygame.time.delay(4000)
            break

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
