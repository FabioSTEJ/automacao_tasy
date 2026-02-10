import time
import ctypes
from modules import autenticacao
from modules import login

# Garante que o Windows não mude a escala das imagens
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

def executar_robo():
    print("🤖 Robô Tasy Iniciado. Monitorando telas...")
    
    while True:
        # 1. VERIFICA SE ESTÁ NA TELA DE SERVIDOR
        if autenticacao.identificar_tela_servidor():
            print("📍 Estado detectado: Seleção de Servidor.")
            autenticacao.executar_acesso_servidor()
        
        # 2. VERIFICA SE ESTÁ NA TELA DE LOGIN
        elif login.identificar_tela_login():
            print("📍 Estado detectado: Tela de Login.")
            if login.realizar_autenticacao():
                print("✅ Processo de autenticação concluído.")
                break # Para o loop após logar com sucesso
        
        else:
            # Caso não veja nada conhecido, apenas aguarda
            print("🔍 Aguardando interface conhecida...", end="\r")
        
        time.sleep(1)

if __name__ == "__main__":
    executar_robo()