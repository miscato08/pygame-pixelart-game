import pygame

# pygame setup
pygame.init()
screen_width, screen_height = 1024, 1024  # Set to your preferred starting size
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
dt = 0

# Load the original hero image
original_hero = pygame.image.load("main_char.png")

# Load and initially scale the background image
background = pygame.image.load("landscape2.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Starting position of the player
player_pos = pygame.Vector2(screen_width / 2, screen_height / 2)

# Jump variables
is_jumping = False
jump_height = 10
initial_jump_height = jump_height


# Define boundary limits
top_boundary = screen_height / 2.5
bottom_boundary = screen_height
left_boundary = 0
right_boundary = screen_width

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Update the screen size when the window is resized
            screen_width, screen_height = event.size
            screen = pygame.display.set_mode(
                (screen_width, screen_height), pygame.RESIZABLE
            )
            # Rescale the background to fit the new window size
            background = pygame.transform.scale(
                background, (screen_width, screen_height)
            )
            # Update boundary limits
            bottom_boundary = screen_height
            right_boundary = screen_width

    # Scale the hero image more dramatically based on its y-coordinate
    hero_scale_factor = (player_pos.y / screen_height) * 2.5  # Adjusted scale factor
    hero_base_size = 200  # Base size of the hero
    hero_size = (
        int(hero_base_size * hero_scale_factor),
        int(hero_base_size * hero_scale_factor),
    )
    hero = pygame.transform.scale(original_hero, hero_size)

    # Draw the scaled background image
    screen.blit(background, (0, 0))

    # Update player's position based on key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 125 * dt
    if keys[pygame.K_s]:
        player_pos.y += 125 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 125 * dt
    if keys[pygame.K_d]:
        player_pos.x += 125 * dt

    # Jumping logic
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
    else:
        # Implement the jump logic
        if jump_height >= -initial_jump_height:
            neg = 1
            if jump_height < 0:
                neg = -1
            player_pos.y -= (jump_height**2) * 0.5 * neg
            jump_height -= 1
        else:
            # Reset jump variables
            is_jumping = False
            jump_height = initial_jump_height

    # Prevent the hero from crossing the boundaries
    player_pos.x = max(left_boundary, min(player_pos.x, right_boundary - hero_size[0]))
    player_pos.y = max(top_boundary, min(player_pos.y, bottom_boundary - hero_size[1]))

    # Draw the scaled hero at the new position
    screen.blit(hero, player_pos)

    # Flip the display to put your work on screen
    pygame.display.flip()

    # Limit FPS to 60 and calculate delta time
    dt = clock.tick(60) / 1000

pygame.quit()
