import arcade

from constants import SCREEN_WIDTH, WALL_WIDTH
from power_up import PowerUpType

MOVEMENT_SPEED = 250


class Player(arcade.Sprite):
    LEFT = 1
    CENTER = 2
    RIGHT = 3

    current_power_up = None

    def __init__(self, filename, scale):
        """Initialize the Player sprite."""
        super().__init__(filename, scale)

        texture = arcade.load_texture('images/player_enlarged.png')
        self.append_texture(texture)

        self.center_x = SCREEN_WIDTH / 2
        self.center_y = 50

        self.break_out = False
        self.break_out_counter = 0

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False

    def on_key_press(self, symbol: int, modifiers: int):
        """Handle user keyboard input.

        Arrows: Move Left or Right

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.LEFT:
            self.left_pressed = True
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, symbol: int, modifiers: int):
        """Undo movement vectors when movement keys are released.

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.LEFT:
            self.left_pressed = False
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = False

    def on_update(self, delta_time: float):
        """Update the positions and statuses of the player object.

        Arguments:
            delta_time {float} -- Time since the last update
        """
        self.change_x = 0
        self.change_y = 0

        if self.left_pressed and not self.right_pressed:
            self.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.change_x = MOVEMENT_SPEED

        self.center_x = self.center_x + self.change_x * delta_time
        self.center_y = self.center_y + self.change_y * delta_time

        # Keep Player in area
        if self.right > SCREEN_WIDTH - WALL_WIDTH and not self.break_out:
            self.right = SCREEN_WIDTH - WALL_WIDTH

        if self.left < WALL_WIDTH:
            self.left = WALL_WIDTH

        if self.break_out and self.break_out_counter > 0:
            self.break_out_counter -= delta_time
        else:
            self.break_out = False

    def collision_location(self, ball):
        """Determine the location of where the ball collided with the player.

        Arguments:
             ball -- The ball game object
        """
        third = self.width / 3
        if ball.center_x > self.left and ball.center_x < self.left + third:
            return Player.LEFT
        elif ball.center_x < self.right and ball.center_x > self.right - third:
            return Player.RIGHT
        else:
            return Player.CENTER

    def clear_power_up(self):
        self.set_texture(0)
        self.current_power_up = None

    def set_power_up(self, pup):
        self.clear_power_up()
        if pup == PowerUpType.ENLARGE:
            self.set_texture(1)
        elif pup == PowerUpType.BREAK:
            self.break_out = True
            # Allow breakout to last 10 seconds
            self.break_out_counter = 10
