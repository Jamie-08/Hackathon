import pygame
import sys
import random
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.SysFont(None, 36)
# clock = pygame.time.Clock()

# Defining the window we will display our game on (in terms of pixels)
pygame.display.set_caption('Light Game')
# pygame.display.set_text("hello")
SKY_BLUE = (105, 186, 255)
DARK_GREY = (72, 72, 72)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# ORB_BLUE = ()

NUMBER_OF_GRIDS = 20
GRID_SIZE = SCREEN_HEIGHT // NUMBER_OF_GRIDS

NUMBER_OF_BOXES_IN_CENTER = 4
CENTER_BOX_SIZE = NUMBER_OF_BOXES_IN_CENTER * GRID_SIZE

bad_tiles_min = (NUMBER_OF_GRIDS - NUMBER_OF_BOXES_IN_CENTER) / 2 - 2
bad_tiles_max = (NUMBER_OF_GRIDS + NUMBER_OF_BOXES_IN_CENTER) / 2

available_good_tiles = [(x, y) for x in range(NUMBER_OF_GRIDS) for y in range(NUMBER_OF_GRIDS)
						if (bad_tiles_min < x < bad_tiles_max and (y == bad_tiles_min or y == bad_tiles_max)) or
						((x == bad_tiles_min or x == bad_tiles_max) and bad_tiles_min < y < bad_tiles_max)]

DEFAULT_LIGHT_SIZE = (GRID_SIZE*2, GRID_SIZE*2)

orbs = [pygame.image.load(f'Light-game/sprites/{n+1}Orb.png') for n in range(11)]

orbs = [pygame.transform.scale(orb, DEFAULT_LIGHT_SIZE) for orb in orbs]

coin_image = pygame.image.load(f'Light-game/sprites/coin.png')
coin_image = pygame.transform.scale(coin_image, (GRID_SIZE*5, GRID_SIZE*5))

NUM_ORBS = len(orbs)
FPS = 650

frame = 0
frames_left = FPS * 30 # How many frames are left before game over

score = 0
top_score = 0

def draw_screen(orb_pos):
    """Draws the grid, marking squares white if visible from the orb, grey otherwise."""
    orb_center = (orb_pos[0] + 0.5) * GRID_SIZE, (orb_pos[1] + 0.5) * GRID_SIZE
    
    # Define the center blocking region
    center_x = (SCREEN_WIDTH - GRID_SIZE) // 2
    center_y = (SCREEN_HEIGHT - GRID_SIZE) // 2
    top_left_x = center_x - CENTER_BOX_SIZE // 2 + 0.5 * GRID_SIZE
    top_left_y = center_y - CENTER_BOX_SIZE // 2 + 0.5 * GRID_SIZE
    bottom_right_x = top_left_x + CENTER_BOX_SIZE
    bottom_right_y = top_left_y + CENTER_BOX_SIZE

    for x in range(NUMBER_OF_GRIDS):
        for y in range(NUMBER_OF_GRIDS):
            square_center = (x + 0.5) * GRID_SIZE, (y + 0.5) * GRID_SIZE
            if can_see(orb_center, square_center, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
                pygame.draw.rect(screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            else:
                pygame.draw.rect(screen, DARK_GREY, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    # Draw center blocking square
    pygame.draw.rect(screen, BLACK, (top_left_x, top_left_y, CENTER_BOX_SIZE, CENTER_BOX_SIZE))

def can_see(orb_center, square_center, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
    """Checks if the orb can see the center of a square, without passing through the blocking region."""
    x1, y1 = orb_center
    x2, y2 = square_center

    dx = x2 - x1
    dy = y2 - y1
    distance = math.hypot(dx, dy)

    steps = int(distance / GRID_SIZE * 2)  # Finer steps for accuracy
    for step in range(1, steps):
        px = x1 + dx * step / steps
        py = y1 + dy * step / steps

        # Check if this point falls inside the center blocking region
        if top_left_x <= px <= bottom_right_x and top_left_y <= py <= bottom_right_y:
            return False

    return True
	
def advance_timer():
	global top_score, frames_left

	frames_left -= 1
	timer_txt = font.render(f"Time left: {frames_left/FPS:.1f}s", True, (255, 255, 255))
	screen.blit(timer_txt, (10, 60))

	#Check if the timer has run out, meaning the game is over
	if frames_left <= 0:
		if score > top_score:
			top_score = score
		game_over_display()

def game_over_display():
	"""Displays game stats whenever time runs out"""
	global score

	screen.fill(SKY_BLUE)
	game_over_txt = font.render("Game Over", True, WHITE)
	score_txt = font.render(f"Your score was: {score}", True, WHITE)
	top_score_txt = font.render(f"The high score is: {top_score}",True,WHITE)
	restart_txt = font.render("Press R to restart, or Q to quit",True, WHITE)

	#Draw the above text onto the screens
	screen.blit(game_over_txt, (SCREEN_WIDTH // 2 - game_over_txt.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
	screen.blit(score_txt, (SCREEN_WIDTH // 2 - score_txt.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
	screen.blit(top_score_txt, (SCREEN_WIDTH // 2 - top_score_txt.get_width() // 2, SCREEN_HEIGHT // 2))
	screen.blit(restart_txt, (SCREEN_WIDTH // 2 - restart_txt.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
	pygame.display.update()

def closest(position, targets):
    smallest_dif = 100
    smallest_target = ()

    for target in targets:
        dist = (target[0] - position[0])**2 + (target[1] - position[1])**2
        if dist < smallest_dif:
            smallest_dif = dist
            smallest_target = target
    
    return smallest_target

def main_music():
    pygame.mixer.init()
    pygame.mixer.music.load('Light-game/sprites/Pure Darkness.mp3')
	
    pygame.mixer.music.play()

def coin_pos():
	ret =  (random.randint(1, NUMBER_OF_GRIDS-1), random.randint(1, NUMBER_OF_GRIDS-1))
	while bad_tiles_min < ret[0] < bad_tiles_max and bad_tiles_min < ret[1] < bad_tiles_max:
		ret = (random.randint(1, 19), random.randint(1, 19))
	
	return ret

def game_loop():
    coin = coin_pos()
    screen.fill(BLACK)
    orb_number = 0
    running = True

    # Character setup
    character_pos = [0, 0]  # Starting at the top-left corner
    
    # Load the character sprite (for the right-facing character)
    character_sprite = pygame.image.load("Light-game/sprites/Character Right.png")
    character_sprite = pygame.transform.scale(character_sprite, (GRID_SIZE, GRID_SIZE))  # Scale to grid size

    # Movement speed: the character will move one grid square per key press
    movement_speed = 1  # Move one grid square per press (1 means 1 square per press)

    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Get the keys currently pressed down
        keys = pygame.key.get_pressed()

        # Update character position based on keys
        if keys[pygame.K_w] and character_pos[1] > 0:  # Move up
            character_pos[1] -= movement_speed
        if keys[pygame.K_s] and character_pos[1] < NUMBER_OF_GRIDS - 1:  # Move down
            character_pos[1] += movement_speed
        if keys[pygame.K_a] and character_pos[0] > 0:  # Move left
            character_pos[0] -= movement_speed
        if keys[pygame.K_d] and character_pos[0] < NUMBER_OF_GRIDS - 1:  # Move right
            character_pos[0] += movement_speed

        # Prevent moving into the center blocking region
        if (
            bad_tiles_min < character_pos[0] < bad_tiles_max
            and bad_tiles_min < character_pos[1] < bad_tiles_max
        ):
            character_pos = closest(character_pos, available_good_tiles)

        # Get orb position based on mouse
        mx, my = pygame.mouse.get_pos()
        mx, my = mx // GRID_SIZE, my // GRID_SIZE

        if mx == GRID_SIZE - 1:
            mx -= 1
        if my == GRID_SIZE - 1:
            my -= 1

        # Avoid the center blocking region for the orb
        if bad_tiles_min < mx < bad_tiles_max and bad_tiles_min < my < bad_tiles_max:
            mx, my = closest((mx, my), available_good_tiles)

        # Clear the screen
        screen.fill(DARK_GREY)

        # Draw the grid and center blocking region
        draw_screen((mx, my))

        # Draw the orb
        screen.blit(orbs[round(orb_number % (NUM_ORBS - 1))], (mx * GRID_SIZE, my * GRID_SIZE))

        # Draw the character sprite (locked to grid)
        screen.blit(
            character_sprite,
            (character_pos[0] * GRID_SIZE, character_pos[1] * GRID_SIZE),
        )

        # Draw the coin
        screen.blit(coin_image, (coin[0] * GRID_SIZE, coin[1] * GRID_SIZE))

        # Update timer and screen
        advance_timer()
        pygame.display.flip()

        # Update orb animation frame
        orb_number += 1 / FPS * 3






#--------------------------------------------------#
#--------------------------------------------------#
#--------------------------------------------------#

# BUTTONS
# pygame.display.set_caption("Button!")
# main_font = pygame.font.SysFont("cambria", 50)

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

button_surface = pygame.image.load("Light-game/sprites/grey box.png")
button_surface = pygame.transform.scale(button_surface, (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

button = Button(button_surface, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), "Button", font, WHITE, BLACK)
pygame.display.set_caption("Menu")

BG = pygame.image.load("Light-game/sprites/Black.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Light-game/sprites/font.ttf", size)
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(0,0), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(SCREEN_HEIGHT//15).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*0.1))

        PLAY_BUTTON = Button(image=button_surface, pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT*0.4), 
                            text_input="PLAY", font=get_font(SCREEN_HEIGHT//20), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=button_surface, pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT*0.6), 
                            text_input="OPTIONS", font=get_font(SCREEN_HEIGHT//20), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=button_surface, pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT*0.8), 
                            text_input="QUIT", font=get_font(SCREEN_HEIGHT//20), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_music()
                    game_loop()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()