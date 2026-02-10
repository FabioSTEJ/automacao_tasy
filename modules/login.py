import pyautogui
import time
import config

def identificar_tela_login():
    """
    Apenas verifica se o campo de usuário está visível na tela.
    Isso confirma que o sistema saiu da tela de servidor e carregou o login.
    """
    path_campo = config.IMAGENS.get("USUARIO_LOGIN")
    try:
        pos = pyautogui.locateOnScreen(path_campo, confidence=0.8, grayscale=True)
        return pos is not None
    except Exception:
        return False

def realizar_autenticacao():
    """
    Clica no campo de usuário, digita as credenciais e entra.
    """
    path_campo = config.IMAGENS.get("USUARIO_LOGIN")
    
    try:
        alvo = pyautogui.locateOnScreen(path_campo, confidence=0.8)
        
        if alvo:
            centro = pyautogui.center(alvo)
            print(f"👤 Campo de login encontrado. Preenchendo dados...")
            
            # Clica no campo para garantir o foco
            pyautogui.click(centro)
            time.sleep(0.5)
            
            # Limpa o campo (Garante que não haja lixo no input)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            
            # Digita Usuário
            pyautogui.write(config.USUARIO, interval=0.05)
            
            # Navega para Senha
            pyautogui.press('tab')
            time.sleep(0.3)
            
            # Digita Senha
            pyautogui.write(config.SENHA, interval=0.05)
            
            # Confirma
            pyautogui.press('enter')
            print("🚀 Credenciais enviadas!")
            return True
            
    except Exception as e:
        print(f"⚠️ Erro ao preencher login: {e}")
    
    return False