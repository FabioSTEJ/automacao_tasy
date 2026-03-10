import identificador_fase
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
        fase_atual = identificador_fase.identificar_fase_atual()
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

            fase = identificador_fase.identificar_fase_atual()

            if fase != "DESCONHECIDO" and fase != ultima_fase:
                print(f"--- [DETECTADO]: {fase} ---")
                
                if fase in acoes:
             
                    sucesso = acoes[fase]()
                    
                    if sucesso:
                        # Ação foi bem-sucedida. Travamos a fase para não agir nela de novo imediatamente.
                        ultima_fase = fase

                        # A fase 'AUTO_ATENDIMENTO' é um estado final de monitoramento.
                        # Não esperamos uma mudança, apenas continuamos o loop de verificação.
                        if fase != "AUTO_ATENDIMENTO":
                            # Para outras fases, esperamos ativamente a transição de tela.
                            mudou_de_fase = aguardar_mudanca_de_fase(fase_anterior=fase)
                            if not mudou_de_fase:
                                # Se a tela não mudou (timeout), algo pode ter travado.
                                # Resetamos ultima_fase para forçar uma nova tentativa da ação no próximo ciclo.
                                ultima_fase = None
                    else:
                        print(f"[AVISO] Falha na execução de {fase}. Tentando novamente...")
                        ultima_fase = None 
                else:
                    print(f"[ERRO] Fase {fase} sem ação definida.")
                    ultima_fase = fase # Trava para não logar o mesmo erro repetidamente

            elif fase == "DESCONHECIDO":
                verificador_sistema.focar_janela_kiosk()
                if ultima_fase is not None:
                    print("[INFO] Tela desconhecida detectada. Resetando estado para reavaliação.")
                    ultima_fase = None

        except Exception as e:
            print(f"[ERRO CRÍTICO NO MAIN]: {e}")
            time.sleep(5)
            ultima_fase = None

        # Ritmo de vigilância. Um sleep curto para não sobrecarregar a CPU,
        # especialmente quando a fase é estável (ex: AUTO_ATENDIMENTO) ou desconhecida.
        time.sleep(1)

if __name__ == "__main__":
    rodar_robo()