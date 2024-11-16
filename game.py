import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jumpy Dino Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

# Game clock
clock = pygame.time.Clock()

# Dinosaur class
class Dinosaur:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT - 100
        self.width = 50
        self.height = 50
        self.velocity = 12  # Adjusted dinosaur speed (slightly slower)
        self.jump = False
        self.jump_count = 10

    def move(self):
        if self.jump:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count ** 2) * 0.4 * neg
                self.jump_count -= 1
            else:
                self.jump = False
                self.jump_count = 10

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

# Cactus class
class Cactus:
    def __init__(self):
        self.x = WIDTH
        self.y = HEIGHT - 70
        self.width = 20
        self.height = 50
        self.velocity = 15  # Adjusted cactus speed (slightly faster)

    def move(self):
        self.x -= self.velocity

    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))

# Function to display messages
def display_message(text, font_size, color, y_offset=0):
    font = pygame.font.SysFont('Arial', font_size)
    message = font.render(text, True, color)
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2 + y_offset))
    pygame.display.update()

# Function to show start screen
def show_start_screen():
    screen.fill(WHITE)
    display_message("Jumpy Dino Game", 48, BLACK, -50)
    display_message("Press ENTER to Start", 36, BLACK, 50)

    pygame.display.update()

    # Wait for player to press ENTER to start
    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_start = False

# Main function
def game():
    dinosaur = Dinosaur()
    cactus_group = []
    run_game = True
    score = 0

    while run_game:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not dinosaur.jump:
                        dinosaur.jump = True

        # Add new cactus
        if random.randint(1, 80) == 1:  # Adjusted spawn rate (slightly slower)
            cactus_group.append(Cactus())

        # Move and draw cactus
        for cactus in cactus_group:
            cactus.move()
            cactus.draw(screen)
            # Remove cactus that goes off-screen
            if cactus.x < 0:
                cactus_group.remove(cactus)
                score += 1

            # Check for collision
            if (dinosaur.x + dinosaur.width > cactus.x and dinosaur.x < cactus.x + cactus.width) and \
               (dinosaur.y + dinosaur.height > cactus.y):
                run_game = False

        # Move and draw dinosaur
        dinosaur.move()
        dinosaur.draw(screen)

        # Display score
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (WIDTH - 150, 20))

        # Update display
        pygame.display.update()

        # Game speed (Moderate FPS)
        clock.tick(50)  # Adjusted FPS for moderate speed

    # Display Game Over message
    display_message("Game Over!", 48, BLACK)
    display_message(f"Score: {score}", 36, BLACK, 50)
    display_message("Press 'R' to Restart or 'Q' to Quit", 24, BLACK, 100)

    # Wait for player to either restart or quit
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    game()
                elif event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    show_start_screen()  # Show the start screen before the game
    game()  # Start the game after the user presses ENTER
