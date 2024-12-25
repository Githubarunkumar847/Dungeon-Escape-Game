from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Game state
game_state = {
    'level': 1,
    'health': 3,
    'maze': [],
    'player_pos': (0, 0),
    'exit_pos': (5, 5),
    'game_over': False
}

def generate_maze(level):
    """Generate a solvable 6x6 maze."""
    size = 6
    maze = [["." for _ in range(size)] for _ in range(size)]

    # Create a solvable path
    start_x, start_y = 0, 0
    exit_x, exit_y = size - 1, size - 1
    path = [(start_x, start_y)]

    while path[-1] != (exit_x, exit_y):
        x, y = path[-1]
        if x < exit_x and (x + 1, y) not in path:
            path.append((x + 1, y))
        elif y < exit_y:
            path.append((x, y + 1))
    
    for x, y in path:
        maze[x][y] = "."

    maze[start_x][start_y] = "P"
    maze[exit_x][exit_y] = "E"

    # Add walls
    wall_count = min(level * 4, size * size // 3)
    for _ in range(wall_count):
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        if maze[x][y] == "." and (x, y) not in path:
            maze[x][y] = "W"

    # Add traps
    trap_count = min(level * 2, size * size // 4)
    for _ in range(trap_count):
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        if maze[x][y] == "." and (x, y) not in path:
            maze[x][y] = "T"

    return maze, (start_x, start_y), (exit_x, exit_y)

@app.route('/')
def index():
    global game_state
    maze, player_pos, exit_pos = generate_maze(game_state['level'])
    game_state['maze'] = maze
    game_state['player_pos'] = player_pos
    game_state['exit_pos'] = exit_pos
    return render_template('index.html', maze=maze, level=game_state['level'], health=game_state['health'])

@app.route('/move', methods=['POST'])
def move():
    global game_state
    move = request.json.get('move')
    x, y = game_state['player_pos']
    moves = {'w': (-1, 0), 'a': (0, -1), 's': (1, 0), 'd': (0, 1)}

    if move in moves:
        dx, dy = moves[move]
        new_x, new_y = x + dx, y + dy

        if 0 <= new_x < 6 and 0 <= new_y < 6:
            cell = game_state['maze'][new_x][new_y]
            if cell == 'W':
                return jsonify(status="wall", comment="You hit a wall! Try a different direction.")
            elif cell == 'T':
                game_state['health'] -= 1
                if game_state['health'] <= 0:
                    game_state['game_over'] = True  # Set the game over flag here
                    return jsonify(status="game_over", comment="You stepped on too many traps. Game over!")
                return jsonify(status="continue", comment="Ouch! You stepped on a trap. Be careful.")
            elif cell == 'E':
                game_state['level'] += 1
                game_state['health'] = 3
                game_state['game_over'] = False  # Reset game over flag on level-up
                maze, player_pos, exit_pos = generate_maze(game_state['level'])
                game_state['maze'] = maze
                game_state['player_pos'] = player_pos
                game_state['exit_pos'] = exit_pos
                return jsonify(status="level_up", comment="Congratulations! You reached the exit. Level up!")

            # Update player position
            game_state['maze'][x][y] = '.'
            game_state['maze'][new_x][new_y] = 'P'
            game_state['player_pos'] = (new_x, new_y)

    return jsonify(status="continue", maze=game_state['maze'], health=game_state['health'], comment="Keep going!")

@app.route('/restart', methods=['POST'])
def restart():
    """Restart the current level."""
    global game_state
    maze, player_pos, exit_pos = generate_maze(game_state['level'])
    game_state['maze'] = maze
    game_state['player_pos'] = player_pos
    game_state['exit_pos'] = exit_pos
    game_state['health'] = 3
    return jsonify(status="restarted")

if __name__ == '__main__':
    app.run(debug=True)
