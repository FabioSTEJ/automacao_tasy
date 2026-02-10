import pyautogui
import time
import os

# Configuração de caminho
DIRETORIO = os.path.dirname(os.path.abspath(__file__))
NOME_ARQUIVO = os.path.join(DIRETORIO, 'passo1_servidor.png')

def capturar_tela_servidor():
    print("--- PREPARAÇÃO PARA CAPTURA ---")
    print("Você tem 5 segundos para colocar o Tasy na tela de seleção de servidor.")
    
    for i in range(5, 0, -1):
        print(f"Capturando em {i}...")
        time.sleep(1)
    
    # Tira o print do monitor principal
    print("📸 Capturando...")
    screenshot = pyautogui.screenshot()
    
    # Salva o arquivo
    screenshot.save(NOME_ARQUIVO)
    
    print("-" * 30)
    print(f"✅ Sucesso! Imagem salva como: {NOME_ARQUIVO}")
    print("DICA: Abra a imagem e verifique se o servidor desejado aparece claramente.")
    print("-" * 30)

if __name__ == "__main__":
    capturar_tela_servidor()