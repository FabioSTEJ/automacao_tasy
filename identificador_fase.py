import pyautogui
import os

def verificar_elemento(nome_arquivo, confiança=0.8, subpasta="botoes"):
    """
    Verifica se um elemento (imagem) específico está visível na tela.
    Usa a pasta 'botoes' como padrão, mas permite especificar outra (ex: 'classificador').
    Retorna True se encontrado, False caso contrário.
    """
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_imagem = os.path.join(diretorio_atual, "assets", subpasta, nome_arquivo)

    if not os.path.exists(caminho_imagem):
        return False # Retorna False silenciosamente se o arquivo de imagem não existir.

    try:
        if pyautogui.locateOnScreen(caminho_imagem, confidence=confiança):
            return True
    except (pyautogui.PyAutoGUIException, FileNotFoundError):
        pass # Ignora se a imagem não for encontrada ou houver erro de screenshot
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
            posicao = pyautogui.locateOnScreen(caminho_imagem, confidence=0.9)

            if posicao:
                nome_fase = arquivo.replace("fase_", "").replace(".png", "").upper()
                return nome_fase

        except Exception as e:
            continue

    return "DESCONHECIDO"
