Brick Breaker is an Arkanoid / Breakout clone written in Python with the [Arcade library](https://arcade.academy/index.html).

![Brick Breaker](https://user-images.githubusercontent.com/46382795/78506436-5cf54400-772e-11ea-8ed6-fe231b509fcc.png)

### Installing
To get it up and running you will need to install [Arcade library](https://arcade.academy/index.html) and the PyObjC (for Mac) dependencies.

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install PyObjC arcade
```

### Run
```
$ python game.py
```

### Play
To start the game, press `Space` to release the ball towards the bricks. Use the `Left` and `Right` arrows to move the paddle to keep the ball in play as you try to destroy all the colored bricks.

Each brick is worth different amount of points. Silver (Gray) bricks take two hits to break. Gold bricks are indestructible.

You lose a life when the ball drops below the paddle. You start with three lives. The game ends when all lives are expended.

Three levels are implemented out of the [33 stages from the original Arkanoid](https://strategywiki.org/wiki/Arkanoid/Walkthrough). You can build your own levels by adding a `.csv` file to the `/levels` folder with the pattern of your choosing. The values for each brick can be found in `brick.py`.

The mechanics are based off information from [here](https://strategywiki.org/wiki/Arkanoid/Getting_Started).

#### Controls
```
Space: Release ball / Shoot lasers
Arrows (Left/Right): Move paddle left and right
P: Pause
Q: Quit
```

### Not implemented (...yet)

- Floating enemies
- Increase Silver brick point value by level
- Persisted High score
- Animations
- Remaining sounds
- Remaining levels 6-33

### Image and Sound Sources
**Image Assets**: Mike Smith using Aseprite

**Sound Assets**: [Sounds-Resource.com](https://www.sounds-resource.com/nes/arkanoid/sound/3698/)
