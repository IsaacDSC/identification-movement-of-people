import cv2
import os

video_path = 'src/videoplayback.mp4'

# Verifica se o arquivo de vídeo existe
if not os.path.exists(video_path):
    print(f"Arquivo de vídeo não encontrado: {video_path}")
    exit()

# Abre o vídeo
cap = cv2.VideoCapture(video_path)

# Verifica se o vídeo foi aberto com sucesso
if not cap.isOpened():
    print("Erro ao abrir o vídeo")
    exit()

# Inicializa o detector de pessoas
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Lista para armazenar os trackers
trackers = []

# Variável para armazenar as posições anteriores dos bounding boxes
previous_boxes = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detecta pessoas no frame
    boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))

    # Adiciona novos trackers para as pessoas detectadas
    if len(trackers) == 0:
        for (x, y, w, h) in boxes:
            tracker = cv2.TrackerKCF_create()
            trackers.append(tracker)
            tracker.init(frame, (x, y, w, h))

    # Atualiza todos os trackers
    new_boxes = []
    for tracker in trackers:
        success, newbox = tracker.update(frame)
        if success:
            new_boxes.append(newbox)

    # Desenha os bounding boxes ao redor das pessoas detectadas
    for i, newbox in enumerate(new_boxes):
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))

        # Verifica se a pessoa se movimentou
        if i < len(previous_boxes):
            prev_box = previous_boxes[i]
            if (abs(prev_box[0] - newbox[0]) > 5 or abs(prev_box[1] - newbox[1]) > 5):
                # Desenha a ROI de cor vermelha para pessoas que se movimentaram
                cv2.rectangle(frame, p1, p2, (0, 0, 255), 2)
            else:
                # Desenha a ROI de cor azul para pessoas que não se movimentaram
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2)
        else:
            # Desenha a ROI de cor azul para novas detecções
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2)

    # Atualiza as posições anteriores dos bounding boxes
    previous_boxes = new_boxes

    # Mostra o frame
    cv2.imshow('Detecção e Tracking de Pessoas', frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera o objeto de captura e fecha todas as janelas
cap.release()
cv2.destroyAllWindows()