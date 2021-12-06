import pieces


def log(*, texto, level):

    date = pieces.datetime.datetime.now().strftime("%d.%m.%Y")
    name = 'LogPrimeRobot ' + date + '.txt'
    full_path = pieces.vars.path_logs + "\\" + name + ".txt"

    time = pieces.datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message = f"\n[{level}] {time} -> {texto}"

    if level != "DEBUG":
        print(message)

    if not pieces.os.path.exists(full_path):
        arquivo = open(full_path, 'w', encoding='utf8')
        arquivo.close()

    arquivo = open(full_path, 'a+', encoding='utf8')
    texto = arquivo.readlines()
    texto.append("\n"+message)
    arquivo.writelines(texto)
    arquivo.close()


if __name__ == "__main__":

    log(texto="TESTE",level="INFO")