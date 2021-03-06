import arcade

from utils import Vector, reflect
from constants import SCALING
from player import Player
from power_up import PowerUpType

BALL_SPEED = 400


class Ball(arcade.Sprite):

    # Keep track of which object the ball is stuck to
    # stuck_on[0] = sprite
    # stuck_on[1] = location of ball on object relative to sprite.left
    stuck_on = (None, 0)

    current_power_up = None

    # Speed modifier to be decreased when a SLOW power up is picked up
    mod = 1.0

    def __init__(self, filename, scale, player, power_up=None):
        """Initialize the Ball sprite."""
        super().__init__(f'images/ball.png', scale)

        self.player = player
        if power_up is None:
            self.set_ball()

        # Initialize collision check counters
        # Prevents consecutive collisions within several frames between
        # player, ball and walls
        self.player_collision_counter = 0
        self.top_wall_collision_counter = 0
        self.side_wall_collision_counter = 0

    def copy(self):
        c_ball = Ball(f'images/ball',
                      SCALING,
                      self.player,
                      power_up=PowerUpType.DISRUPT)
        c_ball.center_x = self.center_x
        c_ball.center_y = self.center_y
        c_ball.change_x = self.change_x
        c_ball.change_y = self.change_y
        return c_ball

    def on_update(self, delta_time: float):
        """Update the positions and statuses of the ball game object.

        Arguments:
            delta_time {float} -- Time since the last update
        """
        # Follow object position if ball is stuck
        if self.stuck_on[0]:
            self.center_x = self.stuck_on[0].left + self.stuck_on[1]
        else:
            self.center_x = self.center_x + self.change_x * delta_time * self.mod
            self.center_y = self.center_y + self.change_y * delta_time * self.mod

        # Decrement collision counters
        # Counters prevent consecutive bounces within 20 frames
        if self.player_collision_counter > 0:
            self.player_collision_counter -= 1

        if self.top_wall_collision_counter > 0:
            self.top_wall_collision_counter -= 1

        if self.side_wall_collision_counter > 0:
            self.side_wall_collision_counter -= 1

    def collides_with_player(self):
        """Update the velocity when a collision with the player occurs."""
        if self.current_power_up == PowerUpType.CATCH:
            self.stick(self.player)
            self.bottom = self.player.top
        else:
            v = Vector(x=self.change_x, y=self.change_y)
            location = self.player.collision_location(self)
            normal = Vector(0, 1)

            # Determine where the ball collided to "enhance" angle of reflection
            if location == Player.LEFT:
                normal = Vector(0.196, -0.981)
            elif location == Player.RIGHT:
                normal = Vector(-0.196, -0.981)

            new_v = reflect(v, normal)
            self.change_x = new_v.x
            self.change_y = new_v.y

            # Increase the speed modifier on each collision when the
            # SLOW power up is picked up
            self.increase_speed_mod()

    def collides_with_brick(self, brick):
        """Update the velocity when a collision with a brick occurs."""
        if brick.side_collision(self):
            self.change_x = self.change_x * -1
        else:
            self.change_y = self.change_y * -1

        # Increase the speed modifier on each collision when the
        # SLOW power up is picked up
        self.increase_speed_mod()

    def set_ball(self):
        """Set the ball to the initial position on the player."""
        self.clear_power_up()
        self.mod = 1.0
        self.bottom = self.player.top
        self.center_x = self.player.center_x
        self.stick(self.player)

    def stick(self, sprite):
        """Set the ball to stick on a game object.

        Most likely this is the player game object.

        Arguments:
            sprite {arcade.Sprite} -- The sprite for the ball to stick to
        """
        diff = 0
        if sprite:
            diff = self.center_x - sprite.left
        self.stuck_on = (sprite, diff)

    def clear_power_up(self):
        self.current_power_up = None

    def set_power_up(self, pup):
        """Set the ball to have the SLOW power up.

        Can be cumulative if multiple slow power ups are picked up.
        """
        self.clear_power_up()
        if pup == PowerUpType.SLOW:
            self.current_power_up = PowerUpType.SLOW
            self.mod = self.mod * 0.5
        elif pup == PowerUpType.CATCH:
            self.current_power_up = PowerUpType.CATCH

    def increase_speed_mod(self, mod=0.05):
        """Increase the speed modifier.

        Increase the speed modifier as long as it is below 1.0.

        Arguments:
            mod {float} -- Increment to increase speed by.
        """
        self.mod = self.mod + mod
        if self.mod > 1.0:
            self.mod = 1.0

    def shoot(self):
        """Shoot the ball with it's initial velocity."""
        if self.stuck_on[0]:
            self.stick(None)
            self.change_y = BALL_SPEED
