import pyautogui
import time
import config

def identificar_tela_servidor():
    """
    Apenas verifica se o sistema está na tela de seleção de servidor.
    Retorna True ou False sem realizar ações.
    """
    path_tela = config.IMAGENS.get("TELA_SERVIDOR")
    try:
        # Busca a âncora visual da tela do servidor
        pos = pyautogui.locateOnScreen(path_tela, confidence=0.8, grayscale=True)
        return pos is not None
    except Exception:
        return False

def executar_acesso_servidor():
    """
    Realiza o clique no servidor alvo após confirmar que a tela está correta.
    """
    path_tela = config.IMAGENS.get("TELA_SERVIDOR")
    path_click = config.IMAGENS.get("CLICK_SERVIDOR")
    
    try:
        # 1. Valida se a tela do servidor ainda está visível
        if pyautogui.locateOnScreen(path_tela, confidence=0.8, grayscale=True):
            
            # 2. Busca o ponto exato onde o clique deve ocorrer (click_servidor.png)
            alvo = pyautogui.locateOnScreen(path_click, confidence=0.8)
            
            if alvo:
                centro = pyautogui.center(alvo)
                print(f"\n🎯 Alvo de clique encontrado! Clicando em: {centro}")
                
                # Move o mouse suavemente e clica
                pyautogui.moveTo(centro, duration=0.5)
                pyautogui.click()
                
                # Aguarda o tempo de resposta do sistema
                time.sleep(1.5)
                return True
            else:
                print("\n⚠️ Tela detectada, mas o alvo específico de clique não foi encontrado.")
                
    except Exception as e:
        print(f"\n⚠️ Erro ao tentar acessar o servidor: {e}")
        
    return False