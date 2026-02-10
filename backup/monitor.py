import pyautogui
import os

CAMINHO_IMAGEM = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'menu.png')

print("--- VALIDANDO RECORTE ---")
try:
    # Procurando o seu recorte na tela
    posicao = pyautogui.locateOnScreen(CAMINHO_IMAGEM, confidence=0.8)
    
    if posicao:
        print(f"✅ SUCESSO! O Python encontrou o ícone em: {posicao}")
        # O mouse vai dar um "oi" no ícone
        pyautogui.moveTo(posicao)
    else:
        print("❌ Ainda não encontrou. Verifique se o ícone está visível no monitor principal.")

except Exception as e:
    print(f"Erro: {e}")