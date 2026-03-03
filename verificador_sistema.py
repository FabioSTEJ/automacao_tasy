import psutil
import subprocess
import time
import pygetwindow as gw
import os

NOME_PROCESSO = "TasyNative.exe"
CAMINHO_EXECUTAVEL = r"C:\Program Files\Philips EMR\TasyNative\TasyNative.exe"
TITULO_JANELA = "Tasy"

def tasy_esta_rodando():

    print(f"[SISTEMA] Verificando se o processo '{NOME_PROCESSO}' está ativo...")
    for proc in psutil.process_iter(['name']):
        try:
            if NOME_PROCESSO.lower() in proc.info['name'].lower():
                print(f"[SISTEMA] Sucesso: Processo '{NOME_PROCESSO}' encontrado.")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    print(f"[SISTEMA] Aviso: O processo '{NOME_PROCESSO}' não foi detectado nos processos do Windows.")
    return False

def focar_janela():

    print(f"[AÇÃO] Verificando foco da janela: '{TITULO_JANELA}'...")
    

    janelas = gw.getWindowsWithTitle(TITULO_JANELA)
    
    if janelas:
        janela = janelas[0]
        try:

            if janela.isMinimized:
                print(f"[AÇÃO] Janela minimizada detectada. Restaurando...")
                janela.restore()
                time.sleep(0.5)


            janela.activate()
            print(f"[AÇÃO] Janela '{TITULO_JANELA}' trazida para o primeiro plano.")
            return True
        except Exception as e:
            print(f"[AVISO] Falha ao focar janela: {e}. O Windows pode estar bloqueando o foco.")
            return False
    
    print(f"[AVISO] Janela '{TITULO_JANELA}' não encontrada para focar.")
    return False

def abrir_tasy():

    print(f"[SISTEMA] Iniciando a abertura do executável em: {CAMINHO_EXECUTAVEL}")
    try:
        subprocess.Popen(CAMINHO_EXECUTAVEL)
        print(f"[SISTEMA] Comando enviado. Aguardando 10 segundos para o carregamento inicial...")
        time.sleep(10)
    except Exception as e:
        print(f"[ERRO] Falha ao tentar abrir o TasyNative: {e}")