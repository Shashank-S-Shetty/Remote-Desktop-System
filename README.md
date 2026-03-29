# 🖥️ Python Remote Desktop System

A lightweight remote desktop application built using Python sockets that enables real-time screen streaming and remote control (mouse + keyboard) between two machines.

---

## 🚀 Overview

This project implements a basic **client-server remote desktop system** similar to tools like TeamViewer or AnyDesk.

* The **server** captures and streams the screen
* The **client** receives and displays the screen
* The client can control the server machine via mouse and keyboard input

---

## ✨ Features

* 📺 Real-time screen streaming
* 🖱️ Remote mouse control (move, click, scroll)
* ⌨️ Remote keyboard input (typing + special keys)
* ⚡ Compressed data transfer using `zlib`
* 🔌 Socket-based communication (TCP)
* 🧠 Lightweight and easy to understand implementation

---

## 🏗️ Architecture

```
+----------------+        TCP Socket        +----------------+
|    Server      |  <-------------------->  |     Client     |
|----------------|                         |----------------|
| Capture Screen |                         | Display Screen |
| Send Frames    |                         | Send Controls  |
| Execute Input  |                         | Capture Input  |
+----------------+                         +----------------+
```

---

## 🛠️ Tech Stack

* Python
* Socket Programming (TCP)
* OpenCV (cv2)
* NumPy
* MSS (screen capture)
* Pynput (keyboard & mouse control)
* PyAutoGUI

---

## 📦 Installation

Install dependencies on both client and server:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install mss pynput opencv-python numpy pyautogui
```

---

## ▶️ How to Run

### 1. Start Server

On the machine you want to control:

```bash
python server.py
```

You should see:

```
Waiting for connection...
```

---

### 2. Get Server IP

* Windows: `ipconfig`
* Mac/Linux: `ifconfig`

Example:

```
192.168.1.5
```

---

### 3. Start Client

On your local machine:

```bash
python client.py
```

Enter server IP:

```
Enter server IP: 192.168.1.5
```

---

### 4. Control

* Move mouse → controls remote machine
* Click → works
* Type → works
* Press `q` → exit

---

## ⚠️ Limitations

* Works only on the same network (LAN)
* No encryption (not secure for public use)
* Fixed screen resolution (default: 1920x1080) (Can be changed in Client.py)
* No authentication mechanism

---

## 🔮 Future Improvements

* 🔐 Add encryption (SSL/TLS)
* 🌍 Internet support (port forwarding / WebRTC)
* 🎥 Adaptive resolution & FPS
* 🧑‍💻 GUI interface
* 🔑 Authentication system

---

## 📁 Project Structure

```
remote-desktop/
│
├── server.py
├── client.py
├── requirements.txt
└── README.md
```

---

## 👨‍💻 Author

**Shashank S Shetty**

