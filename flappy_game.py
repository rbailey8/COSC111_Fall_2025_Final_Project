import pygame
import random

from settings import *

def draw_window(window, bird_rect, top_pipe_rect, bottom_pipe_rect):
    """
   Refreshes the screen using the Painter's Algorithm.
    """
    #STEP 1: Fill the background
    window.fill(SKY_BLUE)

    #STEP 2: Draw the bird
    pygame.draw.rect(window, BIRD_COLOR, bird_rect)

    #STEP 3: Draw the pipes
    pygame.draw.rect(window, PIPE_COLOR, top_pipe_rect)
    pygame.draw.rect(window, PIPE_COLOR, bottom_pipe_rect)

    #STEP 4: Update the display
    pygame.display.update()

def get_random_height():
    """
   Returns a random integer between 50 and 400 for the top pipe height.
    """
    return random.randint(50, 400)

def check_game_over(bird_rect, top_pipe, bottom_pipe):
    """
   Returns True if the bird has crashed into a pipe or the floor/ceiling.
    """
    #1. Check if bird overlaps with top_pipe OR bottom_pipe
    if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
        return True

    #2. Check if bird went too high or too low
    # Remember: 0 is the top of the screen, HEIGHT is the bottom
    if bird_rect.top < 0 or bird_rect.bottom > HEIGHT:
        return True
    return False

def run_game_loop():
    #1. SETUP [cite: 127]
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Cube")
    clock = pygame.time.Clock()

    # Create the Rects
    #bird starts at x=50, y=300, with width/height of 30
    bird = pygame.Rect(50, 300, 30, 30)

    #Pipes start off-screen to the right
    pipe_x = WIDTH
    top_height = get_random_height()

    # Variables for movement
    bird_velocity = 0
    running = True

    #2. START THE LOOP [cite: 141]
    while running:
        clock.tick(60) # Lock the speed to 60 FPS

        # A. EVENT CHECKING (User Input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False

            #Check if Spacebar is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #Apply jump power (instant upward velocity)
                    bird_velocity = JUMP_POWER

        # B. GAME LOGIC (The Physics)
        
        #1. Apply Gravity: Add GRAVITY to bird_velocity
        bird_velocity += GRAVITY

        #2. Move Bird: Add bird_velocity to bird.y
        bird.y += int(bird_velocity)

        #3. Move Pipes: Subtract PIPE_SPEED from pipe_x
        pipe_x -= PIPE_SPEED

        #4. Recycle Pipes
        #If pipe goes off screen to the left
        if pipe_x < -50: 
           pipe_x = WIDTH # Reset to right side
           top_height = get_random_height() # Get new random height

        #5. Update Pipe Rects (We need new Rects because x moved!)
        top_pipe = pygame.Rect(pipe_x, 0, 50, top_height)
        #Bottom pipe y = top_height + gap
        bottom_pipe = pygame.Rect(pipe_x, top_height + PIPE_GAP, 50, HEIGHT) 

        #6. Check for Crash
        if check_game_over(bird, top_pipe, bottom_pipe):
           print("Game Over!")
           running = False

        #--- C. DRAWING ---
        draw_window(window, bird, top_pipe, bottom_pipe)

    pygame.quit()

#This line runs the game when you press Play
if __name__ == "__main__":
    run_game_loop()