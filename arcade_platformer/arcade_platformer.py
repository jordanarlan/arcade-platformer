"""
Platformer Game
"""
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        #init timer for gui
        self.total_time = 0.0
        self.timer_text = arcade.Text(
            text="00:00:00",
            start_x= 0, #SCREEN_WIDTH // 2,
            start_y = SCREEN_HEIGHT,
            color=arcade.color.WHITE,
            font_size=25,
            anchor_x  = 'left', 
            anchor_y  = 'top',
        )

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None
        
        # physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None
        
        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        # Keep track of the score
        self.score = 0
        
        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        # Set up the timer
        self.total_time = 0.0
        
        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)    

        # Set up the GUI Camera
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Keep track of the score
        self.score = 0
        
        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        image_source = "assets/images/player/Cright.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[512, 96], [256, 96], [768, 96], [1000, 180]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png", TILE_SCALING
            )
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)
        
        # Use a loop to place some coins for our character to pick up
        for x in range(128, 1250, 256):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
            coin.center_x = x
            coin.center_y = 396
            self.scene.add_sprite("Coins", coin)
            
        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )
        
    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()
        
        # Activate our Camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()
        
        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw the timer text
        self.timer_text.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )
    
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)
    
    def on_update(self, delta_time):
        """Movement and game logic"""
        
        # Accumulate the total time
        self.total_time += delta_time

        # Calculate minutes
        minutes = int(self.total_time) // 60

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60

        # Calculate 100s of a second
        seconds_100s = int((self.total_time - seconds) * 100)

        # Use string formatting to create a new text string for our timer
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"

        # Move the player with the physics engine
        self.physics_engine.update()
        
        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add one to the score
            self.score += 1
            
        # Position the camera
        self.center_camera_to_player()

def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()