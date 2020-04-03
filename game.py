import arcade

from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,
                       SCALING, WALL_WIDTH)
from player import Player
from ball import Ball
from block import Block


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
        self.blocks = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

        # Set up the walls
        for i in range(8):
            new_left_wall = arcade.Sprite('images/wall_left.png', SCALING)
            new_left_wall.left = 0
            new_left_wall.bottom = i * 100
            self.side_wall_sprites.append(new_left_wall)
            self.all_sprites.append(new_left_wall)

            new_right_wall = arcade.Sprite('images/wall_right.png', SCALING)
            new_right_wall.right = SCREEN_WIDTH
            new_right_wall.bottom = i * 100
            self.side_wall_sprites.append(new_right_wall)
            self.all_sprites.append(new_right_wall)

        for i in range(6):
            new_top_wall = arcade.Sprite('images/wall_top.png', SCALING)
            new_top_wall.top = SCREEN_HEIGHT
            new_top_wall.left = i * 100
            self.top_wall_sprites.append(new_top_wall)
            self.all_sprites.append(new_top_wall)

        self.build_level(self.get_level(1))

        # Set up the player
        self.player = Player('images/player.png', SCALING)
        self.all_sprites.append(self.player)

        # Set up the ball
        self.ball = Ball('images/ball.png', SCALING)
        self.ball.bottom = self.player.top
        self.ball.center_x = self.player.center_x
        self.ball.stick(self.player)
        self.all_sprites.append(self.ball)

    def get_level(self, level):
        filename = f'levels/level_{level}.csv'
        with open(filename) as map_file:
            map_array = []
            for line in map_file:
                line = line.strip()
                map_row = line.split(',')
                map_array.append(map_row)
        return map_array

    def build_level(self, map_array):
        for i, row in enumerate(map_array):
            for j, type in enumerate(row):
                if type != '-':
                    block = Block(int(type),
                                  SCALING,
                                  WALL_WIDTH + (Block.BLOCK_WIDTH * j),
                                  SCREEN_HEIGHT - 40 - (Block.BLOCK_HEIGHT * i))
                    self.blocks.append(block)
                    self.all_sprites.append(block)

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
        Check ball collisions with blocks, walls, and player. Update
        ball vector on each collision. Remove blocks when collision
        detected with ball.

        Arguments:
            delta_time {float} -- Time since the last update
        """
        if self.pause:
            return

        self.player.on_update(delta_time)
        self.ball.on_update(delta_time)

        # If ball collides with a block, determine if block was hit on side
        # or top/bottom. Remove block from sprite lists
        blocks = self.ball.collides_with_list(self.blocks)
        if blocks:
            if blocks[0].side_collision(self.ball):
                self.ball.change_x = self.ball.change_x * -1
            else:
                self.ball.change_y = self.ball.change_y * -1
            blocks[0].hit()
            if blocks[0].hit_points == 0:
                blocks[0].remove_from_sprite_lists()

        if self.ball.collides_with_list(self.side_wall_sprites):
            self.ball.change_x = self.ball.change_x * -1

        if self.ball.collides_with_list(self.top_wall_sprites):
            self.ball.change_y = self.ball.change_y * -1

        if self.ball.collides_with_sprite(self.player):
            self.ball.change_y = self.ball.change_y * -1
            # If ball is moving exactly 90 degrees to player, force angle
            # relative to center of player
            if self.ball.change_x == 0:
                collision_distance = self.ball.center_x - self.player.center_x
                self.ball.change_x = (collision_distance) * 5

        # If ball drops below player and screen, setup from beginning
        if self.ball.top <= 0:
            self.setup()

    def on_draw(self):
        """Draw all game objects."""
        arcade.start_render()  # Needs to be called before drawing
        self.top_wall_sprites.draw()
        self.side_wall_sprites.draw()
        self.blocks.draw()
        self.player.draw()
        self.ball.draw()


if __name__ == "__main__":
    block_breaker = BlockBreaker(
        int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), SCREEN_TITLE
    )
    block_breaker.setup()
    arcade.run()
