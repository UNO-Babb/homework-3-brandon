from flask import Flask, render_template, redirect, url_for, request
import json
import random

app = Flask(__name__)

GAME_DATA_FILE = 'game_data.json'


def load_game_data():
    """Load game data from JSON file"""
    with open(GAME_DATA_FILE, 'r') as f:
        return json.load(f)


def save_game_data(data):
    """Save game data to JSON file"""
    with open(GAME_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


# Route for the homepage
@app.route('/')
def index():
    """Render the homepage with game data and board"""
    data = load_game_data()
    board_size = len(data['tiles'])  # Set board size based on the number of tiles
    return render_template('index.html', data=data, board_size=board_size)


# Route for rolling dice
@app.route('/roll_dice/<player>')
def roll_dice(player):
    """Roll dice and update player position"""
    data = load_game_data()
    roll1 = random.randint(1, 6)
    roll2 = random.randint(1, 6)
    move = roll1 + roll2

    # Update the player's position based on the dice roll
    new_position = (data['players'][player]['position'] + move) % len(data['tiles'])
    data['players'][player]['position'] = new_position

    # Save the updated data
    save_game_data(data)

    # Redirect to the homepage
    return redirect(url_for('index'))


# Route to reset the game
@app.route('/reset')
def reset_game():
    """Reset the game state"""
    data = load_game_data()
    for player in data['players']:
        data['players'][player]['position'] = 0
        data['players'][player]['score'] = 0
    save_game_data(data)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
