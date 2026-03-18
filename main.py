import acoes_tasy
import verificador_sistema
import time

def aguardar_mudanca_de_fase(fase_anterior, timeout=15):
    """
    Aguarda ativamente até que a fase na tela seja diferente da fase anterior.
    Retorna True se a fase mudou, False se o tempo limite foi atingido.
    """
    print(f"[AGUARDANDO] Ação para '{fase_anterior}' concluída. Esperando a tela mudar...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        fase_atual = verificador_sistema.identificar_fase_atual()
        if fase_atual != fase_anterior:
            print(f"[AGUARDANDO] Mudança de tela detectada. Prosseguindo...")
            return True
        time.sleep(0.5) # Verifica a cada meio segundo
    
    print(f"[AVISO] Timeout: A tela permaneceu em '{fase_anterior}' por mais de {timeout} segundos.")
    return False

def rodar_robo():
    print("Monitoramento Blindado 24/7 Iniciado (Modo Totem)...")
    ultima_fase = None

    acoes = {
        "SERVIDOR": acoes_tasy.tratar_fase_servidor,
        "LOGIN": acoes_tasy.tratar_fase_login,
        "GERENCIADOR_SENHA": acoes_tasy.tratar_fase_gerenciamento_senha,
        "CADASTRO_COMPUTADOR": acoes_tasy.tratar_fase_cadastro_computador,
        "AUTO_ATENDIMENTO": acoes_tasy.tratar_fase_auto_atendimento,
        "LOGIN_PROSSEGUIR": acoes_tasy.tratar_fase_login_prosseguir,
        "FUNCAO": acoes_tasy.tratar_fase_funcao,
        "ERRO_SISTEMA": acoes_tasy.tratar_instabilidade_tasy
    }

    while True:
        try:
            # 1. Verificação de Saúde do Sistema
            if not verificador_sistema.tasy_esta_rodando():
                print("[SISTEMA] Tasy não detectado. Iniciando modo Kiosk...")
                verificador_sistema.abrir_tasy_kiosk()
                ultima_fase = None
                continue 

            # 2. Identificação de Estado
            fase = verificador_sistema.identificar_fase_atual()

            # --- NOVO: TRATAMENTO DE TRANSIÇÃO (CARREGANDO) ---
            # Se o Tasy estiver processando, apenas esperamos sem disparar erro.
            if fase == "CARREGANDO":
                print("[SISTEMA] Tasy processando (Carregamento detectado). Aguardando...")
                time.sleep(2)
                continue # Pula para o próximo ciclo sem alterar a 'ultima_fase'
            # --------------------------------------------------

            # 3. Lógica de Ação para Novas Fases
            if fase != "DESCONHECIDO" and fase != ultima_fase:
                print(f"--- [DETECTADO]: {fase} ---")
                
                if fase in acoes:
                    sucesso = acoes[fase]()
                    
                    if sucesso:
                        # Ação foi bem-sucedida. Travamos a fase.
                        ultima_fase = fase
                    else:
                        print(f"[AVISO] Falha na execução de {fase}. Tentando novamente...")
                        ultima_fase = None 
                else:
                    print(f"[ERRO] Fase {fase} sem ação definida.")
                    ultima_fase = fase 

            # 4. Modo Sentinela (Monitoramento de Autoatendimento)
            elif fase == "AUTO_ATENDIMENTO" and ultima_fase == "AUTO_ATENDIMENTO":
                # O robô fica vigiando carregamentos infinitos ou popups de erro
                if acoes_tasy.monitorar_instabilidade_autoatendimento():
                    print("[SISTEMA] Instabilidade detectada e tratada. Reiniciando ciclo de verificação.")
                    ultima_fase = None # Força o robô a reavaliar tudo após o reset

            # 5. Espera Ativa para transições de tela
            if ultima_fase == fase and fase not in ["AUTO_ATENDIMENTO", "DESCONHECIDO"]:
                 mudou_de_fase = aguardar_mudanca_de_fase(fase_anterior=fase)
                 if not mudou_de_fase:
                      ultima_fase = None 

            # 6. Tratamento de Telas Desconhecidas (Protocolo de Recuperação)
            elif fase == "DESCONHECIDO":
                print("[ORQUESTRADOR] Fase desconhecida detectada. Iniciando protocolo de verificação.")
                
                verificador_sistema.focar_janela_kiosk()
                print("[ORQUESTRADOR] Janela do Kiosk focada. Reavaliando a tela...")
                time.sleep(2) 

                fase_pos_foco = verificador_sistema.identificar_fase_atual()

                if fase_pos_foco == "DESCONHECIDO":
                    print("[ORQUESTRADOR] Tela continua desconhecida. Aguardando estabilização (15s)...")
                    time.sleep(15)

                    fase_final = verificador_sistema.identificar_fase_atual()
                    if fase_final == "DESCONHECIDO":
                        print("[ORQUESTRADOR] ERRO PERSISTENTE: Salvando evidência de erro.")
                        acoes_tasy.salvar_print_erro()
                    else:
                        print(f"[ORQUESTRADOR] Recuperação detectada: '{fase_final}'.")
                
                ultima_fase = None 

        except Exception as e:
            print(f"[ERRO CRÍTICO NO MAIN]: {e}")
            time.sleep(5)
            ultima_fase = None

        time.sleep(1)

if __name__ == "__main__":
    rodar_robo()