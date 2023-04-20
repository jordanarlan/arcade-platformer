#This program defines the Score class, which loads, displays, and saves high scores using a JSON file. 
# The class has a constructor that takes two arguments, SCREEN_WIDTH and SCREEN_HEIGHT, 
# representing the game window's dimensions. It initializes several fields, 
# including the path to the JSON file, a dictionary to store the scores, and some index, count, and timer variables used later. 
# The load_score method reads the contents of the JSON file into the score_dict attribute. 
# If the player's score beats the current high score(s), it updates the dictionary, 
# removing the previous lowest one and adding the new one in the correct order. If a player scores the same value as an existing entry, it doesn't add it again. 
# The draw_score_screen method uses Arcade to draw a screen showing the ten highest scores, with the player's score highlighted if they made it onto the board. 
# The score_input method handles text input when the player enters their name for a new high score. 
# It updates the dictionary value for the current score with each character they enter and saves it to the JSON file once they have entered three characters.

import json
import arcade

class Score:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        # Initialize fields with default values
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.path = "arcade_platformer/score.json"
        self.score_dict = {}
        self.index = -1
        self.char_count = 0
        self.restart_timer = -1

    def load_score(self, player_score):
        # Load high scores from the JSON file
        with open(self.path) as file:
            self.score_dict = json.load(file)

        # Check if player has beaten a high score
        if (
            player_score > int(list(self.score_dict.keys())[-1])
            and str(player_score) not in self.score_dict
        ):
            # Add new high score to dictionary
            self.score_dict[str(player_score)] = "___"
            dum = [int(x) for x in list(self.score_dict.keys())]
            # Remove lowest score
            self.score_dict.pop(str(sorted(dum)[0]))

            # Reorder dictionary by score
            new_score = {}
            key_list = [int(x) for x in list(self.score_dict.keys())]
            for score in sorted(key_list, reverse=True):
                new_score[str(score)] = self.score_dict[str(score)]
            self.score_dict = new_score

            # Track index of new high score
            self.index = list(self.score_dict.keys()).index(str(player_score))
        else:
            self.restart_timer = 0

#The first method, draw_score_screen(), draws the high score screen in the game window using the arcade library. 
# It first draws the header text "- HIGH SCORE -" in bold red font. Then, for each key-value pair in the score_dict instance variable, it draws the score (key) and name (value) separated by a hyphen. 
# The current score being edited is highlighted with an asterisk, drawn in yellow font. 
# If the restart_timer instance variable is greater than or equal to 0 (meaning the game has ended), it also displays the text "Press a key to play again" in orange font.
    def draw_score_screen(self):
        # Draw high scores in Arcade window
        arcade.draw_text(
            "- HIGH SCORE -",
            self.width // 2 - 155,
            self.height - self.height // 10 - 10,
            arcade.color.RUBY_RED,
            40,
        )
        count = 1
        for value, item in self.score_dict.items():
            count += 1
            if count - 2 == self.index:
                arcade.draw_text(
                    f"* {value}  -   {item}",
                    self.width // 2 - 40 - 20 * len(value),
                    self.height - (self.height // 10) * count,
                    arcade.color.YELLOW,
                    30,
                )
            else:
                arcade.draw_text(
                    f" {value}  -   {item}",
                    self.width // 2 - 20 - 20 * len(value),
                    self.height - (self.height // 10) * count,
                    arcade.color.RED_DEVIL,
                    30,
                )
        if self.restart_timer >= 0:
            arcade.draw_text(
                "Press a key to play again",
                self.width // 2 - 185,
                self.height // 9,
                arcade.color.YELLOW_ORANGE,
                30,
            )
#score_input(char: str), handles user input for changing the names associated with scores. 
# It takes a char argument as a string (representing a single character) and returns a boolean. 
# If restart_timer is above 1.5 seconds, it returns True, indicating the game is still in progress and the score cannot be changed. 
# Otherwise, if a score is currently being edited (index is greater than or equal to 0), the character count is less than 3, and the char input is alphabetic, it updates the name associated with the current score to include the new character. 
# It then updates the dictionary to put the scores in descending order and stores it in the "score.json" file. It sets the restart_timer to 0, indicating the game is about to restart, and returns False. Otherwise, it just returns False.
    def score_input(self, char: str):
        if self.restart_timer > 1.5:
            return True
        elif self.index >= 0 and self.char_count < 3 and char.isalpha():

            score = list(self.score_dict.keys())[self.index]
            name = list(self.score_dict.values())[self.index]
            self.score_dict.pop(score)
            replace_name = list(name)
            replace_name[self.char_count] = char.upper()
            replace_name = "".join(replace_name)
            self.score_dict[score] = replace_name

            new_score = {}
            key_list = [int(x) for x in list(self.score_dict.keys())]
            for score in sorted(key_list, reverse=True):
                new_score[str(score)] = self.score_dict[str(score)]
            self.score_dict = new_score
            self.char_count += 1

            if self.char_count == 3:
                with open("score.json", "w") as file:
                    json.dump(self.score_dict, file)
                self.restart_timer = 0
            return False

        return False
