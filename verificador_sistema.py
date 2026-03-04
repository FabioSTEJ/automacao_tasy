import psutil
import time
import pygetwindow as gw
import pyautogui
import win32gui
import os

# Mantendo suas constantes e padronizando caminhos
NOME_PROCESSO = "msedge.exe" 
TITULO_JANELA = "Tasy" 
URL_TASY = "https://tasy.hospitaldecirurgia.com.br/#/"
NOME_ARQUIVO_ABA = "botao_aba_tasy.png" # Nome exato que você mencionou

def tasy_esta_rodando():
    """Verifica processos e janelas ignorando o VS Code."""
    print(f"[SISTEMA] Verificando se o Edge e a aba '{TITULO_JANELA}' estão ativos...")
    
    # Verificação de processo otimizada
    navegador_aberto = any(NOME_PROCESSO.lower() in p.info['name'].lower() 
                          for p in psutil.process_iter(['name']) if p.info['name'])

    if not navegador_aberto:
        print(f"[SISTEMA] Aviso: O Microsoft Edge não está em execução.")
        return False

    # Filtro para evitar que o VS Code se passe pelo Tasy
    janelas = [j for j in gw.getWindowsWithTitle(TITULO_JANELA) 
               if "visual studio code" not in j.title.lower()]
    
    if janelas:
        print(f"[SISTEMA] Sucesso: Aba '{TITULO_JANELA}' identificada.")
        return True
    
    print(f"[SISTEMA] Edge aberto, mas a aba '{TITULO_JANELA}' não foi encontrada.")
    return False

def focar_janela():
    """Localiza a aba via imagem usando o caminho relativo correto do seu projeto."""
    print(f"[AÇÃO] Buscando aba do Tasy via reconhecimento de imagem...")
    
    # 1. Construção do caminho conforme sua estrutura: assets/botoes/
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_botao = os.path.join(diretorio_atual, "assets", "botoes", NOME_ARQUIVO_ABA)
    
    # 2. Traz o Edge para frente (preparação para o clique)
    janelas_edge = [j for j in gw.getWindowsWithTitle("Microsoft Edge") 
                    if "visual studio code" not in j.title.lower()]
    if janelas_edge:
        try:
            edge = janelas_edge[0]
            if edge.isMinimized: edge.restore()
            edge.activate()
            time.sleep(0.8) # Tempo para renderização em duas telas
        except:
            pass

    # 3. Reconhecimento Visual
    try:
        # Usando locateCenterOnScreen para clique direto, com confiança ajustada
        ponto = pyautogui.locateCenterOnScreen(caminho_botao, confidence=0.8)
        
        if ponto:
            print(f"[SUCESSO] Aba Tasy encontrada. Forçando foco...")
            # Clica para garantir que o Windows mude o foco do teclado (Input Focus)
            pyautogui.click(ponto)
            time.sleep(0.5)
            
            # 4. Verificação final: o teclado está no lugar certo?
            hwnd_ativo = win32gui.GetForegroundWindow()
            titulo_ativo = win32gui.GetWindowText(hwnd_ativo)
            
            if "visual studio code" not in titulo_ativo.lower():
                print(f"[FOCO] Confirmado em: {titulo_ativo}. Aplicando F11...")
                pyautogui.press('f11')
                return True
            else:
                print("[AVISO] O clique ocorreu, mas o VS Code ainda retém o foco.")
                return False
        else:
            print(f"[AVISO] Botão '{NOME_ARQUIVO_ABA}' não visível. Tentando Ctrl+Tab...")
            pyautogui.hotkey('ctrl', 'tab')
            return False
            
    except Exception as e:
        print(f"[ERRO] Falha no reconhecimento de imagem: {e}")
        return False

def abrir_tasy():
    """Abre o Edge em modo Kiosk Nativo."""
    print(f"[SISTEMA] Iniciando Edge em Modo Kiosk: {URL_TASY}")
    try:
        os.system(f'start msedge --kiosk {URL_TASY} --edge-kiosk-type=fullscreen')
        time.sleep(10)
    except Exception as e:
        print(f"[ERRO] Falha ao abrir no modo Kiosk: {e}")