import identificador_fase
import acoes_tasy
import time


def rodar_robo():
    print("Iniciando monitoramento do Tasy...")
    ultima_fase = None

    while True:
        # 1. O Identificador diz qual é a tela atual
        fase = identificador_fase.identificar_fase_atual()

        # 2. Se a fase mudou, executamos a ação correspondente
        if fase != "DESCONHECIDO" and fase != ultima_fase:
            print(f"--- Entrando na fase: {fase} ---")
            ultima_fase = fase

            if fase == "SERVIDOR":
                acoes_tasy.tratar_fase_servidor()
                

            elif fase == "LOGIN":
                acoes_tasy.tratar_fase_login()
                
            
            elif fase == "GERENCIADOR_SENHA":
                acoes_tasy.tratar_fase_gerenciamento_senha()
                
            
            elif fase == "AUTO_ATENDIMENTO":
                acoes_tasy.tratar_fase_auto_atendimento()
                
            elif fase == "LOGIN_PROSSEGUIR":
                acoes_tasy.tratar_fase_login_prosseguir()
                ultima_fase = fase
                print("Aguardando 3 segundos para o Tasy processar o login...")
                time.sleep(3)
                
            elif fase == "FUNCAO":
                acoes_tasy.tratar_fase_funcao()
                

            # CASO O TASY EXIBA UMA TELA DE ERRO (você precisaria do print dela)
            elif fase == "ERRO_SISTEMA":
                acoes_tasy.tratar_instabilidade_tasy()

        time.sleep(1.5)


if __name__ == "__main__":
    rodar_robo()
