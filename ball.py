import arcade


class Ball(arcade.Sprite):

    # Keep track of which object the ball is stuck to
    # stuck_on[0] = sprite
    # stuck_on[1] = location of ball on object relative to sprite.left
    stuck_on = (None, 0)

    def on_update(self, delta_time: float):
        # Follow object position if ball is stuck
        if self.stuck_on[0]:
            self.center_x = self.stuck_on[0].left + self.stuck_on[1]
        else:
            self.center_x = self.center_x + self.change_x * delta_time
            self.center_y = self.center_y + self.change_y * delta_time

    def stick(self, sprite):
        diff = 0
        if sprite:
            diff = self.center_x - sprite.left
        self.stuck_on = (sprite, diff)

    def shoot(self):
        self.stick(None)
        self.change_y = 300
