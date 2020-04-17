import arcade

from enum import Enum

from constants import SCALING


class Side(Enum):
    LEFT = 'left'
    RIGHT = 'right'


class Laser(arcade.Sprite):

    def __init__(self, side, player):
        """Initialize the Laser sprite."""
        super().__init__(f'images/laser.png', SCALING)

        self.bottom = player.bottom

        if side == Side.LEFT:
            self.center_x = player.left + player.width / 4
        elif side == Side.RIGHT:
            self.center_x = player.right - player.width / 4

        self.change_y = 300

    def on_update(self, delta_time: float):
        self.center_y = self.center_y + self.change_y * delta_time
