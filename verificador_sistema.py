import os
import time
import psutil
import pygetwindow as gw
import identificador_fase

URL_TASY = "https://tasy.hospitaldecirurgia.com.br/#/"

_ultima_fase_logada = None
_contador_logs = 0

_falhas_consecutivas = 0
LIMITE_FALHAS = 3

def tasy_esta_rodando():

    global _ultima_fase_logada, _contador_logs, _falhas_consecutivas

    processo_ativo = any("msedge.exe" in p.name().lower() for p in psutil.process_iter())
    
    if not processo_ativo:
        _falhas_consecutivas = 0
        print("[VERIFICADOR] Processo msedge.exe não encontrado.")
        return False

    fase_atual = identificador_fase.identificar_fase_atual()
    
    if fase_atual not in ("DESCONHECIDO", "ERRO_PASTA"):
        _falhas_consecutivas = 0 
        
        if fase_atual == _ultima_fase_logada:
            _contador_logs += 1
        else:
            _ultima_fase_logada = fase_atual
            _contador_logs = 1

        if _contador_logs <= 5:
            print(f"[VERIFICADOR] Tasy confirmado visualmente na fase: {fase_atual}")
        elif _contador_logs == 6:
            print("[VERIFICADOR] Sistema estável. Monitorando em silêncio...")
            
        return True
    
    _falhas_consecutivas += 1
    
    if _falhas_consecutivas < LIMITE_FALHAS:

        print(f"[AVISO] Tasy em fase desconhecida. Tentativa {_falhas_consecutivas}/{LIMITE_FALHAS}...")
        return True 
    else:

        print(f"[CRÍTICO] Tasy não detectado visualmente após {LIMITE_FALHAS} tentativas.")
        _falhas_consecutivas = 0  # Reseta para o próximo ciclo
        return False

def abrir_tasy_kiosk():

    print("[SISTEMA] Disparando comando Kiosk...")
    comando = f'start msedge --kiosk {URL_TASY} --edge-kiosk-type=fullscreen'
    os.system(comando)
    print("[SISTEMA] Aguardando carregamento...")
    time.sleep(15)

def focar_janela_kiosk():

    try:
        janelas = gw.getWindowsWithTitle("Microsoft Edge")
        if not janelas:
            janelas = gw.getAllWindows()
            
        for j in janelas:
            if "edge" in j.title.lower() or j.title == "":
                if j.isMinimized:
                    j.restore()
                j.activate()
                break
    except:
        pass

def identificar_fase_atual():
    """Wrapper para retornar a fase atual identificada."""
    return identificador_fase.identificar_fase_atual()