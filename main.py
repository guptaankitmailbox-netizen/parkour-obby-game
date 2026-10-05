import pygame  # bring in the Pygame library

pygame.init()  # start up Pygame's internal systems

screen = pygame.display.set_mode((800, 600))  # create the game window (width, height)
pygame.display.set_caption("Obby Game")  # set the window title

# player's position and size (x, y, width, height)
player = pygame.Rect(100, 100, 40, 40)

running = True
while running:  # the game loop - repeats until we close the window
    for event in pygame.event.get():  # check for things like clicks, key presses
        if event.type == pygame.QUIT:  # if the X button was clicked
            running = False  # stop the loop
    
    screen.fill((30, 30, 30))  # clear screen each frame (dark gray background)
    pygame.draw.rect(screen, (0, 200, 0), player)  # draw player as a green square
    pygame.display.flip()  # show everything we just drew

pygame.quit()  # shut down Pygame cleanly


    
