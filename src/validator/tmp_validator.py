import os

def tmp_validation(output_dir, video_path):
    # Verifica se o diretório de saída existe, caso contrário, cria-o
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Verifica se o arquivo de vídeo existe
    if not os.path.exists(video_path):
        print(f"Arquivo de vídeo não encontrado: {video_path}")
        exit()

