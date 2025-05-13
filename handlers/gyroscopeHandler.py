import threading
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.dispatcher import Dispatcher

# Shared variable and lock
gyroscope_data = {"x": 0, "y": 0, "z": 0}
data_lock = threading.Lock()

# Create a dispatcher to handle incoming messages
def gyroscope_handler(address, *args):
    x, y, z = args
    with data_lock:
        gyroscope_data["x"] = x
        gyroscope_data["y"] = y
        gyroscope_data["z"] = z

# Set up the OSC server
def start_osc_server(ip="0.0.0.0", port=12345):
    dispatcher = Dispatcher()
    dispatcher.map("/gyroscope", gyroscope_handler)  # Mapping the gyroscope data to handler function

    server = ThreadingOSCUDPServer((ip, port), dispatcher)  # Listen on IP and port
    print(f"Listening for OSC messages on {ip}:{port}")
    server.serve_forever()

def osc_thread_start():
    oscThread = threading.Thread(target=start_osc_server)
    oscThread.daemon = True
    oscThread.start()

        
