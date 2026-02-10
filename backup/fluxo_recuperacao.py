import pyautogui
import os
import time

# --- CONFIGURAÇÃO ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGENS = {
    "USUARIO_CONECTADO": os.path.join(BASE_DIR, 'usuario_conectado.png'),
    "BOTAO_OK_AVISO":    os.path.join(BASE_DIR, 'botao_ok_aviso.png'),
    "SERVIDOR":          os.path.join(BASE_DIR, 'passo1_alvo_servidor.png'),
    "CAMPO_USER":        os.path.join(BASE_DIR, 'passo2_campo_usuario.png'),
    "MENU_OK":           os.path.join(BASE_DIR, 'menu.png') 
}

USUARIO = "automacao"
SENHA = "12345678a"

def analisar_prioridade():
    """Analisa a tela e retorna APENAS o estado mais importante detectado"""
    # A ordem desta lista define a importância (Hierarquia)
    ordem_importancia = [
        "USUARIO_CONECTADO", 
        "BOTAO_OK_AVISO", 
        "MENU_OK", 
        "SERVIDOR", 
        "CAMPO_USER"
    ]
    
    for estado in ordem_importancia:
        try:
            if pyautogui.locateOnScreen(IMAGENS[estado], confidence=0.8, grayscale=True):
                return estado
        except:
            continue
    return None

def rodar_inteligencia():
    print("🧠 Cérebro ativo. Decidindo ação única...")
    
    while True:
        # O robô decide qual é a ÚNICA prioridade agora
        estado_atual = analisar_prioridade()
        print(f"🎯 Decisão atual: {estado_atual if estado_atual else 'Aguardando mudança na tela...'}")

        # 1. TRATAR AVISO (BLOQUEIO TOTAL)
        if estado_atual in ["USUARIO_CONECTADO", "BOTAO_OK_AVISO"]:
            print("⚠️ Bloqueio detectado: Limpando aviso de sessão...")
            alvo = IMAGENS["BOTAO_OK_AVISO"] 
            pos = pyautogui.locateOnScreen(alvo, confidence=0.7)
            if pos:
                centro = pyautogui.center(pos)
                pyautogui.click(centro)
                time.sleep(0.5)
                pyautogui.press('enter')
            time.sleep(2) # Pausa para a tela atualizar

        # 2. SE JÁ ESTIVER LOGADO
        elif estado_atual == "MENU_OK":
            print("✅ Sistema pronto. Monitorando estabilidade...")
            time.sleep(10)

        # 3. SE PRECISAR CLICAR NO SERVIDOR
        elif estado_atual == "SERVIDOR":
            print("📍 Ação: Acessando servidor...")
            pos = pyautogui.locateOnScreen(IMAGENS["SERVIDOR"], confidence=0.8)
            if pos:
                pyautogui.click(pos)
            time.sleep(3)

        # 4. SE PRECISAR FAZER LOGIN
        elif estado_atual == "CAMPO_USER":
            print("📍 Ação: Realizando login...")
            pos = pyautogui.locateOnScreen(IMAGENS["CAMPO_USER"], confidence=0.8)
            if pos:
                pyautogui.click(pos)
                time.sleep(0.5)
                # Garante que o campo esteja limpo
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('backspace')
                pyautogui.write(USUARIO, interval=0.05)
                pyautogui.press('tab')
                time.sleep(0.2)
                pyautogui.write(SENHA, interval=0.05)
                pyautogui.press('enter')
            time.sleep(5)

        time.sleep(2) # Pequeno intervalo entre pensamentos

if __name__ == "__main__":
    rodar_inteligencia()