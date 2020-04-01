import arcade

from constants import SCREEN_WIDTH, WALL_WIDTH, MOVEMENT_SPEED


class Player(arcade.Sprite):

    def __init__(self, filename, scale):
        """Initialize the Player sprite."""
        super().__init__(filename, scale)

        self.center_x = SCREEN_WIDTH / 2
        self.center_y = 50

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
        self.change_x = 0
        self.change_y = 0

        if self.left_pressed and not self.right_pressed:
            self.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.change_x = MOVEMENT_SPEED

        self.center_x = self.center_x + self.change_x * delta_time
        self.center_y = self.center_y + self.change_y * delta_time

        # Keep Player in area
        if self.right > SCREEN_WIDTH - WALL_WIDTH:
            self.right = SCREEN_WIDTH - WALL_WIDTH

        if self.left < WALL_WIDTH:
            self.left = WALL_WIDTH
