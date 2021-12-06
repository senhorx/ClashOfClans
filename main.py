import pieces


def main():
    #Diretórios que serão usados no robô
    path_files = pieces.vars.path_files
    path_excel = pieces.vars.path_excel
    path_logs = pieces.vars.path_logs

    # Verificando se a pasta Files existe
    if not pieces.os.path.exists(path_files):
        pieces.os.mkdir(path_files)

    # Verificando se a pasta Excel existe
    if not pieces.os.path.exists(path_excel):
        pieces.os.mkdir(path_excel)

    # Verificando se a pasta Logs existe
    if not pieces.os.path.exists(path_logs):
        pieces.os.mkdir(path_logs)

    #Variáveis que serão usadas no robo
    email = pieces.vars.email
    password = pieces.vars.password
    name_cla = pieces.vars.name_cla
    tag_cla = pieces.vars.tag_cla

    # Verificando se o email está preenchido
    if email == "":
        pieces.log(texto=f"[End Func] -> Main: Email está vazio. Insira no arquivo vars.py", level="ERRO")
        return -1

    # Verificando se a senha está preenchida
    if password == "":
        pieces.log(texto=f"[End Func] -> Main: Senha está vazio. Insira no arquivo vars.py", level="ERRO")
        return -1

    # Verificando se o nome do clã está preenchido
    if name_cla == "":
        pieces.log(texto=f"[End Func] -> Main: Nome do clã está vazio. Insira no arquivo vars.py", level="ERRO")
        return -1

    # Verificando se a tag do clã está preenchida
    if tag_cla == "":
        pieces.log(texto=f"[End Func] -> Main: Tag do clã está vazio. Insira no arquivo vars.py", level="ERRO")
        return -1

    # Verificando os retornos da função principal
    clash_royale = pieces.clash_royale()
    if clash_royale == 0:
        pieces.log(texto=f"[End Func] -> Main: Robô foi executado com sucesso", level="DEBUG")
    elif clash_royale == -1:
        pieces.log(texto=f"[End Func] -> Main: Login não foi efetuado", level="ERRO")
        return -2
    elif clash_royale == -2:
        pieces.log(texto=f"[End Func] -> Main: IP público não foi encontrado", level="ERRO")
        return -2
    elif clash_royale == -3:
        pieces.log(texto=f"[End Func] -> Main: Key da API não foi criada", level="ERRO")
        return -2
    elif clash_royale == -4:
        pieces.log(texto=f"[End Func] -> Main: Não foi possível carregar o token", level="ERRO")
        return -2
    elif clash_royale == -5:
        pieces.log(texto=f"[End Func] -> Main: Tag do Clã não foi capturada", level="ERRO")
        return -2
    elif clash_royale == -6:
        pieces.log(texto=f"[End Func] -> Main: Excel do membros do clã nao foi criado", level="ERRO")
        return -2
    else:
        pieces.log(texto=f"[End Func] -> Main: Erro nao mapeado", level="ERRO")
        return -2


if __name__ ==  "__main__":
    main()