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

            if not verificador_sistema.tasy_esta_rodando():
                print("[SISTEMA] Tasy não detectado. Iniciando modo Kiosk...")
                verificador_sistema.abrir_tasy_kiosk()
                ultima_fase = None
                continue 

            fase = verificador_sistema.identificar_fase_atual()

            if fase != "DESCONHECIDO" and fase != ultima_fase:
                print(f"--- [DETECTADO]: {fase} ---")
                
                if fase in acoes:
             
                    sucesso = acoes[fase]()
                    
                    if sucesso:
                        # Ação foi bem-sucedida. Travamos a fase para não agir nela de novo imediatamente.
                        ultima_fase = fase
                        
                    else:
                        print(f"[AVISO] Falha na execução de {fase}. Tentando novamente...")
                        ultima_fase = None 
                else:
                    print(f"[ERRO] Fase {fase} sem ação definida.")
                    ultima_fase = fase # Trava para não logar o mesmo erro repetidamente

            elif fase == "AUTO_ATENDIMENTO" and ultima_fase == "AUTO_ATENDIMENTO":
                # [NOVO] Se estamos parados no autoatendimento, verificamos instabilidades.
                if acoes_tasy.monitorar_instabilidade_autoatendimento():
                    print("[SISTEMA] Instabilidade resolvida. Reiniciando ciclo.")
                    ultima_fase = None

            # Lógica de espera para fases que não são finais
            if ultima_fase == fase and fase != "AUTO_ATENDIMENTO" and fase != "DESCONHECIDO":
                 mudou_de_fase = aguardar_mudanca_de_fase(fase_anterior=fase)
                 if not mudou_de_fase:
                      ultima_fase = None # Timeout ocorreu, tentar ação novamente

            elif fase == "DESCONHECIDO":
                print("[ORQUESTRADOR] Fase desconhecida detectada. Iniciando protocolo de verificação.")
                
                # Passo 1: Trazer a janela para o foco como primeira tentativa de correção.
                verificador_sistema.focar_janela_kiosk()
                print("[ORQUESTRADOR] Janela do Kiosk focada. Reavaliando a tela...")
                time.sleep(1) # Pausa para a janela renderizar completamente após o foco.

                # Passo 2: Verificar a fase novamente após focar.
                fase_pos_foco = verificador_sistema.identificar_fase_atual()

                if fase_pos_foco == "DESCONHECIDO":
                    # A tela ainda é desconhecida. Agora iniciamos o período de espera.
                    print("[ORQUESTRADOR] A tela continua desconhecida. Aguardando 15 segundos para confirmar se o erro é persistente...")
                    time.sleep(15)

                    # Passo 3: Verificação final após o período de espera.
                    fase_final = verificador_sistema.identificar_fase_atual()
                    if fase_final == "DESCONHECIDO":
                        print("[ORQUESTRADOR] ERRO PERSISTENTE: A tela continua desconhecida. Salvando evidência.")
                        acoes_tasy.salvar_print_erro()
                    else:
                        print(f"[ORQUESTRADOR] O sistema se recuperou durante a espera para a fase '{fase_final}'. Retomando o fluxo.")
                else:
                    print(f"[ORQUESTRADOR] Problema resolvido com o foco da janela. Nova fase: '{fase_pos_foco}'.")
                ultima_fase = None # Força a reavaliação completa no próximo ciclo.

        except Exception as e:
            print(f"[ERRO CRÍTICO NO MAIN]: {e}")
            time.sleep(5)
            ultima_fase = None

        # Ritmo de vigilância. Um sleep curto para não sobrecarregar a CPU,
        # especialmente quando a fase é estável (ex: AUTO_ATENDIMENTO) ou desconhecida.
        time.sleep(1)

if __name__ == "__main__":
    rodar_robo()