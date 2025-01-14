# Gesture-Controlled Interactive-Browsing

## Introduction

This project enables users to control mouse actions and navigate browser tabs using hand gestures. It leverages the **MediaPipe** library for hand tracking and **PyAutoGUI** for simulating keyboard and mouse events. The supported gestures include:

- **Two-finger swipe left/right**: Switch between browser tabs.
- **Hand movement up/down**: Scroll the page vertically.
- **Thumbs-up**: Open a new tab.
- **Thumbs-down**: Close the current tab.

## Features

- **Gesture Recognition**: Detects specific hand gestures mapped to browser navigation actions.
- **Smooth Gesture Execution**: Utilizes smoothing algorithms to minimize jitter and improve usability.
- **Gesture Timeout**: Prevents unintended multiple triggers from a single gesture.
- **Dynamic Scroll Speed**: Adjusts scrolling speed based on the intensity of hand movements.

## Dependencies

Ensure the following Python libraries are installed:

- OpenCV (`cv2`)
- MediaPipe (`mediapipe`)
- PyAutoGUI (`pyautogui`)
- NumPy (`numpy`)

Install these dependencies using pip:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

## Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Faizi805/Interactive-Browsing.git
   ```

2. **Navigate to the Project Directory:**

   ```bash
   cd Interactive-Browsing
   ```

3. **Run the Script:**

   ```bash
   python gesture_control.py
   ```

## Usage

1. **Perform Gestures:**

   - **Two-finger swipe left/right:** Place your index and middle fingers together and swipe left or right to switch tabs.
   - **Hand movement up/down:** Move your entire hand upward or downward to scroll the page.
   - **Thumbs-up:** Touch your thumb to your index finger to open a new tab.
   - **Thumbs-down:** Touch your thumb to your middle finger to close the current tab.

2. **Exit the Program:**

   - Press `q` on your keyboard to exit the gesture control loop.

## Code Overview

The project is built using the following key components:

- **MediaPipe:** For detecting hand landmarks and tracking gestures.
- **OpenCV:** For capturing video from the webcam and displaying the output.
- **PyAutoGUI:** For simulating keyboard and mouse events (e.g., tab switching, scrolling).
- **NumPy:** For numerical operations and smoothing hand movements.

## Key Functions

- `left_tab_switch()`: Switches to the previous tab in the browser.
- `right_tab_switch()`: Switches to the next tab in the browser.
- `scroll_up()` and `scroll_down()`: Scroll the page up or down based on hand movement.
- `open_new_tab()`: Opens a new tab in the browser.
- `close_current_tab()`: Closes the current tab in the browser.
- `smooth_position(position)`: Applies a moving average filter to smooth hand positions and reduce noise.
- `exponential_smooth(position, alpha)`: Applies exponential smoothing with a defined alpha value to further minimize jitter.
- `detect_thumbs_up(hand_landmarks)`: Detects a thumbs-up gesture from hand landmark data.
- `detect_thumbs_down(hand_landmarks)`: Detects a thumbs-down gesture from hand landmark data.

## Future Enhancements

- **Customizable Gestures:** Allow users to define their own gestures for specific actions.
- **Extended Browser Control:** Add gestures for functions like refreshing, bookmarking, or navigating back and forward.
- **Cross-Platform Compatibility:** Optimize the script for seamless use on different operating systems.
- **Multi-Gesture Support:** Enable multiple gestures to be recognized simultaneously.

---

This project combines simplicity with functionality, making it an excellent tool for hands-free browser navigation. Explore the possibilities and enjoy a more interactive browsing experience!



