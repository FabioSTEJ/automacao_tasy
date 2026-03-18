import os
import time
import psutil
import pygetwindow as gw
import identificador_fase

URL_TASY = "https://tasy.hospitaldecirurgia.com.br/#/"

# Variáveis globais para controle de log repetitivo
_ultima_fase_logada = None
_contador_logs = 0

# --- NOVO: Variáveis para controle de tolerância ---
_falhas_consecutivas = 0
LIMITE_FALHAS = 3  # O robô tentará ver o Tasy 3 vezes antes de desistir

def tasy_esta_rodando():
    global _ultima_fase_logada, _contador_logs, _falhas_consecutivas
    """
    Verificação robusta:
    1. O processo msedge.exe existe?
    2. O Identificador de Fase consegue ver alguma imagem do Tasy?
    (Com tolerância a falhas momentâneas de reconhecimento visual)
    """
    
    # Passo 1: O processo existe no Windows?
    processo_ativo = any("msedge.exe" in p.name().lower() for p in psutil.process_iter())
    
    if not processo_ativo:
        _falhas_consecutivas = 0  # Reseta se o navegador nem aberto estiver
        print("[VERIFICADOR] Processo msedge.exe não encontrado.")
        return False

    # Passo 2: Verificação Visual (O que o robô vê)
    fase_atual = identificador_fase.identificar_fase_atual()
    
    # Se o identificador encontrou QUALQUER fase conhecida:
    if fase_atual != "DESCONHECIDO" and fase_atual != "ERRO_PASTA":
        _falhas_consecutivas = 0  # SUCESSO! Reseta o contador de falhas
        
        # Lógica de controle de log (Silenciar após 5 mensagens iguais)
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
    
    # --- LÓGICA DE TOLERÂNCIA ---
    # Se chegou aqui, a fase é "DESCONHECIDO", mas o processo Edge ainda existe.
    _falhas_consecutivas += 1
    
    if _falhas_consecutivas < LIMITE_FALHAS:
        # Ainda estamos dentro da margem de erro. 
        # Reportamos que o Tasy "está rodando" para evitar que o main abra o Kiosk.
        print(f"[AVISO] Tasy em fase desconhecida. Tentativa {_falhas_consecutivas}/{LIMITE_FALHAS}...")
        return True 
    else:
        # Se ultrapassou o limite, o Tasy provavelmente travou em tela branca ou fechou.
        print(f"[CRÍTICO] Tasy não detectado visualmente após {LIMITE_FALHAS} tentativas.")
        _falhas_consecutivas = 0  # Reseta para o próximo ciclo
        return False

def abrir_tasy_kiosk():
    """Abre o Edge forçando o modo Kiosk."""
    print("[SISTEMA] Disparando comando Kiosk...")
    comando = f'start msedge --kiosk {URL_TASY} --edge-kiosk-type=fullscreen'
    os.system(comando)
    print("[SISTEMA] Aguardando carregamento...")
    time.sleep(15) # Tempo de rede do Totem

def focar_janela_kiosk():
    """Tenta trazer qualquer janela do Edge para frente."""
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