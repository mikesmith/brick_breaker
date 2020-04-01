import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, SCALING
from player import Player
from ball import Ball


class BlockBreaker(arcade.Window):

    def __init__(self, width, height, title):
        """Initialize the game."""
        super().__init__(width, height, title)

    def setup(self):
        """Get the game ready to play."""
        arcade.set_background_color(arcade.color.GRAY)
        self.pause = False

        # Initialize sprite lists
        self.side_wall_sprites = arcade.SpriteList()
        self.top_wall_sprites = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

        # Set up the walls
        for i in range(8):
            new_left_wall = arcade.Sprite('images/wall_left.png', SCALING)
            new_left_wall.left = 0
            new_left_wall.bottom = i * 100
            self.side_wall_sprites.append(new_left_wall)

            new_right_wall = arcade.Sprite('images/wall_right.png', SCALING)
            new_right_wall.right = SCREEN_WIDTH
            new_right_wall.bottom = i * 100
            self.side_wall_sprites.append(new_right_wall)

        for i in range(6):
            new_top_wall = arcade.Sprite('images/wall_top.png', SCALING)
            new_top_wall.top = SCREEN_HEIGHT
            new_top_wall.left = i * 100
            self.top_wall_sprites.append(new_top_wall)

        # Set up the player
        self.player = Player('images/player.png', SCALING)
        self.all_sprites.append(self.player)

        # Set up the ball
        self.ball = Ball('images/ball.png', SCALING)
        self.ball.bottom = self.player.top
        self.ball.center_x = self.player.center_x
        self.ball.stick(self.player)
        self.all_sprites.append(self.ball)

    def on_key_press(self, symbol: int, modifiers: int):
        """Handle user keyboard input.

        Q: Quit the game
        P: Pause/Unpause the game
        J/K: Move Left or Right
        Arrows: Move Left or Right

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.Q:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.P:
            self.pause = not self.pause

        if symbol == arcade.key.SPACE:
            # Shoot the ball!
            self.ball.shoot()

        self.player.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        """Undo movement vectors when movement keys are released.

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        self.player.on_key_release(symbol, modifiers)

    def on_update(self, delta_time: float):
        """Update the positions and statuses of all game objects.

        If paused, do nothing

        Arguments:
            delta_time {float} -- Time since the last update
        """
        if self.pause:
            return

        self.player.on_update(delta_time)
        self.ball.on_update(delta_time)

        if self.ball.collides_with_list(self.side_wall_sprites):
            self.ball.change_x = self.ball.change_x * -1

        if self.ball.collides_with_list(self.top_wall_sprites):
            self.ball.change_y = self.ball.change_y * -1

        if self.ball.collides_with_sprite(self.player):
            self.ball.change_y = self.ball.change_y * -1
            if self.ball.change_x == 0:
                self.ball.change_x = (self.ball.center_x - self.player.center_x) * 5

        if self.ball.top <= 0:
            self.setup()

    def on_draw(self):
        """Draw all game objects."""
        arcade.start_render()  # Needs to be called before drawing
        self.top_wall_sprites.draw()
        self.side_wall_sprites.draw()
        self.player.draw()
        self.ball.draw()


if __name__ == "__main__":
    block_breaker = BlockBreaker(
        int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), SCREEN_TITLE
    )
    block_breaker.setup()
    arcade.run()
