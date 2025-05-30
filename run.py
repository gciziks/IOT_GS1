import cv2
import mediapipe as mp
import winsound
import pyttsx3
import threading
import queue
from datetime import datetime

# Inicialização do MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hand_detector = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Inicialização do TTS e controle por fila
tts_engine = pyttsx3.init()
tts_queue = queue.Queue()

# Inicialização de variáveis de estado
flash_on = False
alert_atv = False
emerg_sound = False
screen_msg = ""
msg_counter = 0

# Função para logar os gestos
def log_action(text):
    with open("log_gestos.txt", "a", encoding="utf-8") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{timestamp}] {text}\n")

# Thread e funções para enfileirar os textos que serão lidos em voz
def tts_worker():
    while True:
        text = tts_queue.get()
        if text is None:
            break
        tts_engine.say(text)
        tts_engine.runAndWait()
        tts_queue.task_done()

tts_thread = threading.Thread(target=tts_worker, daemon=True)
tts_thread.start()

def speak_async(text):
    tts_queue.put(text)

# Função para contar dedos levantados
def count_fingers(hand_landmarks, hand_label):
    fingers = []

    # Lógica do polegar (dependendo da mão direita ou esquerda)
    if hand_label == "Right":
        fingers.append(
            1 if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x <
                 hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x else 0
        )
    else:
        fingers.append(
            1 if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x >
                 hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x else 0
        )

    # Outros dedos (compara a ponta com a articulação do meio)
    tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    pips = [
        mp_hands.HandLandmark.INDEX_FINGER_PIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        mp_hands.HandLandmark.RING_FINGER_PIP,
        mp_hands.HandLandmark.PINKY_PIP
    ]

    for tip, pip in zip(tips, pips):
        fingers.append(1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y else 0)

    return fingers

# Inicialização da câmera
cap = cv2.VideoCapture(0)
print("Aplicação inicializando...")
print("Pressione ESC para parar")

# Loop principal
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hand_detector.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = handedness.classification[0].label
            fingers = count_fingers(hand_landmarks, label)
            total_fingers = sum(fingers)

            # Ações baseadas nos gestos

            if total_fingers == 5 and not flash_on:
                screen_msg = "Mão Aberta - Ligando lanterna"
                msg_counter = 60
                flash_on = True
                speak_async("Lanterna ligada")
                log_action("Lanterna ligada")

            elif fingers == [1, 0, 0, 0, 1] and flash_on:
                screen_msg = "Hang Loose - Desligando lanterna"
                msg_counter = 60
                flash_on = False
                speak_async("Lanterna desligada")
                log_action("Lanterna desligada")

            elif total_fingers == 0 and not emerg_sound:
                screen_msg = "Punho - Emitindo som de emergência"
                msg_counter = 60
                emerg_sound = True
                speak_async("Som de emergência ativado")
                log_action("Som de emergência ativado")
                winsound.Beep(1000, 500)

            elif total_fingers == 1 and fingers[1] == 1 and emerg_sound:
                screen_msg = "Indicador - Parando som"
                msg_counter = 60
                emerg_sound = False
                speak_async("Som de emergência desativado")
                log_action("Som de emergência desativado")

            elif fingers == [0, 1, 1, 0, 0] and not alert_atv:
                screen_msg = "Paz - Alerta visual ativado"
                msg_counter = 60
                alert_atv = True
                speak_async("Alerta visual ativado")
                log_action("Alerta visual ativado")

            elif fingers == [0, 1, 0, 0, 1] and alert_atv:
                screen_msg = "Rock - Alerta visual desativado"
                msg_counter = 60
                alert_atv = False
                speak_async("Alerta visual desativado")
                log_action("Alerta visual desativado")

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Efeitos na tela
    if flash_on:
        frame[:] = (255, 255, 255)
        cv2.putText(frame, "Lanterna Ligada", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)

    if alert_atv:
        cv2.putText(frame, "!!! ALERTA ATIVO !!!", (30, 400), cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 255), 3)

    if msg_counter > 0:
        cv2.putText(frame, screen_msg, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        msg_counter -= 1

    cv2.imshow("Sistema de Emergência por Gestos", frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

tts_queue.put(None)
tts_thread.join()
