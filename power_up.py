import arcade
import random
from enum import Enum

from constants import SCALING


class PowerUpType(Enum):
    CATCH = 'catch'
    SLOW = 'slow'


class PowerUp(arcade.Sprite):

    def __init__(self, x, y):
        """Initialize the Brick sprite."""
        self.type = random.choice(list(PowerUpType))
        print(self.type)

        super().__init__(f'images/pup_catch.png', SCALING)

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
        if self.type == PowerUpType.CATCH:
            ball.current_power_up = self.type
        elif self.type == PowerUpType.SLOW:
            print('Slow Power Up')
