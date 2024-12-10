import cv2
import os

video_path = 'src/persons.mp4'

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

# Lê o primeiro frame do vídeo
ret, frame = cap.read()
if not ret:
    print("Não foi possível ler o primeiro frame")
    exit()

# Seleciona a região de interesse (ROI) para o tracking
bbox = cv2.selectROI(frame, False)

# Inicializa o tracker
tracker = cv2.TrackerKCF_create()
tracker.init(frame, bbox)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Atualiza o tracker
    ret, bbox = tracker.update(frame)

    if ret:
        # Desenha o bounding box
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    else:
        # Tracking falhou
        cv2.putText(frame, "Tracking falhou", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Mostra o frame
    cv2.imshow('Tracking', frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera o objeto de captura e fecha todas as janelas
cap.release()
cv2.destroyAllWindows()