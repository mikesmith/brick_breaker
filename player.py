import arcade

from constants import SCREEN_WIDTH, WALL_WIDTH


class Player(arcade.Sprite):

    def __init__(self, filename, scale):
        """Initialize the Player sprite."""
        super().__init__(filename, scale)

        self.center_x = SCREEN_WIDTH / 2
        self.center_y = 50

    def on_key_press(self, symbol: int, modifiers: int):
        """Handle user keyboard input.

        J/K: Move Left or Right
        Arrows: Move Left or Right

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.J or symbol == arcade.key.LEFT:
            self.change_x = -250

        if symbol == arcade.key.L or symbol == arcade.key.RIGHT:
            self.change_x = 250

    def on_key_release(self, symbol: int, modifiers: int):
        """Undo movement vectors when movement keys are released.

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if (
            symbol == arcade.key.J
            or symbol == arcade.key.L
            or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT
        ):
            self.change_x = 0

    def on_update(self, delta_time: float):
        self.center_x = self.center_x + self.change_x * delta_time
        self.center_y = self.center_y + self.change_y * delta_time

        # Keep Player in area
        if self.right > SCREEN_WIDTH - WALL_WIDTH:
            self.right = SCREEN_WIDTH - WALL_WIDTH

        if self.left < WALL_WIDTH:
            self.left = WALL_WIDTH
