import arcade

BLOCK_WIDTH = 34
BLOCK_HEIGHT = 20


class Block(arcade.Sprite):

    clrs = [('white', 50),
            ('orange', 60),
            ('light_blue', 70),
            ('green', 80),
            ('red', 90),
            ('blue', 100),
            ('pink', 110),
            ('yellow', 120),
            ('silver', 50),
            ('gold', 0)]
    hit_points = 1

    def __init__(self, type, scale, x, y):
        """Initialize the Block sprite."""
        super().__init__(f'images/block_{self.clrs[type][0]}.png', scale)

        self.type = type
        self.left = x
        self.top = y

        if self.type == 8:
            texture = arcade.load_texture('images/block_silver_broken.png')
            self.append_texture(texture)
            self.hit_points = 2

    def side_collision(self, ball):
        """Determine if ball is near the block's left or right sides.

        Arguments:
            ball {Ball} -- The ball sprite

        Returns:
            bool -- True if the ball is near the sides of the brick. False
                    if the ball is near the top or bottome of the brick.

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

    def hit(self):
        """Reduce hit points of block by 1.

        A silver block will switch to a broken texture with 1 hit point left.
        A gold block cannot be damaged.
        """
        if self.type != 9:
            self.hit_points -= 1
        if self.type == 8 and self.hit_points <= 1:
            self.set_texture(1)
