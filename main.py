import identificador_fase
import acoes_tasy
import verificador_sistema
import time


def rodar_robo():
    print("Iniciando monitoramento do Tasy...")
    ultima_fase = None
    contador_desconhecido = 0

    while True:
        
        fase = identificador_fase.identificar_fase_atual()

        
        if fase != "DESCONHECIDO" and fase != ultima_fase:
            print(f"--- Entrando na fase: {fase} ---")
            ultima_fase = fase
            contador_desconhecido = 0

            if fase == "SERVIDOR":
                acoes_tasy.tratar_fase_servidor()
            elif fase == "LOGIN":
                acoes_tasy.tratar_fase_login()
            elif fase == "GERENCIADOR_SENHA":
                acoes_tasy.tratar_fase_gerenciamento_senha()
                print("[INFO] Aguardando transição para o Autoatendimento...")
                time.sleep(5)
            elif fase == "AUTO_ATENDIMENTO":
                acoes_tasy.tratar_fase_auto_atendimento()
            elif fase == "LOGIN_PROSSEGUIR":
                acoes_tasy.tratar_fase_login_prosseguir()
                ultima_fase = fase
                print("Aguardando 3 segundos para o Tasy processar o login...")
                time.sleep(3)
            elif fase == "FUNCAO":
                acoes_tasy.tratar_fase_funcao()
            elif fase == "ERRO_SISTEMA":
                acoes_tasy.tratar_instabilidade_tasy()

        
        elif fase == "DESCONHECIDO":
            contador_desconhecido += 1
            print(f"[INFO] Fase desconhecida. Tentativa de reconhecimento {contador_desconhecido}/10...")
            
            
            if contador_desconhecido == 10:
                print("[ALERTA] Tempo limite atingido sem reconhecimento. Capturando tela...")
                acoes_tasy.salvar_print_erro()

            if not verificador_sistema.tasy_esta_rodando():
                print("[INFO] Aplicativo TasyNative não encontrado. Solicitando abertura...")
                verificador_sistema.abrir_tasy()
                ultima_fase = None 
            else:
                verificador_sistema.focar_janela()

        time.sleep(2.5)


if __name__ == "__main__":
    rodar_robo()