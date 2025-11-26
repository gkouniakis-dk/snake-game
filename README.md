# Snake Game

A classic Snake game built with Pygame featuring progressive difficulty levels, smooth controls, and a grid-based visual system.

## Features

- **Classic Gameplay** - Navigate your snake to eat food and grow longer
- **Progressive Difficulty** - Game speed increases every 10 food eaten
- **Level System** - Track your level as you progress
- **Grid Visualization** - Clear grid lines for easy navigation
- **Game Over Screen** - See your final score and level, with restart option
- **Responsive Controls** - Arrow keys for smooth snake movement

## Installation

### Quick Start - Windows Standalone (No Python Required)

Download and run the standalone executable:

1. Download `snake-game.exe` from the [Releases page](https://github.com/yourusername/snake-game/releases)
2. Double-click the file to launch the game
3. Play! No installation or Python needed.

### From Source

```bash
# Clone or download the repository
cd snake-game

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the package and dependencies
pip install -e .
```

### From PyPI (when published)

```bash
pip install snake-game
```

## Usage

### Run the Game

After installation, you can run the game in two ways:

**Option 1: Command line**
```bash
snake-game
```

**Option 2: Python module**
```bash
python -m src.snake_game
```

**Option 3: Direct execution**
```bash
python src/main.py
```

## Controls

- **Arrow Keys** - Move the snake (Up, Down, Left, Right)
- **R** - Restart the game (on Game Over screen)
- **Q** - Quit the game (on Game Over screen)
- **Close Window** - Exit the game

## Gameplay

1. The snake starts in the center of the grid moving right
2. Use arrow keys to change direction
3. Eat the red food squares to grow and increase your score
4. Each food eaten gives 10 points
5. Every 10 foods eaten, you level up and the game gets faster
6. Avoid hitting the walls or yourself
7. When you collide, the game ends and shows your final score and level

## Game Mechanics

- **Score** - +10 points per food eaten
- **Levels** - Increase every 10 foods eaten
- **Speed** - Increases by 1 FPS per level
- **Food Spawning** - Food never spawns on the snake's body

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── main.py              # Game entry point
│   └── snake_game.py        # Main game logic
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── setup.py                 # Package setup configuration
├── requirements.txt         # Development dependencies
├── README.md               # This file
└── .gitignore              # Git ignore rules
```

## Development

### Install in Development Mode

```bash
pip install -e .
```

### Run Tests

```bash
pytest tests/
```

### Run Linting

```bash
pip install pylint
pylint src/
```

### Building the Standalone Executable

To create a standalone Windows executable (.exe) that requires no Python installation:

```bash
# Install PyInstaller (if not already installed)
pip install pyinstaller

# Build the executable
pyinstaller snake_game.spec

# Output will be in the dist/ folder
```

The resulting `dist/snake-game.exe` can be distributed to Windows users.

## Distribution

### For Windows Users

Share the `snake-game.exe` file (12.77 MB) from the dist folder. Users can download and run it directly without any Python installation.

**Recommended distribution methods:**
- Upload to GitHub Releases for easy access
- Host on your website
- Share via cloud storage (Google Drive, Dropbox, etc.)

### For Developers/Contributors

Users can install from source following the "From Source" installation instructions above.

## Requirements

- Python 3.8+
- Pygame 2.5.0+

## License

MIT License - feel free to use and modify for your own projects!

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## Future Enhancements

Potential features for future versions:
- [ ] High score tracking/leaderboard
- [ ] Pause functionality
- [ ] Sound effects
- [ ] Different difficulty modes
- [ ] Power-ups
- [ ] Multiple game modes

