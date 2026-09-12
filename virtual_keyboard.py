import cv2
import mediapipe as mp
import math
from pynput.keyboard import Controller, Key

# ==========================================
# Keyboard controller
# ==========================================

keyboard_controller = Controller()

# ==========================================
# MediaPipe
# ==========================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ==========================================
# Keyboard layout
# ==========================================

keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M"],
    ["SPACE", "BACKSPACE", "ENTER"]
]

# ==========================================
# Text typed by user
# ==========================================

typed_text = ""

# ==========================================
# Get key position
# ==========================================

def get_key(x, y):

    start_y = 300
    key_height = 60

    for row_index, row in enumerate(keys):

        key_y = start_y + row_index * 70

        current_x = 40

        for key in row:

            if key == "SPACE":
                width = 300

            elif key == "BACKSPACE":
                width = 180

            elif key == "ENTER":
                width = 130

            else:
                width = 55

            if (
                current_x <= x <= current_x + width
                and key_y <= y <= key_y + key_height
            ):
                return key

            current_x += width + 8

    return None


# ==========================================
# Press key
# ==========================================

def press_key(key):

    global typed_text

    if key is None:
        return

    print("KEY PRESSED:", key)

    # ------------------------------
    # Normal letters
    # ------------------------------

    if len(key) == 1:

        typed_text += key

        keyboard_controller.press(key.lower())
        keyboard_controller.release(key.lower())

    # ------------------------------
    # Space
    # ------------------------------

    elif key == "SPACE":

        typed_text += " "

        keyboard_controller.press(Key.space)
        keyboard_controller.release(Key.space)

    # ------------------------------
    # Backspace
    # ------------------------------

    elif key == "BACKSPACE":

        if len(typed_text) > 0:
            typed_text = typed_text[:-1]

        keyboard_controller.press(Key.backspace)
        keyboard_controller.release(Key.backspace)

    # ------------------------------
    # Enter
    # ------------------------------

    elif key == "ENTER":

        typed_text += "\n"

        keyboard_controller.press(Key.enter)
        keyboard_controller.release(Key.enter)


# ==========================================
# Draw keyboard
# ==========================================

def draw_keyboard(frame, selected_key):

    start_y = 300
    key_height = 60

    for row_index, row in enumerate(keys):

        y = start_y + row_index * 70

        x = 40

        for key in row:

            if key == "SPACE":
                width = 300

            elif key == "BACKSPACE":
                width = 180

            elif key == "ENTER":
                width = 130

            else:
                width = 55

            # --------------------------
            # Selected key
            # --------------------------

            if key == selected_key:

                rectangle_color = (0, 255, 0)
                text_color = (0, 0, 0)
                thickness = -1

            else:

                rectangle_color = (255, 255, 255)
                text_color = (255, 255, 255)
                thickness = 2

            # Rectangle

            cv2.rectangle(
                frame,
                (x, y),
                (x + width, y + key_height),
                rectangle_color,
                thickness
            )

            # Text

            text_size = cv2.getTextSize(
                key,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                2
            )[0]

            text_x = x + (width - text_size[0]) // 2
            text_y = y + 40

            cv2.putText(
                frame,
                key,
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                text_color,
                2
            )

            x += width + 8


# ==========================================
# Camera
# ==========================================

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 700)

# ==========================================
# Pinch control
# ==========================================

pinch_active = False

# ==========================================
# Main loop
# ==========================================

while True:

    success, frame = cap.read()

    if not success:

        print("Camera not detected")
        break

    # Mirror camera

    frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape

    # RGB

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # Hand detection

    results = hands.process(rgb)

    selected_key = None

    # ======================================
    # Detect hand
    # ======================================

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        # Index finger

        index = hand.landmark[8]

        # Thumb

        thumb = hand.landmark[4]

        # Coordinates

        index_x = int(index.x * w)
        index_y = int(index.y * h)

        thumb_x = int(thumb.x * w)
        thumb_y = int(thumb.y * h)

        # ==================================
        # Find key
        # ==================================

        selected_key = get_key(
            index_x,
            index_y
        )

        # ==================================
        # Draw finger
        # ==================================

        cv2.circle(
            frame,
            (index_x, index_y),
            10,
            (0, 255, 0),
            -1
        )

        # ==================================
        # Thumb-index distance
        # ==================================

        distance = math.sqrt(
            (index.x - thumb.x) ** 2 +
            (index.y - thumb.y) ** 2
        )

        # ==================================
        # Pinch
        # ==================================

        if distance < 0.06:

            if not pinch_active:

                if selected_key:

                    press_key(selected_key)

                    pinch_active = True

        else:

            pinch_active = False

        # Draw hand

        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

    else:

        pinch_active = False

    # ======================================
    # Text area
    # ======================================

    cv2.rectangle(
        frame,
        (30, 110),
        (970, 210),
        (40, 40, 40),
        -1
    )

    cv2.rectangle(
        frame,
        (30, 110),
        (970, 210),
        (255, 255, 255),
        2
    )

    # Display typed text

    display_text = typed_text[-60:]

    cv2.putText(
        frame,
        display_text,
        (45, 170),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    # ======================================
    # Status
    # ======================================

    if selected_key:

        cv2.putText(
            frame,
            "Selected: " + selected_key,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    else:

        cv2.putText(
            frame,
            "Point at a key",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

    # ======================================
    # Instructions
    # ======================================

    cv2.putText(
        frame,
        "Pinch thumb + index to type",
        (30, 250),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    # ======================================
    # Draw keyboard
    # ======================================

    draw_keyboard(
        frame,
        selected_key
    )

    # ======================================
    # Show
    # ======================================

    cv2.imshow(
        "Virtual Keyboard",
        frame
    )

    # ======================================
    # Quit
    # ======================================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()