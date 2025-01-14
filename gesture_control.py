import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np

# Initialize MediaPipe hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Variables to track gesture
previous_positions = {}
gesture_triggered = False
last_gesture_time = time.time()
gesture_timeout = 1.0  # Timeout in seconds to prevent multiple gestures in quick succession

# Smoothing variables
SMOOTHING_WINDOW_SIZE = 5  # Number of frames to average for smoothing
index_finger_tip_history = []
middle_finger_tip_history = []
wrist_history = []
thumb_tip_history = []

# Exponential smoothing factor
SMOOTHING_FACTOR = 0.3  # Lower values make the smoothing stronger

def left_tab_switch():
    """Function to switch to the previous tab in Chrome."""
    pyautogui.hotkey('ctrl', 'shift', 'tab')
    time.sleep(0.2)  # Small delay to allow tab to switch

def right_tab_switch():
    """Function to switch to the next tab in Chrome."""
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(0.2)  # Small delay to allow tab to switch

def scroll_up(scroll_speed):
    """Function to scroll up the current page."""
    pyautogui.scroll(scroll_speed)
    time.sleep(0.05)  # Small delay to allow scroll to apply

def scroll_down(scroll_speed):
    """Function to scroll down the current page."""
    pyautogui.scroll(-scroll_speed)
    time.sleep(0.05)  # Small delay to allow scroll to apply

def open_new_tab():
    """Function to open a new tab in Chrome."""
    pyautogui.hotkey('ctrl', 't')
    time.sleep(0.2)  # Small delay to allow tab to open

def close_current_tab():
    """Function to close the current tab in Chrome."""
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(0.2)  # Small delay to allow tab to close

def smooth_position(history, new_value, window_size):
    """Apply a moving average filter to smooth the position."""
    history.append(new_value)
    if len(history) > window_size:
        history.pop(0)  # Remove the oldest value
    return np.mean(history)  # Return the average of the last `window_size` values

def exponential_smooth(previous_value, new_value, smoothing_factor):
    """Apply exponential smoothing to reduce jitter."""
    return smoothing_factor * new_value + (1 - smoothing_factor) * previous_value

def detect_thumbs_up(thumb_tip, index_finger_tip):
    """Detect a thumbs-up gesture (thumb and index finger touching)."""
    distance = np.sqrt((thumb_tip.x - index_finger_tip.x)**2 + (thumb_tip.y - index_finger_tip.y)**2)
    return distance < 0.1  # Threshold for thumb and index finger touching

def detect_thumbs_down(thumb_tip, middle_finger_tip):
    """Detect a thumbs-down gesture (thumb and middle finger touching)."""
    distance = np.sqrt((thumb_tip.x - middle_finger_tip.x)**2 + (thumb_tip.y - middle_finger_tip.y)**2)
    return distance < 0.1  # Threshold for thumb and middle finger touching

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame to avoid mirror effect
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    # Check if any hand landmarks are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the positions of the index, middle, and thumb fingertips
            index_finger_tip = hand_landmarks.landmark[8]  # INDEX_FINGER_TIP
            middle_finger_tip = hand_landmarks.landmark[12]  # MIDDLE_FINGER_TIP
            thumb_tip = hand_landmarks.landmark[4]  # THUMB_TIP
            wrist = hand_landmarks.landmark[0]  # WRIST

            # Smooth the positions using a moving average
            index_finger_tip_x = smooth_position(index_finger_tip_history, index_finger_tip.x, SMOOTHING_WINDOW_SIZE)
            middle_finger_tip_x = smooth_position(middle_finger_tip_history, middle_finger_tip.x, SMOOTHING_WINDOW_SIZE)
            thumb_tip_x = smooth_position(thumb_tip_history, thumb_tip.x, SMOOTHING_WINDOW_SIZE)

            # Exponential smoothing for wrist position
            if 'wrist' not in previous_positions:
                wrist_y = wrist.y
            else:
                wrist_y = exponential_smooth(previous_positions['wrist'], wrist.y, SMOOTHING_FACTOR)

            # Initialize previous positions if this is the first detection
            if not previous_positions:
                previous_positions = {
                    'index_finger_tip': index_finger_tip_x,
                    'middle_finger_tip': middle_finger_tip_x,
                    'thumb_tip': thumb_tip_x,
                    'wrist': wrist_y
                }

            # Detect left and right swipes for tab switching
            if abs(previous_positions['index_finger_tip'] - index_finger_tip_x) > 0.05 and \
               abs(previous_positions['middle_finger_tip'] - middle_finger_tip_x) > 0.05:
                if not gesture_triggered:
                    current_time = time.time()
                    if current_time - last_gesture_time > gesture_timeout:
                        if previous_positions['index_finger_tip'] > index_finger_tip_x and \
                           previous_positions['middle_finger_tip'] > middle_finger_tip_x:
                            print("Two-finger swipe left detected! Switching to previous tab.")
                            left_tab_switch()
                        elif previous_positions['index_finger_tip'] < index_finger_tip_x and \
                             previous_positions['middle_finger_tip'] < middle_finger_tip_x:
                            print("Two-finger swipe right detected! Switching to next tab.")
                            right_tab_switch()
                        gesture_triggered = True
                        last_gesture_time = current_time
                        time.sleep(0.5)  # Wait for 0.5 seconds to avoid multiple triggers

            # Detect up and down hand movements for scrolling
            if abs(previous_positions['wrist'] - wrist_y) > 0.05:
                if not gesture_triggered:
                    current_time = time.time()
                    if current_time - last_gesture_time > gesture_timeout:
                        scroll_speed = int(abs(previous_positions['wrist'] - wrist_y) * 20000)  # Dynamic scroll speed
                        if previous_positions['wrist'] > wrist_y:
                            print("Hand moved up! Scrolling up.")
                            scroll_up(scroll_speed)
                        elif previous_positions['wrist'] < wrist_y:
                            print("Hand moved down! Scrolling down.")
                            scroll_down(scroll_speed)
                        gesture_triggered = True
                        last_gesture_time = current_time
                        time.sleep(0.1)  # Small delay to allow smooth scrolling

            # Detect thumbs-up gesture for opening a new tab
            if detect_thumbs_up(thumb_tip, index_finger_tip):
                if not gesture_triggered:
                    current_time = time.time()
                    if current_time - last_gesture_time > gesture_timeout:
                        print("Thumbs-up detected! Opening a new tab.")
                        open_new_tab()
                        gesture_triggered = True
                        last_gesture_time = current_time
                        time.sleep(0.5)  # Wait for 0.5 seconds to avoid multiple triggers

            # Detect thumbs-down gesture for closing the current tab
            if detect_thumbs_down(thumb_tip, middle_finger_tip):
                if not gesture_triggered:
                    current_time = time.time()
                    if current_time - last_gesture_time > gesture_timeout:
                        print("Thumbs-down detected! Closing the current tab.")
                        close_current_tab()
                        gesture_triggered = True
                        last_gesture_time = current_time
                        time.sleep(0.5)  # Wait for 0.5 seconds to avoid multiple triggers

            # Update previous positions for the next frame
            previous_positions = {
                'index_finger_tip': index_finger_tip_x,
                'middle_finger_tip': middle_finger_tip_x,
                'thumb_tip': thumb_tip_x,
                'wrist': wrist_y
            }

        # Reset gesture trigger if fingers are not moving
        if abs(previous_positions['index_finger_tip'] - index_finger_tip_x) < 0.01 and \
           abs(previous_positions['middle_finger_tip'] - middle_finger_tip_x) < 0.01 and \
           abs(previous_positions['wrist'] - wrist_y) < 0.01:
            gesture_triggered = False

    # Display the frame
    cv2.imshow("Gesture Control Demo", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()