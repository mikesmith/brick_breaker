import arcade


class Block(arcade.Sprite):

    BLOCK_WIDTH = 40

    def __init__(self, filename, scale, x, y):
        """Initialize the Block sprite."""
        super().__init__(filename, scale)

        self.center_x = x
        self.center_y = y

    def side_collision(self, ball):
        """Determine if ball is near the block's left or right sides.

        Arguments:
            ball {Ball} -- The ball sprite
        """
        if (ball.center_x >= self.right
           and ball.center_y >= self.bottom
           and ball.center_y <= self.top):
            return True
        elif (ball.center_x <= self.left
              and ball.center_y >= self.bottom
              and ball.center_y <= self.top):
            return True
        return False
