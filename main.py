import pygame  # bring in the Pygame library

pygame.init()  # start up Pygame's internal systems

screen = pygame.display.set_mode((800, 600))  # create the game window (width, height)
pygame.display.set_caption("Obby Game")  # set the window title
clock = pygame.time.Clock()  # helps control game speed (frames per second)

# where the player starts and respawns
spawn_x, spawn_y = 100, 500

# player's position and size (x, y, width, height)
player = pygame.Rect(spawn_x, spawn_y, 40, 40)
speed = 5  # how many pixels the player moves per frame

velocity_y = 0  # vertical speed (how fast player is moving up/down)
gravity = 0.8  # how much velocity_y increases each frame (pulls player down)
jump_strength = -15  # negative = upward (pygame's y-axis goes down as positive)
on_ground = False  # tracks if player is touching the "floor"

# static platforms (x, y, width, height)
platforms = [
    pygame.Rect(0, 560, 300, 40),     # floor, left part
    pygame.Rect(500, 560, 300, 40),   # floor, right part
    pygame.Rect(200, 460, 150, 20),   # first step
    pygame.Rect(620, 300, 150, 20),   # third step
]

# moving platforms: each one is a dictionary storing its shape + movement info
moving_platforms = [
    {"rect": pygame.Rect(420, 380, 100, 20), "speed": 2, "left": 400, "right": 660},
]

# kill bricks: touching these sends you back to spawn
lava = [
    pygame.Rect(300, 580, 200, 20),   # lava in the gap of the floor
]

def respawn():
    """Put the player back at the start and stop any movement."""
    global velocity_y
    player.x, player.y = spawn_x, spawn_y
    velocity_y = 0


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
    
    # move the moving platforms back and forth
    for mp in moving_platforms:
        standing_on_it = (
            player.bottom == mp["rect"].top
            and player.right > mp["rect"].left
            and player.left < mp["rect"].right
        )
        mp["rect"].x += mp["speed"]

        if standing_on_it:
            player.x += mp["speed"]  # NEW: carry the player along with it
            
        if mp["rect"].left < mp["left"] or mp["rect"].right > mp["right"]:
            mp["speed"] *= -1  # reverse direction at the edges

    # check each platform to see if we landed on it
    on_ground = False
    all_platforms = platforms + [mp["rect"] for mp in moving_platforms]
    for platform in all_platforms:
        if player.colliderect(platform) and velocity_y >= 0:
            player.bottom = platform.top  # sit on top of the platform
            velocity_y = 0
            on_ground = True

    # check lava: touching it means respawn
    for brick in lava:
        if player.colliderect(brick):
            respawn()

    # also respawn if the player falls off the bottom of the screen
    if player.top > 600:
        respawn()
    
    screen.fill((30, 30, 30))  # clear screen each frame (dark gray background)
    for platform in platforms:
        pygame.draw.rect(screen, (150, 150, 150), platform)  # draw platforms in gray
    for mp in moving_platforms:
        pygame.draw.rect(screen, (100, 160, 255), mp["rect"])  # moving platforms in blue
    for brick in lava:
        pygame.draw.rect(screen, (220, 40, 40), brick)  # draw lava in red
    pygame.draw.rect(screen, (0, 200, 0), player)  # draw player as a green square
    pygame.display.flip()  # show everything we just drew

    clock.tick(60)  # limit the loop to 60 times per second

pygame.quit()  # shut down Pygame cleanly


    
