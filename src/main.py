import cv2
from validator.tmp_validator import tmp_validation
from validator.tmp_moments import save_movement_image
from rules.cmd_rules import get_color

video_path = 'src/videoplayback.mp4'
output_dir = 'tmp/movement_images'

tmp_validation(output_dir, video_path)

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

# Contador de frames
frame_count = 0

# Detectar a cada N frames
detect_interval = 10

movement_count = 0
# 10 primeiras movimentações de pessoas serão salvas
max_movements = 10

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Detecta pessoas a cada N frames
    if frame_count % detect_interval == 0:
        boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))
        trackers = []
        for (x, y, w, h) in boxes:
            tracker = cv2.TrackerKCF_create()
            trackers.append(tracker)
            tracker.init(frame, (x, y, w, h))
    else:
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
                    cv2.rectangle(frame, p1, p2, get_color('moved'), 2)
                    # Salva a imagem da pessoa que se movimentou, se o limite não foi atingido
                    if movement_count < max_movements:
                        save_movement_image(output_dir, frame, p1, p2, movement_count)
                        movement_count += 1
                else:
                    # Desenha a ROI de cor azul para pessoas que não se movimentaram
                    cv2.rectangle(frame, p1, p2, get_color('listener'), 2)
            else:
                # Desenha a ROI de cor azul para novas detecções
                cv2.rectangle(frame, p1, p2, get_color('identificate'), 2)

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