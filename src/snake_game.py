"""Snake game using Pygame."""

import pygame
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
GRID_COLOR = (50, 50, 50)


class Direction(Enum):
    """Direction enum for snake movement."""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


@dataclass
class Position:
    """Position class for grid coordinates."""

    x: int
    y: int

    def __add__(self, other: Tuple[int, int]) -> "Position":
        """Add a direction tuple to the position."""
        return Position(self.x + other[0], self.y + other[1])

    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False


class Snake:
    """Snake class."""

    def __init__(self):
        """Initialize the snake."""
        self.body: List[Position] = [Position(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.grow_pending = False

    def move(self) -> None:
        """Move the snake in the current direction."""
        head = self.body[0]
        new_head = head + self.direction.value
        self.body.insert(0, new_head)

        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

    def grow(self) -> None:
        """Mark the snake to grow on next move."""
        self.grow_pending = True

    def check_collision(self) -> bool:
        """Check if snake collides with itself or walls."""
        head = self.body[0]

        # Check wall collision
        if head.x < 0 or head.x >= GRID_WIDTH or head.y < 0 or head.y >= GRID_HEIGHT:
            return True

        # Check self collision
        if head in self.body[1:]:
            return True

        return False

    def set_direction(self, direction: Direction) -> None:
        """Set the direction, preventing 180-degree turns."""
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }

        if direction != opposite_directions[self.direction]:
            self.direction = direction


class Food:
    """Food class."""

    def __init__(self):
        """Initialize food at a random position."""
        self.position = Position(
            random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
        )

    def respawn(self, snake_body: List[Position]) -> None:
        """Respawn food at a random position, avoiding snake body."""
        while True:
            self.position = Position(
                random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
            )
            # Only accept position if it's not on the snake's body
            if self.position not in snake_body:
                break


class Game:
    """Main game class."""

    def __init__(self):
        """Initialize the game."""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self) -> None:
        """Reset game state for a new game."""
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.food_eaten = 0
        self.level = 1
        self.running = True
        self.game_over = False

    def handle_events(self) -> None:
        """Handle game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    # Handle game over keys
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        self.running = False
                else:
                    # Handle game play keys
                    if event.key == pygame.K_UP:
                        self.snake.set_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.set_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.set_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.set_direction(Direction.RIGHT)

    def update(self) -> None:
        """Update game state."""
        if self.game_over:
            return

        self.snake.move()

        # Check if snake ate food
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food.respawn(self.snake.body)
            self.score += 10
            self.food_eaten += 1

            # Level up every 10 food eaten
            if self.food_eaten % 10 == 0:
                self.level += 1

        # Check collisions
        if self.snake.check_collision():
            self.game_over = True

    def draw(self) -> None:
        """Draw the game."""
        self.screen.fill(BLACK)

        # Draw grid
        self.draw_grid()

        # Draw snake
        for i, segment in enumerate(self.snake.body):
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(
                self.screen,
                color,
                (segment.x * GRID_SIZE, segment.y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1),
            )

        # Draw food
        pygame.draw.rect(
            self.screen,
            RED,
            (
                self.food.position.x * GRID_SIZE,
                self.food.position.y * GRID_SIZE,
                GRID_SIZE - 1,
                GRID_SIZE - 1,
            ),
        )

        # Draw score and level
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (WINDOW_WIDTH - 250, 10))

        # Draw game over screen if game is over
        if self.game_over:
            self.draw_game_over_overlay()

        pygame.display.flip()

    def draw_grid(self) -> None:
        """Draw the grid."""
        # Draw vertical lines
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT), 1)

        # Draw horizontal lines
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y), 1)

    def draw_game_over_overlay(self) -> None:
        """Draw semi-transparent game over overlay and options."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Game over text
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)

        game_over_text = font_large.render("Game Over!", True, RED)
        final_score_text = font_medium.render(f"Final Score: {self.score}", True, WHITE)
        final_level_text = font_medium.render(f"Level Reached: {self.level}", True, WHITE)
        restart_text = font_small.render("Press R to Restart or Q to Quit", True, WHITE)

        # Center text on screen
        self.screen.blit(
            game_over_text,
            (
                WINDOW_WIDTH // 2 - game_over_text.get_width() // 2,
                WINDOW_HEIGHT // 2 - 140,
            ),
        )
        self.screen.blit(
            final_score_text,
            (
                WINDOW_WIDTH // 2 - final_score_text.get_width() // 2,
                WINDOW_HEIGHT // 2 - 40,
            ),
        )
        self.screen.blit(
            final_level_text,
            (
                WINDOW_WIDTH // 2 - final_level_text.get_width() // 2,
                WINDOW_HEIGHT // 2 + 20,
            ),
        )
        self.screen.blit(
            restart_text,
            (
                WINDOW_WIDTH // 2 - restart_text.get_width() // 2,
                WINDOW_HEIGHT // 2 + 100,
            ),
        )

    def run(self) -> None:
        """Run the game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            # Increase speed with level: base FPS + level speed bonus
            current_fps = FPS + (self.level - 1)
            self.clock.tick(current_fps)

        pygame.quit()


def main():
    """Main function."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
