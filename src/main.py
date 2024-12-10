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

# Inicializa o detector de pessoas
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detecta pessoas no frame
    boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))

    # Desenha os bounding boxes ao redor das pessoas detectadas
    for (x, y, w, h) in boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Mostra o frame
    cv2.imshow('Detecção de Pessoas', frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera o objeto de captura e fecha todas as janelas
cap.release()
cv2.destroyAllWindows()