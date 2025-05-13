# Mini Golf Game

This is a 2D golf game built with **Pygame** and **Open Sound Control (OSC)** integration. The game features a side-scrolling parallax background, interactive golf physics, and sensor-based club movement.

---

## 🛠️ Project Structure
```
parallax-golf-game/
├── main.py # Main game loop and rendering
├── components.py # GolfBall, GolfClub, Background, Obstacles, etc.
├── handlers.py # OSC listener and gyroscope data handler
├── init.py # Game initialization logic
├── assets/ # Game assets (images, sounds, etc.)
├── README.md # Project documentation (this file)
```

## 🚀 Getting Started

### Prerequisites - Python

- Python 3.8+ [Download Python](https://www.python.org/downloads/)
- pip (python package manager -> inclusive in Python 3.4+ from python.org)

### Prerequisites - OSC

### Installation

1. **Clone the repository**
2. **Navigate to the git folder**
3. **Install necessary packages**
4. **Launch the game**

```bash
git clone https://github.com/awalerikesh/mini_golf.git
cd {path}/mini_golf
pip install -r requirements.txt
python laucher.py