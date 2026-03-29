import socket
import struct
import pickle
import zlib
import numpy as np
import cv2  # For displaying the screen
import pyautogui  # For getting mouse position
from pynput import keyboard, mouse  # For capturing keyboard & mouse inputs

# Connect to Server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input("Enter server IP: ")
client_socket.connect((host, 9999))

data = b""
payload_size = struct.calcsize(">L")  # 4 bytes for data size

# Function to send keystrokes to server
def on_press(key):
    try:
        if key == keyboard.Key.enter:
            client_socket.sendall("enter".encode())
        elif key == keyboard.Key.backspace:
            client_socket.sendall("backspace".encode())
        elif key == keyboard.Key.space:  # ✅ Fix for Space Key
            client_socket.sendall("space".encode())
        elif key == keyboard.Key.tab:  # ✅ Allows Alt + Tab for switching windows
            client_socket.sendall("tab".encode())
        elif key == keyboard.Key.esc:  # ✅ Allows closing applications
            client_socket.sendall("esc".encode())
        elif key == keyboard.Key.up:
            client_socket.sendall("up_arrow".encode())  # ✅ Up Arrow Key
        elif key == keyboard.Key.down:
            client_socket.sendall("down_arrow".encode())  # ✅ Down Arrow Key
        elif key == keyboard.Key.left:
            client_socket.sendall("left_arrow".encode())  # ✅ Left Arrow Key
        elif key == keyboard.Key.right:
            client_socket.sendall("right_arrow".encode())  # ✅ Right Arrow Key
        elif hasattr(key, 'char') and key.char:  # Handles normal typing
            client_socket.sendall(f"type:{key.char}".encode())
    except:
        pass

# Start listening for keyboard events
keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

# Function to send mouse clicks and scrolls
def on_click(x, y, button, pressed):
    if pressed:
        if button == mouse.Button.left:
            client_socket.sendall("click".encode())  # Send left click
        elif button == mouse.Button.right:
            client_socket.sendall("right_click".encode())  # Send right click

def on_scroll(x, y, dx, dy):
    if dy > 0:
        client_socket.sendall("scroll_up".encode())  # ✅ Scroll Up
    else:
        client_socket.sendall("scroll_down".encode())  # ✅ Scroll Down

# Start listening for mouse clicks & scroll
mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
mouse_listener.start()

while True:
    # Receive the size of incoming image data
    while len(data) < payload_size:
        data += client_socket.recv(4096)
    packed_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_size)[0]

    # Receive the image data
    while len(data) < msg_size:
        data += client_socket.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Decompress and convert to image
    frame = pickle.loads(zlib.decompress(frame_data))
    frame = np.frombuffer(frame, dtype=np.uint8).reshape(1080,1920, 3)  # Adjust resolution if needed

    # Display Screen
    cv2.imshow("Remote Desktop", frame)

    # Capture Mouse Movement
    x, y = pyautogui.position()
    client_socket.sendall(f"mouse:{x},{y}".encode())

    if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to quit
        break

client_socket.close()