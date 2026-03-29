import socket
import struct
import pickle
import zlib
import mss  # For capturing the screen
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key

# Initialize mouse and keyboard controllers
mouse = MouseController()
keyboard = KeyboardController()

# Setup Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 9999))  # Listen on all IPs, port 9999
server_socket.listen(1)
print("Waiting for connection...")

conn, addr = server_socket.accept()
print(f"Connected to {addr}")

with mss.mss() as sct:
    while True:
        # Capture screen
        screenshot = sct.grab(sct.monitors[1])  # Capture primary screen
        img_data = pickle.dumps(screenshot.rgb)  # Convert image to bytes
        compressed_data = zlib.compress(img_data, 6)  # Compress to optimize

        # Send data size first (fixed length: 4 bytes)
        conn.sendall(struct.pack(">L", len(compressed_data)))
        conn.sendall(compressed_data)  # Send the actual image data

        # Receive and process remote control commands
        try:
            command = conn.recv(1024).decode()
            if command.startswith("mouse:"):
                x, y = map(int, command.split(":")[1].split(","))
                mouse.position = (x, y)  # Move mouse
            elif command == "click":
                mouse.press(Button.left)
                mouse.release(Button.left)  # Ensures the click registers properly
            elif command == "right_click":
                mouse.press(Button.right)
                mouse.release(Button.right)
            elif command == "double_click":
                mouse.click(Button.left, 2)
            elif command == "scroll_up":
                mouse.scroll(0, 2)  # ✅ Scroll Up
            elif command == "scroll_down":
                mouse.scroll(0, -2)  # ✅ Scroll Down
            elif command.startswith("type:"):
                text = command.split(":")[1]
                keyboard.type(text)
            elif command == "enter":
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
            elif command == "backspace":
                keyboard.press(Key.backspace)
                keyboard.release(Key.backspace)
            elif command == "space":
                keyboard.press(Key.space)
                keyboard.release(Key.space)
            elif command == "tab":
                keyboard.press(Key.tab)
                keyboard.release(Key.tab)  # Allows Alt + Tab for switching windows
            elif command == "esc":
                keyboard.press(Key.esc)
                keyboard.release(Key.esc)  # Allows closing applications
            elif command == "up_arrow":
                keyboard.press(Key.up)
                keyboard.release(Key.up)  # ✅ Up Arrow Key
            elif command == "down_arrow":
                keyboard.press(Key.down)
                keyboard.release(Key.down)  # ✅ Down Arrow Key
            elif command == "left_arrow":
                keyboard.press(Key.left)
                keyboard.release(Key.left)  # ✅ Left Arrow Key
            elif command == "right_arrow":
                keyboard.press(Key.right)
                keyboard.release(Key.right)  # ✅ Right Arrow Key
        except:
            pass