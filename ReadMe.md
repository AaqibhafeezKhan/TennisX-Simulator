# TennisX | The Python Driven Tennis Simulator

TennisX is a premium, web-based tennis simulator that uses **PyScript** (Python in the browser) to drive realistic match logic and scoring. It features a modern, neon-inspired look with glassmorphism aesthetics and advanced player attribute customization.

## Features
- **Realistic Game Engine**: Implemented in Python (`engine.py`), handling tie-breaks, serving rotations, and stamina-based success chances.
- **Player Customization**: Adjust Power, Agility, and Stamina for both players to see how they impact the match.
- **Dynamic Commentary**: Varied and context-aware match reporting for every point, error, and winner.
- **Critical Moment Alerts**: High-stakes indicators for Break Points, Set Points, and Match Points.
- **Match History**: Persistent storage of past match results using local storage.

## Getting Started
To run the simulator locally, simply start a web server in the project directory:

```bash
python -m http.server 8000
```

Then, open your browser and navigate to:
[http://localhost:8000/index.html](http://localhost:8000/index.html)

## Project Structure
- `index.html`: The main user interface and PyScript orchestration.
- `style.css`: Modern, responsive CSS design with glassmorphism and neon accents.
- `engine.py`: The core tennis logic engine.
- `README.md`: This documentation.

## Technologies Used
- **Python (PyScript)** for match logic.
- **HTML5/CSS3** for the UI.
- **Google Fonts** (Outfit, Space Grotesk).