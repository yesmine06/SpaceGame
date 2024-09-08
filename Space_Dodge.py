import pygame
import time
import random

# Initialize Pygame
pygame.font.init()

# Set up display dimensions
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

# Load background image
BG = pygame.image.load("bg.jpeg")

# Set player dimensions
player_WIDTH = 40
player_HEIGHT = 60

# Player velocity
PLAYER_VEL = 5

# Star dimensions and velocity
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5

# Font for displaying the time
Font = pygame.font.SysFont("comicsans", 30)

# Function to draw elements on the window
def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))  # Place the background at the top-left corner
    
    # Display the elapsed time
    time_text = Font.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    
    # Draw the player (a red rectangle)
    pygame.draw.rect(WIN, "red", player)
    
    # Draw each falling star (yellow rectangles)
    for star in stars:
        pygame.draw.rect(WIN, "yellow", star)
    
    pygame.display.update()  # Update the display

# Main game loop
def main():
    run = True
    
    # Create a rectangle representing the player
    player = pygame.Rect(200, HEIGHT - player_HEIGHT, player_WIDTH, player_HEIGHT)
    
    clock = pygame.time.Clock()
    start_time = time.time()  # Initialize start time
    elapsed_time = 0
    
    star_add_increment = 2000  # Interval for adding stars
    star_count = 0
    stars = []
    
    hit = False  # Variable to check if the player is hit
    
    while run:
        # Control the speed of the game loop
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        
        # Add stars after certain time intervals
        if star_count > star_add_increment:
            for _ in range(3):  # Add 3 stars at once
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0
        
        # Check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player_WIDTH <= WIDTH:
            player.x += PLAYER_VEL
        
        # Move the stars down
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.colliderect(player):
                stars.remove(star)
                hit = True  # Player is hit
                break
        
        # If the player is hit, stop the game
        if hit:
            break
        
        # Draw the background, player, and stars
        draw(player, elapsed_time, stars)
    
    # End game message
    end_game_text = Font.render(f"You were hit! Time survived: {round(elapsed_time)}s", 1, "white")
    WIN.blit(end_game_text, (WIDTH//2 - end_game_text.get_width()//2, HEIGHT//2))
    pygame.display.update()
    pygame.time.delay(3000)  # Pause for 3 seconds before closing
    
    pygame.quit()

# Entry point of the program
if __name__ == "__main__":
    main()
