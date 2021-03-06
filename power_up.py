import arcade
import random
from enum import Enum

from constants import SCALING


class PowerUpType(Enum):
    CATCH = 'catch'
    SLOW = 'slow'
    ENLARGE = 'enlarge'
    EXTRA = 'player'
    DISRUPT = 'disruption'
    BREAK = 'break_out'
    LASER = 'laser'


class PowerUp(arcade.Sprite):

    def __init__(self, x, y):
        """Initialize the Brick sprite."""
        self.type = random.choice(list(PowerUpType))

        super().__init__(f'images/pup_{self.type.value}.png', SCALING)

        self.center_x = x
        self.center_y = y
        self.change_y = -150

    def on_update(self, delta_time: float):
        """Update the positions and statuses of the power up game object.

        Arguments:
            delta_time {float} -- Time since the last update
        """
        self.center_y = self.center_y + self.change_y * delta_time

    def on_collide(self, player, ball):
        """Apply power up effects to ball or player.

        Arguments:
            player -- The player game object
            ball -- The ball game object
        """
        player.clear_power_up()
        ball.clear_power_up()

        if (self.type == PowerUpType.CATCH
           or self.type == PowerUpType.SLOW):

            ball.set_power_up(self.type)
        elif (self.type == PowerUpType.ENLARGE):
            player.set_power_up(self.type)

        elif (self.type == PowerUpType.BREAK):
            player.set_power_up(self.type)

        elif (self.type == PowerUpType.LASER):
            player.set_power_up(self.type)
