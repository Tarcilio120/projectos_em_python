import cv2  # Biblioteca para manipulação de vídeo e imagens
import mediapipe as mp  # Biblioteca para rastreamento de mãos
import numpy as np  # Biblioteca para cálculos numéricos
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # Biblioteca para controle de áudio do sistema
from comtypes import CLSCTX_ALL  # Biblioteca para contexto COM necessário no Pycaw

# Configurações do MediaPipe para detecção de mãos
mp_hands = mp.solutions.hands  # Solução para rastreamento de mãos
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)  # Inicializa o modelo de detecção de mãos
mp_drawing = mp.solutions.drawing_utils  # Utilitário para desenhar landmarks

# Configurações do Pycaw para controle de volume
devices = AudioUtilities.GetSpeakers()  # Obtém os dispositivos de áudio disponíveis
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None  # Ativa a interface para controle de volume
)
volume = interface.QueryInterface(IAudioEndpointVolume)  # Obtém a interface de controle de volume

# Obter os níveis de volume mínimo e máximo
vol_range = volume.GetVolumeRange()  # Obtém o intervalo de volume disponível
min_vol = vol_range[0]  # Volume mínimo
max_vol = vol_range[1]  # Volume máximo

# Inicializar a câmera
cap = cv2.VideoCapture(0)  # Abre a webcam

while cap.isOpened():  # Loop enquanto a câmera estiver aberta
    success, frame = cap.read()  # Captura um frame da webcam
    if not success:
        break  # Sai do loop se não conseguir capturar o frame

    # Inverter a imagem para um efeito espelho e converter para RGB
    frame = cv2.flip(frame, 1)  # Espelha o frame horizontalmente
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Converte o frame de BGR para RGB

    # Processar a imagem para detectar mãos
    results = hands.process(rgb_frame)  # Detecta as mãos na imagem

    if results.multi_hand_landmarks:  # Verifica se há mãos detectadas
        for hand_landmarks in results.multi_hand_landmarks:  # Itera sobre as mãos detectadas
            # Obter coordenadas dos pontos específicos da mão
            landmarks = hand_landmarks.landmark  # Lista de landmarks da mão
            thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]  # Coordenadas da ponta do polegar
            index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]  # Coordenadas da ponta do indicador

            # Converter para coordenadas de pixel
            h, w, _ = frame.shape  # Obtém a altura e largura do frame
            thumb_coords = (int(thumb_tip.x * w), int(thumb_tip.y * h))  # Coordenadas do polegar em pixels
            index_coords = (int(index_tip.x * w), int(index_tip.y * h))  # Coordenadas do indicador em pixels

            # Desenhar os pontos na tela
            cv2.circle(frame, thumb_coords, 10, (255, 0, 0), -1)  # Desenha um círculo na ponta do polegar
            cv2.circle(frame, index_coords, 10, (0, 255, 0), -1)  # Desenha um círculo na ponta do indicador
            cv2.line(frame, thumb_coords, index_coords, (0, 255, 255), 2)  # Desenha uma linha entre o polegar e o indicador

            # Calcular a distância entre o polegar e o indicador
            distance = np.linalg.norm(np.array(thumb_coords) - np.array(index_coords))  # Calcula a distância entre os pontos

            # Normalizar a distância para ajustar o volume
            vol = np.interp(distance, [30, 200], [min_vol, max_vol])  # Mapeia a distância para o intervalo de volume
            volume.SetMasterVolumeLevel(vol, None)  # Ajusta o volume do sistema com base na distância

            # Mostrar o volume atual na tela
            cv2.putText(frame, f'Volume: {int(np.interp(vol, [min_vol, max_vol], [0, 100]))}%',
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)  # Exibe o volume em porcentagem

            # Desenhar as conexões da mão
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)  # Desenha os landmarks e conexões da mão

    # Mostrar o vídeo
    cv2.imshow('Controle de Volume com a Mão', frame)  # Exibe o frame na janela

    # Sair ao pressionar a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # Encerra o loop se a tecla 'q' for pressionada

# Liberar recursos
cap.release()  # Libera a câmera
cv2.destroyAllWindows()  # Fecha todas as janelas abertas
