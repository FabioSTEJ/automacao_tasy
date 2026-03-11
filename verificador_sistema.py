import os
import time
import psutil
import pygetwindow as gw
import identificador_fase

URL_TASY = "https://tasy.hospitaldecirurgia.com.br/#/"

def tasy_esta_rodando():
    """
    Verificação robusta:
    1. O processo msedge.exe existe?
    2. O Identificador de Fase consegue ver alguma imagem do Tasy?
    """
    # Passo 1: O processo existe? (Checagem rápida)
    processo_ativo = any("msedge.exe" in p.name().lower() for p in psutil.process_iter())
    
    if not processo_ativo:
        print("[VERIFICADOR] Processo msedge.exe não encontrado.")
        return False

    # Passo 2: O Identificador consegue ver as telas iniciais?
    # Se o Edge estiver aberto (mesmo que em segundo plano), 
    # o pyautogui tentará achar as imagens de LOGIN ou CARREGANDO.
    fase_atual = identificador_fase.identificar_fase_atual()
    
    # Se o identificador encontrou QUALQUER fase conhecida, significa que o Tasy está visível.
    if fase_atual != "DESCONHECIDO" and fase_atual != "ERRO_PASTA":
        print(f"[VERIFICADOR] Tasy confirmado visualmente na fase: {fase_atual}")
        return True
        
    print(f"[VERIFICADOR] Processo Edge existe, mas nenhuma tela conhecida do Tasy é visível (Fase atual: {fase_atual})")
    return False

def abrir_tasy_kiosk():
    """Abre o Edge forçando o modo Kiosk."""
    print("[SISTEMA] Disparando comando Kiosk...")
    # Usamos o comando que você validou que funciona
    comando = f'start msedge --kiosk {URL_TASY} --edge-kiosk-type=fullscreen'
    os.system(comando)
    print("[SISTEMA] Aguardando carregamento...")
    time.sleep(15) # Tempo maior para o Totem carregar a rede

def focar_janela_kiosk():
    """Tenta trazer qualquer janela do Edge para frente."""
    try:
        janelas = gw.getWindowsWithTitle("Microsoft Edge")
        if not janelas:
            # No modo Kiosk o título pode mudar, tentamos pegar a janela ativa
            janelas = gw.getAllWindows()
            
        for j in janelas:
            if "edge" in j.title.lower() or j.title == "": # Kiosk às vezes tem título vazio
                if j.isMinimized:
                    j.restore()
                j.activate()
                break
    except:
        pass

def identificar_fase_atual():
    """Wrapper para retornar a fase atual identificada, desacoplando o main do identificador direto."""
    return identificador_fase.identificar_fase_atual()