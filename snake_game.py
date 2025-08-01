import pygame
import random
import numpy as np
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font(None, 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 200

class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake ML')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        # Place food randomly on the grid, but not on the snake
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        # If food spawned on snake, try again (recursive)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        
        # Handle pygame events smoothly
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Move the snake based on AI's decision
        self._move(action)
        self.snake.insert(0, self.head)  # Add new head

        # Check if game should end
        reward = 0
        game_over = False
        
        # Game ends if snake hits wall/itself OR takes too long
        # The 100*len(snake) prevents infinite loops
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10  # Big penalty for dying
            return reward, game_over, self.score

        # Check if snake ate food
        if self.head == self.food:
            self.score += 1
            reward = 10  # Reward for eating food
            self._place_food()
        else:
            # Remove tail if no food eaten (snake doesn't grow)
            self.snake.pop()

        # Update the visual display
        self._update_ui()
        self.clock.tick(SPEED)
        
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        # Check if point collides with walls or snake body
        if pt is None:
            pt = self.head
            
        # Hit boundary walls
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
            
        # Hit snake body (excluding head)
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        # Draw everything on screen
        self.display.fill(BLACK)

        # Draw snake - outer blue, inner lighter blue
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        # Draw food as red square
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # Show current score
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # Convert AI action to movement
        # action is [straight, right_turn, left_turn]
        
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # Keep going straight
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4  # Turn right
            new_dir = clock_wise[next_idx]
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4  # Turn left
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        # Update head position based on new direction
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)