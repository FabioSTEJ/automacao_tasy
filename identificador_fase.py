import pyautogui
import os
from contextlib import suppress

def verificar_elemento(nome_arquivo, confiança=0.8, subpasta="botoes"):

    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_imagem = os.path.join(diretorio_atual, "assets", subpasta, nome_arquivo)

    if not os.path.exists(caminho_imagem):
        return False

    with suppress(pyautogui.PyAutoGUIException, FileNotFoundError):
        if pyautogui.locateOnScreen(caminho_imagem, confidence=confiança):
            return True
    return False

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
            if posicao := pyautogui.locateOnScreen(caminho_imagem, confidence=0.9):
                return arquivo.replace("fase_", "").replace(".png", "").upper()

        except Exception as e:
            continue

    return "DESCONHECIDO"
