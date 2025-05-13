# Mini Golf Game

This is a 2D golf game built with **Pygame** and **Open Sound Control (OSC)** integration. The game features a side-scrolling parallax background, interactive golf physics, and sensor-based club movement.

---

## 🛠️ Project Structure
```
parallax-golf-game/
├── launcher.py             # Main game loop and rendering logic
├── component/              # Folder containing classes for game components
│ ├── GolfBall.py           # Class for managing golf ball logic
│ ├── GolfClub.py           # Class for managing golf club logic
│ ├── Background.py         # Class for parallax background handling
│ └── Obstacles.py          # Class for managing obstacles and collision detection
├── handlers/               # Folder for OSC listener and gyroscope data handler
│ └── gyroscopeHandler.py   # OSC server and data handling
├── init.py                 # Game initialization logic and setup
├── README.md               # Project documentation (this file)
└──  docs/                   # Documentation folder (API docs, setup guide, etc.)
```

---

## 🚀 Getting Started

### Prerequisites - Python

- Python 3.8+ [Download Python](https://www.python.org/downloads/)
- pip (python package manager -> inclusive in Python 3.4+ from python.org)

### Prerequisites - OSC

### Game Installation - Local

1. **Clone the repository**
2. **Navigate to the git folder**
3. **Install necessary packages**
4. **Launch the game**

```bash
git clone https://github.com/awalerikesh/mini_golf.git
cd {path}/mini_golf
pip install -r requirements.txt
python laucher.py