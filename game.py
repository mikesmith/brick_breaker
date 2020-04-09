import arcade
import random

from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,
                       SCALING, WALL_WIDTH)
from player import Player
from ball import Ball
from brick import Brick, BRICK_WIDTH, BRICK_HEIGHT
from power_up import PowerUp


class BrickBreaker(arcade.Window):

    def __init__(self, width, height, title):
        """Initialize the game."""
        super().__init__(width, height, title)

        # Initialize score
        self.score = 0
        self.lives = 2

    def setup(self, level):
        """Get the game ready to play."""
        arcade.set_background_color(arcade.color.GRAY)
        self.pause = False

        # Initialize level
        self.level = level

        # Initialize collision check counters
        # Prevents consecutive collisions within several frames between
        # player, ball and walls
        self.player_collision_counter = 0
        self.top_wall_collision_counter = 0
        self.side_wall_collision_counter = 0

        # Initialize power up counter
        self.pup_counter = 5

        # Initialize sprite lists
        self.side_wall_sprites = arcade.SpriteList()
        self.top_wall_sprites = arcade.SpriteList()
        self.bricks = arcade.SpriteList()
        self.extra_lives = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()
        self.power_ups = arcade.SpriteList()

        # Load sounds
        # Sound src: https://www.sounds-resource.com/nes/arkanoid/sound/3698/
        self.sbrick_sound = arcade.load_sound('sounds/sbrick_bounce.wav')
        self.brick_sound = arcade.load_sound('sounds/brick_bounce.wav')
        self.player_sound = arcade.load_sound('sounds/player_bounce.wav')

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

        # Set up the extra lives sprites
        for i in range(self.lives):
            life = arcade.Sprite('images/player_life.png', SCALING)
            life.bottom = 10
            life.left = WALL_WIDTH + (30 * i)
            self.extra_lives.append(life)
            self.all_sprites.append(life)

        # Retrieve the level pattern and build the current level
        self.build_level(self.get_level_map(self.level))

        # Set up the player
        self.player = Player('images/player.png', SCALING)
        self.all_sprites.append(self.player)

        # Set up the ball
        self.ball = Ball('images/ball.png', SCALING, self.player)
        self.all_sprites.append(self.ball)

    def get_level_map(self, level):
        """Retrieve the given level map from csv file.

        Arguments:
            level {int} -- The level ID to fetch

        Returns:
            map_array {[[str]]} -- A 2D array representing the brick pattern

        """
        filename = f'levels/level_{level}.csv'
        with open(filename) as map_file:
            map_array = []
            for line in map_file:
                line = line.strip()
                map_row = line.split(',')
                map_array.append(map_row)
        return map_array

    def build_level(self, map_array):
        """Build the brick pattern given a map array of the level.

        Arguments:
            map_array {[[str]]} -- A 2D array representing the brick pattern
        """
        for i, row in enumerate(map_array):
            for j, type in enumerate(row):
                if type != '-':
                    brick = Brick(int(type),
                                  SCALING,
                                  WALL_WIDTH + (BRICK_WIDTH * j),
                                  SCREEN_HEIGHT - 40 - (BRICK_HEIGHT * i))
                    self.bricks.append(brick)
                    self.all_sprites.append(brick)

    def on_key_press(self, symbol: int, modifiers: int):
        """Handle user keyboard input.

        Q: Quit the game
        P: Pause/Unpause the game
        Arrows: Move Left or Right
        Space: Shoot the ball from initial position

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
        Check ball collisions with bricks, walls, and player. Update
        ball vector on each collision. Remove bricks when collision
        detected with ball.

        Arguments:
            delta_time {float} -- Time since the last update
        """
        if self.pause:
            return

        # Decrement collision counters
        # Counters prevent consecutive bounces within 20 frames
        if self.player_collision_counter > 0:
            self.player_collision_counter -= 1

        if self.top_wall_collision_counter > 0:
            self.top_wall_collision_counter -= 1

        if self.side_wall_collision_counter > 0:
            self.side_wall_collision_counter -= 1

        self.player.on_update(delta_time)
        self.power_ups.on_update(delta_time)
        self.ball.on_update(delta_time)

        bricks = self.ball.collides_with_list(self.bricks)
        if bricks:
            # Limit to one brick collision at a time
            brick = bricks[0]
            self.ball.collides_with_brick(brick)

            brick.hit()
            if brick.type == 9 or brick.type == 8:
                arcade.play_sound(self.sbrick_sound)
            else:
                arcade.play_sound(self.brick_sound)

            # If brick reaches 0 hp, destroy brick and increase score
            if brick.hit_points == 0:
                self.score += Brick.clrs[brick.type][1]
                # If enough non-gold/silver bricks have been destroyed,
                # drop a power up
                if brick.type != 9 and brick.type != 8 and self.pup_counter == 0:
                    self.drop_power_up(brick)
                else:
                    self.pup_counter = self.pup_counter - 1
                brick.remove_from_sprite_lists()
                if self.level_completed():
                    self.setup(self.level + 1)

        if (self.ball.collides_with_list(self.side_wall_sprites)
                and self.side_wall_collision_counter == 0):
            self.ball.change_x = self.ball.change_x * -1
            self.side_wall_collision_counter = 20

        if (self.ball.collides_with_list(self.top_wall_sprites)
                and self.top_wall_collision_counter == 0):
            self.ball.change_y = self.ball.change_y * -1
            self.top_wall_collision_counter = 20

        if (self.ball.collides_with_sprite(self.player)
                and self.player_collision_counter == 0):
            self.player_collision_counter = 20
            self.ball.collides_with_player()
            arcade.play_sound(self.player_sound)

        pup = self.player.collides_with_list(self.power_ups)
        if pup:
            pup[0].remove_from_sprite_lists()
            pup[0].on_collide(self.player, self.ball)

        # If ball drops below player and screen, setup from beginning
        if self.ball.top <= 0:
            if len(self.extra_lives) == 0:
                print('Game Over')
                arcade.close_window()
            else:
                self.extra_lives.pop()
                self.ball.set_ball()

    def level_completed(self):
        """Check if the level has been completed.

        If the number of bricks is 0, the level has been completed. If the
        only remaining bricks are gold, the level is completed.

        Returns:
            bool -- True if level is completed. False otherwise.

        """
        if len(self.bricks) == 0:
            return True
        for brick in self.bricks:
            if brick.type != 9:
                return False
        return True

    def drop_power_up(self, brick):
        """Create a new random power up.

        The power up is created where the brick sprite was located. A new
        pup_counter value is randomly assigned for the next power up.

        Arguments:
            brick -- The brick the power up is spawning from.
        """
        new_pup = PowerUp(brick.center_x, brick.center_y)
        self.power_ups.append(new_pup)
        self.pup_counter = random.randrange(3, 8)

    def on_draw(self):
        """Draw all game objects."""
        arcade.start_render()  # Needs to be called before drawing
        self.top_wall_sprites.draw()
        self.side_wall_sprites.draw()
        self.extra_lives.draw()
        self.power_ups.draw()
        self.bricks.draw()
        self.player.draw()
        self.ball.draw()

        # Display score
        arcade.draw_text(f'Score: {self.score}',
                         50,
                         SCREEN_HEIGHT - 30,
                         arcade.color.BLACK,
                         12)

        # Display Level
        arcade.draw_text(f'Level: {self.level}',
                         SCREEN_WIDTH - 100,
                         SCREEN_HEIGHT - 30,
                         arcade.color.BLACK,
                         12)


if __name__ == "__main__":
    brick_breaker = BrickBreaker(
        int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), SCREEN_TITLE
    )
    brick_breaker.setup(level=1)
    arcade.run()
