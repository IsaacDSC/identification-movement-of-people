import cv2
import os
import asyncio
import websockets
import json

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

# Variável de controle para start/stop
processando = True

async def process_video():
    global processando
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fim do vídeo ou erro ao ler o frame.")
            break

        if processando:
            # Detecta pessoas no frame
            boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))

            # Desenha os bounding boxes ao redor das pessoas detectadas
            for (x, y, w, h) in boxes:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Mostra o frame
        cv2.imshow('Detecção de Pessoas', frame)

        # Controle de teclas
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Pressione 'q' para sair
            print("Tecla 'q' pressionada. Encerrando processamento de vídeo.")
            break

        await asyncio.sleep(0.01)  # Permite que o loop de eventos do asyncio processe outras tarefas

    # Libera o objeto de captura e fecha todas as janelas
    cap.release()
    cv2.destroyAllWindows()

async def control(websocket):
    global processando
    print("Cliente conectado ao WebSocket")
    try:
        async for message in websocket:
            data = json.loads(message)
            print(data)
            if data.get("command") == "toggle":
                processando = not processando
                print(f"Processamento {'ativado' if processando else 'pausado'}")
            elif data.get("command") == "stop":
                print("Comando 'stop' recebido. Encerrando servidor WebSocket.")
                break
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Conexão WebSocket encerrada: {e}")
    await websocket.send(message)

async def main():
    # Inicia o servidor de controle
    async with websockets.serve(control, "localhost", 8766):
        print("Iniciando servidor WebSocket...")
        await asyncio.gather(
            process_video()
        )
        print("Servidor WebSocket iniciado na porta 8766")

# Executa o loop principal
asyncio.run(main())