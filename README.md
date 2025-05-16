# Mini Golf Game

This is a 2D golf game built with **Pygame** and **Open Sound Control (OSC)** integration. The game features a side-scrolling parallax background, interactive golf physics, and sensor-based club movement.

---

## 🛠️ Project Structure
```
mini-golf-game/
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
└──  docs/                  # Documentation folder (API docs, setup guide, etc.)
```

---

## 🚀 Getting Started

### Prerequisites - Python

- Python 3.8+ [Download Python](https://www.python.org/downloads/)
- pip (python package manager -> inclusive in Python 3.4+ from python.org)

---

### Prerequisites - OSC

To enable gyroscope-based club control, this project uses **Open Sound Control (OSC)** data streamed from a mobile device using the **Sensors2OSC** app. You’ll need the following setup:

#### 🧭 Step 1: Install Sensors2OSC via F-Droid

The **Sensors2OSC** app is available on **F-Droid**, a trusted platform for open-source Android applications.

1. **Install F-Droid**  
   Visit [https://f-droid.org](https://f-droid.org) and download the latest F-Droid APK to your Android device.

2. **Open F-Droid** and search for:  
   `Sensors2OSC` or visit the [Sensors2OSC app page](https://f-droid.org/en/packages/org.sensors2osc/).

3. **Install Sensors2OSC** on your phone.

#### 📱 Step 2: Configure Sensors2OSC

Once installed:

1. Open the **Sensors2OSC** app.
2. Enable the **Gyroscope** sensor.
3. Under **Network Settings**, set the following:
   - **Target IP address**: `255.255.255.255`.
   - **Target Port**: `12345`.

> 💡 Make sure both your phone and computer are on the **same Wi-Fi network**.

#### 💻 Step 3: OSC Handler in the Game

The game runs an internal OSC server on your machine (using `python-osc`) that listens for incoming gyroscope values.

Relevant code is located in:

```python
handlers/
├── gyroscopeHandler.py     # Starts a threaded OSC server
```

---

### 🕹️ Game Installation – Local Setup

Follow these steps to set up and run the Mini Golf game locally:

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/awalerikesh/mini_golf.git
```

#### 2️⃣ Navigate to the Project Directory
```bash
cd mini_golf
```

#### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4️⃣ Launch the Game
```bash
python launcher.py
```