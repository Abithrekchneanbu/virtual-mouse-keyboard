# 🖱️ Virtual Mouse & ⌨️ Virtual Keyboard

> A real-time computer vision based Human-Computer Interaction (HCI) system that enables mouse and keyboard interaction using hand gestures captured through a webcam.

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-red?logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange)
![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-Automation-green)
![Pynput](https://img.shields.io/badge/Pynput-Input%20Control-purple)
![JavaScript](https://img.shields.io/badge/JavaScript-Web%20Demo-yellow?logo=javascript)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Deployed-black?logo=github)

</p>

---

## 📌 Overview

**Virtual Mouse & Virtual Keyboard** is a computer vision based Human-Computer Interaction project that allows users to interact with a computer using hand gestures instead of traditional physical input devices.

The system captures live video from a webcam, detects the user's hand using **MediaPipe**, processes hand landmarks using **Python and OpenCV**, and converts specific gestures into mouse and keyboard actions.

The project also includes an **interactive browser-based demonstration** deployed using GitHub Pages.

---

## ✨ Features

### 🖱️ Virtual Mouse

- Real-time hand tracking using webcam
- Index-finger based cursor movement
- Pinch gesture for mouse clicking
- Smooth cursor movement
- Touch-free interaction
- Real-time visual feedback

### ⌨️ Virtual Keyboard

- Gesture-controlled virtual keyboard
- Real-time hand landmark detection
- Index-finger based key selection
- Pinch gesture for key selection
- Supports:
  - Alphabet keys
  - Space
  - Enter
  - Backspace
- Real-time typed text display

### 🌐 Web Demonstration

The project also provides an interactive browser-based demonstration.

Users can:

- Access the webcam directly from the browser
- Visualize hand tracking
- Control a virtual cursor
- Interact with a virtual keyboard
- Test gesture recognition without installing Python

> **Note:** The browser demo controls interaction inside the webpage. Browser security restrictions prevent a normal website from controlling the visitor's operating-system-level mouse or typing into external applications.

---

# 🏗️ System Architecture

```text
                  ┌────────────────────┐
                  │      Webcam        │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │   OpenCV Capture   │
                  │  & Frame Processing│
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │     MediaPipe      │
                  │  Hand Landmarker   │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Hand Landmark      │
                  │ Extraction         │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Gesture Recognition│
                  └─────────┬──────────┘
                            │
                  ┌─────────┴──────────┐
                  ▼                    ▼
        ┌─────────────────┐  ┌─────────────────┐
        │  Virtual Mouse  │  │ Virtual Keyboard│
        └────────┬────────┘  └────────┬────────┘
                 │                    │
                 ▼                    ▼
        ┌─────────────────┐  ┌─────────────────┐
        │ PyAutoGUI /     │  │ Pynput /        │
        │ Mouse Control   │  │ Keyboard Input  │
        └─────────────────┘  └─────────────────┘
