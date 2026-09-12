import cv2
import mediapipe as mp
import pyautogui
import math

# -----------------------------
# Screen size
# -----------------------------

screen_width, screen_height = pyautogui.size()

# -----------------------------
# MediaPipe
# -----------------------------

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# -----------------------------
# Camera
# -----------------------------

cap = cv2.VideoCapture(0)

# Camera resolution
cam_width = 640
cam_height = 480

cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)

# Previous mouse position
prev_x = 0
prev_y = 0

# Smoothness
smoothening = 5

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        # Index finger
        index = hand.landmark[8]

        # Thumb
        thumb = hand.landmark[4]

        # Convert index position
        x = int(index.x * cam_width)
        y = int(index.y * cam_height)

        # Convert camera coordinates to screen coordinates
        screen_x = int(
            index.x * screen_width
        )

        screen_y = int(
            index.y * screen_height
        )

        # Smooth movement
        current_x = prev_x + (
            screen_x - prev_x
        ) / smoothening

        current_y = prev_y + (
            screen_y - prev_y
        ) / smoothening

        pyautogui.moveTo(
            current_x,
            current_y
        )

        prev_x = current_x
        prev_y = current_y

        # Draw index point
        cv2.circle(
            frame,
            (x, y),
            10,
            (0, 255, 0),
            -1
        )

        # Distance between thumb and index
        distance = math.sqrt(
            (index.x - thumb.x) ** 2 +
            (index.y - thumb.y) ** 2
        )

        # Pinch = click
        if distance < 0.05:

            pyautogui.click()

            cv2.putText(
                frame,
                "CLICK",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

    cv2.imshow(
        "Virtual Mouse",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()