# Pygame development
# Start the basic game setup
# Setup the display

# Load the pygame library
import pygame

# Size of the screen
SCREEN_TITLE = 'Crossy RPG'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
# Colors according to RGB codes
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (0, 0, 255)
# Clock used to update game events and frames
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)
pygame.mixer.init()

# Main game class
class Game:

    # Equivalent to FPS (typically 60)
    TICK_RATE = 60
    level_up = False
    game_level = 0
    
    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        # Create the window of specified size to display the game
        self.game_screen = pygame.display.set_mode((width, height))
        # Set the game window color to white
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)
        # Load the object image from the file directory
        background_image = pygame.image.load(image_path)
        # Scale the image up
        self.image = pygame.transform.scale(background_image, (width, height))
        pygame.mixer.music.load('assets\\background4.mp3')
        pygame.mixer.music.play()

    def run_game_loop(self):
        is_game_over = False
        did_win = False
        direction = 0

        player_character = PlayerCharacter('assets\\player.png', 375, 700, 50, 50)
        enemy_0 = EnemyCharacter('assets\\enemy.png', 20, 600, 50, 50)
        enemy_1 = EnemyCharacter('assets\\enemy.png', self.width - 50, 400, 50, 50)
        enemy_2 = EnemyCharacter('assets\\enemy.png', 20, 200, 50, 50)
        enemies = [enemy_0, enemy_1, enemy_2]
        treasure = GameObject('assets\\treasure.png', 375, 10, 50, 50)
        rate_of_change = 1
        if self.level_up:
            #print ('Level', self.game_level)
            for idx, enemy in enumerate(enemies):
                if idx == 1 and self.game_level < 3:
                    break
                if idx == 2 and self.game_level < 5:
                    break
                enemy.speed += self.game_level * rate_of_change
                print('Enemy #', idx, 'speed: ', enemy.speed)
            rate_of_change += 1
            self.level_up = False
            
        while not is_game_over:
            for event in pygame.event.get():
                # If we have a quit type event (exit out) then exit out of the game loop
                if event.type == pygame.QUIT:
                    is_game_over = True
                # Detect when key is pressed down
                elif event.type == pygame.KEYDOWN:
                    # Move up if up key pressed
                    if event.key == pygame.K_UP:
                        direction = 1
                    # Move down if down key pressed
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                # Detect when key is released
                elif event.type == pygame.KEYUP:
                    # Stop movement when key no longer pressed
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0
                
                #print(event)

            # Draw background image before drawing other sprites
            self.game_screen.blit(self.image, (0,0))

            # Draw the treasure
            treasure.draw(self.game_screen)
            
            # Move and draw the enemy images on top of the background
            for idx, enemy in enumerate(enemies):
                enemy.move(self.width)
                enemy.draw(self.game_screen)
                if idx == 0 and self.game_level < 3:
                    break
                elif idx == 1 and self.game_level < 5:
                    break
                
            # Move and draw the player image on top of the background
            player_character.move(direction, self.height, 50)
            player_character.draw(self.game_screen)

            for enemy in enemies:
                if player_character.detect_collision(enemy):
                    is_game_over = True
                    did_win = False
                    text = font.render('You suck! :(', True, RED_COLOR)
                    self.game_screen.blit(text, (275, 350))
                    pygame.display.update()
                    clock.tick(1)
                    break
            if player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                self.level_up = True
                self.game_level += 1
                text = font.render('You win! :)', True, GREEN_COLOR)
                self.game_screen.blit(text, (275, 350))
                pygame.display.update()
                clock.tick(1)
                break
            
            # Update all game graphics
            pygame.display.update() #.flip is similar to update
            # Tick the clock to update everything within the game
            clock.tick(self.TICK_RATE)
        if did_win:
            self.run_game_loop()
        else:
            return

# Generic game object class to be subclassed by other objects in the game
class GameObject:

    def __init__(self, image_path, x, y, width, height):
        
        # Load the object image from the file directory
        object_image = pygame.image.load(image_path)
        # Scale the image up
        self.image = pygame.transform.scale(object_image, (width, height))
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

# Class to represent the character controlled by the player
                        
class PlayerCharacter(GameObject):

    # How many tiles the character moves per second
    speed = 10
    
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    # Move function will move character up if direction > 0 and down if < 0        
    def move(self, direction, min_height, max_height):
        if direction > 0 and self.y_pos > max_height:
            self.y_pos -= self.speed
        elif direction < 0 and self.y_pos < min_height - 70:
            self.y_pos += self.speed

    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False
        return True


class EnemyCharacter(GameObject):

    # How many tiles the character moves per second
    speed = 10
    
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    # Move function will move enemy back and forth
    def move(self, max_width):
        if self.x_pos <= 20:
            self.speed = abs(self.speed)
        elif self.x_pos >= max_width - 70:
            self.speed = -abs(self.speed)
        self.x_pos += self.speed
        
# Initialize pygame
pygame.init()
background_image_path = '.\\assets\\background.png'
new_game = Game(background_image_path, SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop()

# Quite pygame and then the program
pygame.mixer.music.stop()
pygame.quit()
quit()













# Load the player image from the file directory
#player_image = pygame.image.load('.\\assets\player.png')
# Scale the image up
#player_image = pygame.transform.scale(player_image, (50, 50))

# Main game loop, used to update all gameplay such as movement, checks, and graphics
# Runs until is_game_over = True



