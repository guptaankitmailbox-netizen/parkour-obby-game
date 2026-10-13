import pygame  # bring in the Pygame library

pygame.init()  # start up Pygame's internal systems

screen = pygame.display.set_mode((800, 600))  # create the game window (width, height)
pygame.display.set_caption("Obby Game")  # set the window title
clock = pygame.time.Clock()  # helps control game speed (frames per second)

# player's position and size (x, y, width, height)
player = pygame.Rect(100, 100, 40, 40)
speed = 5  # how many pixels the player moves per frame

velocity_y = 0  # vertical speed (how fast player is moving up/down)
gravity = 0.8  # how much velocity_y increases each frame (pulls player down)
jump_strength = -15  # negative = upward (pygame's y-axis goes down as positive)
on_ground = False  # tracks if player is touching the "floor"

# a list of platforms (x, y, width, height)
platforms = [
    pygame.Rect(0, 560, 800, 40),     # the floor
    pygame.Rect(200, 460, 150, 20),   # first step
    pygame.Rect(420, 380, 150, 20),   # second step
    pygame.Rect(620, 300, 150, 20),   # third step
]

running = True
while running:  # the game loop - repeats until we close the window
    for event in pygame.event.get():  # check for things like clicks, key presses
        if event.type == pygame.QUIT:  # if the X button was clicked
            running = False  # stop the loop

    keys = pygame.key.get_pressed()  # check which keys are currently held down
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_SPACE] and on_ground:
        velocity_y = jump_strength  # jump! only if standing on ground
        on_ground = False

    velocity_y += gravity  # gravity keeps pulling player down every frame
    player.y += int(velocity_y)  # apply vertical movement

    # check each platform to see if we landed on it
    on_ground = False
    for platform in platforms:
        if player.colliderect(platform) and velocity_y >= 0:
            player.bottom = platform.top  # sit on top of the platform
            velocity_y = 0
            on_ground = True
    
    screen.fill((30, 30, 30))  # clear screen each frame (dark gray background)
    pygame.draw.rect(screen, (0, 200, 0), player)  # draw player as a green square
    for platform in platforms:
        pygame.draw.rect(screen, (150, 150, 150), platform)  # draw platforms in gray
    pygame.display.flip()  # show everything we just drew

    clock.tick(60)  # limit the loop to 60 times per second

pygame.quit()  # shut down Pygame cleanly


    
