import cv2
import os

# Função para salvar a imagem da pessoa que se movimentou
def save_movement_image(output_dir, frame, p1, p2, count):
    roi = frame[p1[1]:p2[1], p1[0]:p2[0]]
    filename = os.path.join(output_dir, f'movement_{count}.png')
    cv2.imwrite(filename, roi)
    print(f"Imagem salva: {filename}")