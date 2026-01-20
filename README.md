# Gesture Recognition System using OpenCV & MediaPipe

## 📌 Overview
This project is a real-time **gesture recognition system** built using **Python, OpenCV, and MediaPipe**.  
It captures live video from a webcam, detects hand and facial landmarks, recognizes predefined gestures, and dynamically displays corresponding images.

The system is designed to be **stable, flicker-free**, and suitable for **college mini-projects, demos, and portfolios**.

## 🚀 Features
- Real-time webcam processing
- Hand gesture recognition
- Facial expression detection
- Gesture latching for stability (no flicker)
- Image display based on detected gesture
- Modular and easily extendable design

---

## 🧠 Gestures Implemented

| Gesture Name | Description |
|-------------|------------|
| Shock | Both hands placed behind the head |
| Devious | Both hands together with a smile |
| Angry | Clenched fist |
| Baby | Laughing expression |
| Monkey | Finger placed near lips |
| Lemme | Eyes closed with head tilted upward |
| Vana | Hands together (Namaste gesture) |
| Thumb | Double thumbs up |

---

## 🛠 Tech Stack
- **Python 3.10**
- **OpenCV**
- **MediaPipe**
- **Git & GitHub**

---

## 🔄 System Flowchart

                                    +------------------+
                                    | Start Program |
                                    +------------------+
                                            |
                                            v
                                    +------------------+
                                    | Capture Webcam |
                                    | Frame (OpenCV) |
                                    +------------------+
                                            |
                                            v
                                    +--------------------------+
                                    | Extract Face & Hand |
                                    | Landmarks (MediaPipe) |
                                    +--------------------------+
                                            |
                                            v
                                    +--------------------------+
                                    | Gesture Rule Matching |
                                    | (Hands / Face Logic) |
                                    +--------------------------+
                                            |
                                            v    
                                    +--------------------------+
                                    | Gesture Confirmation |
                                    | (Frame Count + Latch) |
                                    +--------------------------+
                                            |
                                            v
                                    +--------------------------+
                                    | Display Corresponding |
                                    | Image on Screen |
                                    +--------------------------+
                                            |
                                            v
                                    +------------------+
                                    | Repeat Loop |
                                    +------------------+


## 📚 Applications

- Human–Computer Interaction (HCI)
- Smart displays
- Gesture-controlled interfaces
- AR/VR prototyping
- Computer vision learning projects

---
