import identificador_fase
import acoes_tasy
import verificador_sistema
import time

def rodar_robo():
    print("Monitoramento Blindado 24/7 Iniciado...")
    ultima_fase = None
    
    # Dicionário que mapeia o nome da fase para a função que deve ser executada
    # Isso torna o código limpo e fácil de expandir
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
            fase = identificador_fase.identificar_fase_atual()

            # Se a fase é conhecida e é diferente da última (ou se a última falhou)
            if fase != "DESCONHECIDO" and fase != ultima_fase:
                print(f"--- [DETECTADO]: {fase} ---")
                
                # Verifica se temos uma ação programada para essa fase
                if fase in acoes:
                    # EXECUÇÃO COM VALIDAÇÃO:
                    # Chamamos a função e ela nos diz se funcionou (True/False)
                    executou_com_sucesso = acoes[fase]()

                    if executou_com_sucesso:
                        print(f"[OK] Fase {fase} concluída com sucesso.")
                        ultima_fase = fase # Só trava a fase se deu certo
                    else:
                        print(f"[AVISO] Falha ao executar {fase}. Tentando novamente...")
                        ultima_fase = None # Força a tentativa no próximo ciclo
                else:
                    print(f"[ERRO] Fase {fase} identificada, mas sem ação definida no dicionário.")

            elif fase == "DESCONHECIDO":
                # Lógica de recuperação (abrir Tasy, focar janela, etc)
                if not verificador_sistema.tasy_esta_rodando():
                    verificador_sistema.abrir_tasy()
                    ultima_fase = None
                else:
                    verificador_sistema.focar_janela()

        except Exception as e:
            print(f"[ERRO CRÍTICO]: {e}")
            ultima_fase = None # Reset total em caso de erro
            time.sleep(5)

        time.sleep(2.5) # Ritmo de vigilância

if __name__ == "__main__":
    rodar_robo()