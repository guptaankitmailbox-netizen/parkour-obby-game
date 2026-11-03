import pygame  # bring in the Pygame library

pygame.init()  # start up Pygame's internal systems

screen = pygame.display.set_mode((800, 600))  # create the game window (width, height)
pygame.display.set_caption("Obby Game")  # set the window title
clock = pygame.time.Clock()  # helps control game speed (frames per second)
font = pygame.font.SysFont(None, 36)  # a font for showing text on screen

# every tier is a dictionary describing one level.
# To make a new tier, you just add another dictionary to this list!
levels = [
    {
        "name": "Tier 1 - Easy",
        "spawn": (50, 500),
        "platforms": [
            pygame.Rect(0, 560, 250, 40),
            pygame.Rect(320, 560, 200, 40),
            pygame.Rect(590, 480, 210, 20),
        ],
        "moving_platforms": [],  # none in the easy tier
        "lava": [
            pygame.Rect(250, 580, 70, 20),
            pygame.Rect(520, 580, 70, 20),
        ],
        "checkpoints": [pygame.Rect(410, 520, 20, 40)],
        "goal": pygame.Rect(735, 420, 40, 60),
    },
    {
        "name": "Tier 2 - Normal",
        "spawn": (100, 500),
        "platforms": [
            pygame.Rect(0, 560, 300, 40),
            pygame.Rect(500, 560, 300, 40),
            pygame.Rect(200, 460, 150, 20),
            pygame.Rect(620, 300, 150, 20),
        ],
        "moving_platforms": [
            {"rect": pygame.Rect(420, 380, 100, 20), "speed": 2, "left": 400, "right": 660},
        ],
        "lava": [pygame.Rect(300, 580, 200, 20)],
        "checkpoints": [pygame.Rect(690, 260, 20, 40)],
        "goal": pygame.Rect(735, 240, 35, 60),
    },
    {
        "name": "Tier 3 - Hard",
        "spawn": (50, 500),
        "platforms": [
            pygame.Rect(0, 560, 120, 40),
            pygame.Rect(240, 500, 80, 20),
            pygame.Rect(600, 380, 70, 20),
            pygame.Rect(120, 260, 80, 20),
        ],
        "moving_platforms": [
            {"rect": pygame.Rect(380, 440, 70, 20), "speed": 3, "left": 360, "right": 520},
            {"rect": pygame.Rect(330, 320, 70, 20), "speed": -3, "left": 250, "right": 520},
        ],
        "lava": [pygame.Rect(120, 580, 680, 20)],
        "checkpoints": [pygame.Rect(625, 340, 20, 40)],
        "goal": pygame.Rect(150, 200, 35, 60),
    },
]

# player's position and size (x, y, width, height)
player = pygame.Rect(0, 0, 40, 40)
speed = 5  # how many pixels the player moves per frame

velocity_y = 0  # vertical speed (how fast player is moving up/down)
gravity = 0.8  # how much velocity_y increases each frame (pulls player down)
jump_strength = -15  # negative = upward (pygame's y-axis goes down as positive)
on_ground = False  # tracks if player is touching the "floor"
game_won = False  # becomes True after beating the last tier

def load_level(index):
    """NEW: set up the game using the data from levels[index]."""
    global level_index, spawn_x, spawn_y, velocity_y
    global platforms, moving_platforms, lava, checkpoints, goal

    level_index = index
    level = levels[index]

    spawn_x, spawn_y = level["spawn"]
    platforms = level["platforms"]
    lava = level["lava"]
    goal = level["goal"]

    # moving platforms and checkpoints change while playing, so we make
    # fresh copies - that way the original level data stays untouched
    moving_platforms = [{**mp, "rect": mp["rect"].copy()} for mp in level["moving_platforms"]]
    checkpoints = [{"rect": cp.copy(), "active": False} for cp in level["checkpoints"]]

    player.x, player.y = spawn_x, spawn_y
    velocity_y = 0

def respawn():
    """Put the player back at the start and stop any movement."""
    global velocity_y
    player.x, player.y = spawn_x, spawn_y
    velocity_y = 0

load_level(0)  # start on the first tier
# TIP: to test a harder tier quickly, change this 0 to 1 or 2!

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
         # is the player standing on top of this platform right now?
        standing_on_it = (
            player.bottom == mp["rect"].top
            and player.right > mp["rect"].left
            and player.left < mp["rect"].right
        )
        mp["rect"].x += mp["speed"]

        if standing_on_it:
            player.x += mp["speed"]  # carry the player along with it

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

     # check checkpoints - touching one saves it as your new spawn point
    for cp in checkpoints:
        if player.colliderect(cp["rect"]):
            cp["active"] = True  # remember it's been reached (changes its color)
            spawn_x, spawn_y = cp["rect"].x, cp["rect"].y  # update where we respawn

    # NEW: check the goal - load the next tier, or win if this was the last one
    if player.colliderect(goal):
        if level_index + 1 < len(levels):
            load_level(level_index + 1)
        else:
            game_won = True
    
    # check lava: touching it means respawn
    for brick in lava:
        if player.colliderect(brick):
            respawn()

    # also respawn if the player falls off the bottom of the screen
    if player.top > 600:
        respawn()
    
    screen.fill((30, 30, 30))  # clear screen each frame (dark gray background)
    for platform in platforms:
        pygame.draw.rect(screen, (150, 150, 150), platform)  # static    platforms in gray
    for mp in moving_platforms:
        pygame.draw.rect(screen, (100, 160, 255), mp["rect"])  # moving platforms in blue
    for brick in lava:
        pygame.draw.rect(screen, (220, 40, 40), brick)  # draw lava in red
    for cp in checkpoints:
        color = (80, 255, 120) if cp["active"] else (255, 220, 0)  # yellow while waiting, bright green once activated
        pygame.draw.rect(screen, color, cp["rect"])  # draw checkpoints
    pygame.draw.rect(screen, (255, 215, 0), goal)  # NEW: goal block in gold
    pygame.draw.rect(screen, (0, 200, 0), player)  # draw player as a green square

    # NEW: show the tier name (and a win message) as text
    screen.blit(font.render(levels[level_index]["name"], True, (255, 255, 255)), (10, 10))
    if game_won:
        screen.blit(font.render("You beat every tier!", True, (255, 215, 0)), (270, 280))

    pygame.display.flip()  # show everything we just drew
    clock.tick(60)  # limit the loop to 60 times per second

pygame.quit()  # shut down Pygame cleanly


    
