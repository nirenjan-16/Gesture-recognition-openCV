import cv2
import mediapipe as mp
import math
import time

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)

# ---------------- MEDIAPIPE ----------------
mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_mesh

hands = mp_hands.Hands(max_num_hands=2)
face_mesh = mp_face.FaceMesh(refine_landmarks=True)

# ---------------- LOAD IMAGES ----------------
def load_img(name):
    img = cv2.imread(name)
    if img is None:
        print(f"ERROR loading {name}")
        exit()
    return cv2.resize(img, (180, 180))

IMAGES = {
    "shock": load_img("shock.jpeg"),
    "laugh": load_img("baby.jpg"),
    "monkey": load_img("display.jpg"),
    "lemme know": load_img("lemme.jpeg"),
    "Absolute Cinema": load_img("cinema.jpeg"),
    "thumb": load_img("thumb.jpeg"),
}

# ---------------- HELPERS ----------------
def dist(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

# ---------------- STABILITY ----------------
FRAME_CONFIRM = 10
LATCH_DURATION = 2.5

gesture_buffer = {}
latched_gesture = None
latch_start = 0

PRIORITY = [
    "shock",
    "angry",
    "Absolute Cinema",
    "thumb",
    "devious",
    "laugh",
    "monkey",
    "lemme know"
]

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_res = hands.process(rgb)
    face_res = face_mesh.process(rgb)

    detected = []
    now = time.time()

    # ---------------- FACE ----------------
    if face_res.multi_face_landmarks:
        face = face_res.multi_face_landmarks[0]
        mouth_open = abs(face.landmark[13].y - face.landmark[14].y) > 0.04
        smile = abs(face.landmark[61].y - face.landmark[291].y) > 0.02
        eye_closed = (
            abs(face.landmark[159].y - face.landmark[145].y) < 0.008 and
            abs(face.landmark[386].y - face.landmark[374].y) < 0.008
        )
        head_up = face.landmark[10].y < face.landmark[152].y - 0.1
    else:
        continue

    # ---------------- HANDS ----------------
    hands_count = 0
    fist = False
    hands_close = False
    hands_head = False
    finger_lips = False
    fist_near_mouth = False
    thumbs_up_count = 0

    if hand_res.multi_hand_landmarks:
        hands_count = len(hand_res.multi_hand_landmarks)

        if hands_count == 2:
            h1 = hand_res.multi_hand_landmarks[0].landmark[9]
            h2 = hand_res.multi_hand_landmarks[1].landmark[9]
            hands_close = dist(h1, h2) < 0.07

        for hand in hand_res.multi_hand_landmarks:
            palm = hand.landmark[9]
            tips = [hand.landmark[i] for i in [8, 12, 16, 20]]

            # clenched fist
            if all(dist(t, palm) < 0.045 for t in tips):
                fist = True

            # finger on lips
            if dist(hand.landmark[8], face.landmark[13]) < 0.04:
                finger_lips = True

            # hands behind head
            if palm.y < face.landmark[10].y:
                hands_head = True

            # fist near mouth (baby)
            if mouth_open and dist(palm, face.landmark[13]) < 0.08:
                fist_near_mouth = True

            # thumbs up detection
            thumb_tip = hand.landmark[4]
            index_tip = hand.landmark[8]
            if thumb_tip.y < index_tip.y:
                thumbs_up_count += 1

    # ---------------- GESTURES ----------------

    # SHOCK → both hands behind head
    if hands_count == 2 and hands_head:
        detected.append("shock")

    # VANA → hands together (namaste)
    if hands_count == 2:
        detected.append("Absolute Cinema")

    # THUMB → double thumbs up
    if thumbs_up_count == 1:
        detected.append("thumb")

    # BABY → laugh
    if mouth_open:
        detected.append("laugh")

    # MONKEY → finger on lips
    if finger_lips:
        detected.append("monkey")

    # LEMME → unchanged
    if eye_closed and head_up and hands_count == 0:
        detected.append("lemme know")

    # ---------------- PRIORITY ----------------
    gesture = None
    for p in PRIORITY:
        if p in detected:
            gesture = p
            break

    # ---------------- LATCH ----------------
    if latched_gesture is None:
        if gesture:
            gesture_buffer[gesture] = gesture_buffer.get(gesture, 0) + 1
        else:
            gesture_buffer.clear()

        if gesture and gesture_buffer.get(gesture, 0) >= FRAME_CONFIRM:
            latched_gesture = gesture
            latch_start = now
            gesture_buffer.clear()
    else:
        if now - latch_start > LATCH_DURATION:
            latched_gesture = None

    # ---------------- DISPLAY ----------------
    if latched_gesture:
        frame[20:200, 20:200] = IMAGES[latched_gesture]
        cv2.putText(
            frame,
            latched_gesture.upper(),
            (20, 225),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2
        )

    cv2.imshow("Gesture Recognition System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
