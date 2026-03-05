import pyautogui
import os

def identificar_fase_atual():
    
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    
    pasta_classificador = os.path.join(diretorio_atual, "assets", "classificador")

    if not os.path.exists(pasta_classificador):
        print(f"ERRO: Pasta de classificação não encontrada: {pasta_classificador}")
        return "ERRO_PASTA"

    
    arquivos = [f for f in os.listdir(pasta_classificador) if f.endswith(".png")]

    for arquivo in arquivos:
        caminho_imagem = os.path.join(pasta_classificador, arquivo)

        try:
            posicao = pyautogui.locateOnScreen(caminho_imagem, confidence=0.9)

            if posicao:
                nome_fase = arquivo.replace("fase_", "").replace(".png", "").upper()
                return nome_fase

        except Exception as e:
            continue

    return "DESCONHECIDO"

