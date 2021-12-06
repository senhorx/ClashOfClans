import pieces


def clash_royale():
    pieces.log(texto=f"[Func] -> clash_royale", level="DEBUG")
    driver = pieces.lib_web.iniciar_web_driver()

    #URL de Login
    url_login = pieces.vars.url_clash_royale
    #URL API
    url_api_clans = pieces.vars.urlurl_api_clash_royale_clans
    # URL de IP
    url_ip = pieces.vars.url_my_ip

    #Credenciais do usuário
    email = pieces.vars.email
    password = pieces.vars.password

    #Info API Clans
    name_cla = pieces.vars.name_cla
    tag_cla = pieces.vars.tag_cla

    #Variables Key
    name_key = "Test Key"
    description_key = "Key for use in an excelent test"

    #Path files
    path_excel = pieces.vars.path_excel

    #Fazendo login no site
    return_login = login(driver=driver, url=url_login, email=email, password=password)
    if return_login == 0:
        pieces.log(texto=f"[Func] -> clash_royale: Login foi ralizado com sucesso", level="INFO")
    elif return_login == 1:
        pieces.log(texto=f"[End Func] -> clash_royale: Login já estava efetuado", level="INFO")
    elif return_login == 2:
        pieces.log(texto=f"[End Func] -> clash_royale: Email ou senha incorretos", level="DEBUG")
        return 1
    elif return_login < 0:
        pieces.log(texto=f"[End Func] -> clash_royale: Erro ao tentar fazer login. Erro: {return_login}", level="ERROR")
        return -1
    else:
        pieces.log(texto=f"[End Func] -> clash_royale: Erro inesperado ao tentar fazer login. Erro: {return_login}", level="ERROR")
        return -1

    #Obtendo seu IP público
    return_ip = get_my_ip(url=url_ip)
    if isinstance(return_ip, str):
        pieces.log(texto=f"[Func] -> clash_royale: IP foi encontrado com sucesso. IP: {return_ip}", level="DEBUG")
    else:
        pieces.log(texto=f"[End Func] -> clash_royale: Erro ao procurar IP. Erro: {return_ip}", level="ERROR")
        return -2

    #Criando a Key da API
    return_create_key = create_key(driver=driver, name=name_key, description=description_key, ip=return_ip)
    if return_create_key == 0:
        pieces.log(texto=f"[Func] -> clash_royale: Key foi criada com sucesso.", level="INFO")
    elif return_create_key == 1:
        pieces.log(texto=f"[Func] -> clash_royale: Já existia uma Key criada", level="INFO")
    elif return_create_key < 0:
        pieces.log(texto=f"[End Func] -> clash_royale: Erro ao tentar criar a Key. Erro: {return_create_key}", level="ERROR")
        return -3
    else:
        pieces.log(texto=f"[End Func] -> clash_royale: Erro inesperado ao tentar criar a Key. Erro: {return_create_key}", level="ERROR")
        return -3

    #Retornando o TOKEN de acesso a API
    return_token = get_my_token(driver=driver)
    if isinstance(return_token, str):
        pieces.log(texto=f"[Func] -> clash_royale: Token foi capturado com sucesso", level="INFO")
    elif isinstance(return_token, int):
        pieces.log(texto=f"[End Func] -> clash_royale: Erro ao tentar capturar o token. Erro: {return_token}", level="ERROR")
        return -4
    else:
        pieces.log(texto=f"[End Func] -> clash_royale: Erro não mapeado ao tentar capturar o token. Erro: {return_token}", level="ERROR")
        return -4

    #Retornando a TAG inteira do clã
    return_tag = get_tag_of_cla(url=url_api_clans,name=name_cla, token=return_token, tag=tag_cla)
    if isinstance(return_tag, str):
        pieces.log(texto=f"[Func] -> clash_royale: Tag foi capturada com sucesso", level="INFO")
    elif return_tag == 1:
        pieces.log(texto=f"[Func] -> clash_royale: Tag procurada nao foi encontrada", level="DEBUG")
        return -5
    elif return_tag < 0:
        pieces.log(texto=f"[End Func] -> clash_royale: Erro ao tentar capturar a Tag. Erro: {return_tag}", level="ERROR")
        return -5
    else:
        pieces.log(texto=f"[End Func] -> clash_royale: Erro não mapeado ao tentar capturar a Tag. Erro: {return_tag}", level="ERROR")
        return -5

    #Formando a tag pra ASCII
    new_tag = str(return_tag).replace('#', '%23')

    #Criando a URL de membros de clã da API
    url_api_members = url_api_clans + "/" + new_tag + r"/members"
    pieces.log(texto=f"[Func] -> clash_royale: URL de membros => {url_api_members}", level="DEBUG")

    #Pegando os membros da API e criando o Excel
    return_members = get_members_of_cla(url=url_api_members, token=return_token, path_file=path_excel)
    if return_members == 0:
        pieces.log(texto=f"[Func] -> clash_royale: Excel de membros foi criado com sucesso.", level="INFO")
    elif return_members < 0:
        pieces.log(texto=f"[End Func] -> clash_royale: Erro ao tentar criar excel dos membros. Erro: {return_create_key}", level="ERROR")
        return -6
    else:
        pieces.log(texto=f"[End Func] -> clash_royale: Erro inesperado ao tentar criar a Key. Erro: {return_create_key}", level="ERROR")
        return -6

    pieces.log(texto=f"[Func] -> clash_royale: Robô foi executado com sucesso", level="INFO")
    return 0


def login(*, driver, url, email, password):
    pieces.log(texto=f"[Func] -> login", level="DEBUG")

    #XPATHS
    xpath_login = '//*[@id="content"]/div/div[2]/div/header/div/div/div[3]/div/a[2]'
    xpath_email = '//*[@id="email"]'
    xpath_password = '//*[@id="password"]'
    xpath_submit = '//*[@id="content"]/div/div[2]/div/div/div/div/div/div/form/div[4]/button'
    xpath_getting_started = '//*[@id="content"]/div/div[2]/div/header/div/div/div[2]/div/a[1]'
    xpath_error_login = '//*[@id="content"]/div/div[2]/div/div/div/div/div/div/form/div[1]/div/span[2]'

    #Acessando URL de login
    access_url = pieces.lib_web.acessar_url(url, driver=driver)
    if access_url == -1:
        pieces.log(texto=f"[End Func] -> login: Erro ao acessar a URL({url}). Erro: {access_url} ", level="ERROR")
        return -1
    else:
        pieces.log(texto=f"[Func] -> login: URL({url}) acesada com sucesso", level="DEBUG")

    #Verificando se o login já está efetuado
    pieces.log(texto=f"[Func] -> login: Verificando se login já está efetuado...", level="DEBUG")
    verify_is_logged = pieces.lib_web.verificar_elemento_existe(driver=driver, xpath=xpath_getting_started, timeout=10)
    if verify_is_logged == 0:
        pieces.log(texto=f"[End Func] -> login: Login já está efetuado", level="DEBUG")
        return 1
    else:
        pieces.log(texto=f"[Func] -> login: Login ainda não está efetuado", level="DEBUG")

    #Clicando no botão de login
    click_login = pieces.lib_web.clicar_elemento(driver=driver, xpath=xpath_login)
    if click_login == 0:
        pieces.log(texto=f"[Func] -> login: Botão de login foi clicado com sucesso", level="DEBUG")
    else:
        pieces.log(texto=f"[End Func] -> login: Erro ao clicar no botão de login. Erro: {click_login}", level="ERROR")
        return -2

    #Inserindo o email de acesso
    insert_email = pieces.lib_web.preencher_campo(driver=driver, xpath=xpath_email, texto=email)
    if insert_email == 0:
        pieces.log(texto=f"[Func] -> login: Email foi inserido no input com sucesso", level="DEBUG")
    else:
        pieces.log(texto=f"[End Func] -> login: Erro ao inserir email no input. Erro: {insert_email}", level="ERROR")
        return -3

    #Inserindo a senha de acesso
    insert_password = pieces.lib_web.preencher_campo(driver=driver, xpath=xpath_password, texto=password)
    if insert_password == 0:
        pieces.log(texto=f"[Func] -> login: Senha foi inserido no input com sucesso", level="DEBUG")
    else:
        pieces.log(texto=f"[End Func] -> login: Erro ao inserir senha no input. Erro: {insert_password}", level="ERROR")
        return -4

    #Clicando em fazer login
    click_enter = pieces.lib_web.clicar_elemento(driver=driver, xpath=xpath_submit)
    if click_enter == 0:
        pieces.log(texto=f"[Func] -> login: Botão de Sign In foi clicado com sucesso", level="DEBUG")
    else:
        pieces.log(texto=f"[End Func] -> login: Erro ao clicar no botão de Sign In. Erro: {click_enter}", level="ERROR")
        return -5

    #Verificando se teve erro de senha
    verify_error = pieces.lib_web.verificar_elemento_existe(driver=driver, xpath=xpath_error_login, timeout=10)
    if verify_error == 0:
        pieces.log(texto=f"[End Func] -> login: Email ou senha inválida", level="DEBUG")
        return 2

    #Verificando se login foi efetuado se tiver entrado na página principal
    verify_login = pieces.lib_web.verificar_elemento_existe(driver=driver, xpath=xpath_getting_started, timeout=10)
    if verify_login == 0:
        pieces.log(texto=f"[End Func] -> login: Login foi efetuado com sucesso", level="DEBUG")
        return 0
    else:
        pieces.log(texto=f"[End Func] -> login: Página inicial não foi encontrada. Erro: {verify_login}", level="ERROR")
        return -6


def create_key(*, driver, name, description, ip):
    pieces.log(texto=f"[Func] -> create_key", level="DEBUG")

    #XPATHS
    xpath_getting_started = '//*[@id="content"]/div/div[2]/div/header/div/div/div[2]/div/a[1]'
    xpath_profile = '//*[@id="content"]/div/div[2]/div/header/div/div/div[3]/div/div/button/span[1]'
    xpath_my_account = '//*[@id="content"]/div/div[2]/div/header/div/div/div[3]/div/div/ul/li[1]/a'
    xpath_have_key = '//*[@id="content"]/div/div[2]/div/div/section[2]/div/div/div[2]/ul/li'
    xpath_create = '//*[@id="content"]/div/div[2]/div/div/section[2]/div/div/div[2]/p/a/span[2]'
    xpath_name_key = '//*[@id="name"]'
    xpath_description_key = '//*[@id="description"]'
    xpath_ip_key = '//*[@id="range-0"]'
    xpath_create_key = '//*[@id="content"]/div/div[2]/div/div/section/div/div/div[2]/form/div[5]/button'
    xpath_success = '//*[@id="content"]/div/div[2]/div/div/section[2]/div/div/div[2]/ul/div/span[3]'
    text_success = ' Key created successfully.'

    #Verifica se realmente está na página inicial
    verify_home = pieces.lib_web.verificar_elemento_existe(driver=driver, xpath=xpath_getting_started, timeout=10)
    if verify_home != 0:
        pieces.log(texto=f"[End Func] -> create_key: Home Page não foi encontrada.", level="ERROR")
        return -1

    #Clica no nome do usuário
    click_profile = pieces.lib_web.clicar_elemento(driver=driver, xpath=xpath_profile)
    if click_profile == 0:
        pieces.log(texto=f"[Func] -> create_key: Botão de Profile foi clicado com sucesso", level="DEBUG")
    else:
        pieces.log(texto=f"[End Func] -> create_key: Erro ao clicar no botão de Profile. Erro: {click_profile}", level="ERROR")
        return -2

    #Clica em My Account
    click_account = pieces.lib_web.clicar_elemento(driver=driver, xpath=xpath_my_account)
    if click_account == 0:
        pieces.log(texto=f"[Func] -> create_key: Botão de My Account foi clicado com sucesso", level="DEBUG")
    else:
        pieces.log(texto=f"[End Func] -> create_key: Erro ao clicar no botão de My Account. Erro: {click_account}", level="ERROR")
        return -3

    #Verifica se já tem uma chave criada
    verify_have_key = pieces.lib_web.verificar_elemento_existe(driver=driver, xpath=xpath_have_key, timeout=10)
    if verify_have_key == 0:
        pieces.log(texto=f"[End Func] -> create_key: Já existe uma Key criada", level="DEBUG")
        return 1

    #Cria uma chave nova se nao tiver
    click_create = pieces.lib_web.clicar_elemento(driver=driver, xpath=xpath_create)
    if click_create == 0:
        pieces.log(texto=f"[Func] -> create_key: Botão de Create New Key foi clicado com sucesso", level="DEBUG")
    else:
        pieces.log(texto=f"[End Func] -> create_key: Erro ao clicar no botão de Create New Key. Erro: {click_create}", level="ERROR")
        return -4

    #Insere o nome da Chave
    insert_name = pieces.lib_web.preencher_campo(driver=driver, xpath=xpath_name_key, texto=name)
    if insert_name == 0:
        pieces.log(texto=f"[Func] -> create_key: Nome da chave foi inserido com sucesso", level="DEBUG")
    else:
        pieces.log(texto=f"[End Func] -> create_key: Erro ao inserir Nome da Chave. Erro: {insert_name}", level="ERROR")
        return -5

    #Insere a descrição da chave
    insert_description = pieces.lib_web.preencher_campo(driver=driver, xpath=xpath_description_key, texto=description)
    if insert_description == 0:
        pieces.log(texto=f"[Func] -> create_key: Descrição da chave foi inserido com sucesso", level="DEBUG")
    else:
        pieces.log(texto=f"[End Func] -> create_key: Erro ao inserir Descrição da Chave. Erro: {insert_description}", level="ERROR")
        return -6

    #Insere o IP público do usuário
    insert_ip = pieces.lib_web.preencher_campo(driver=driver, xpath=xpath_ip_key, texto=ip)
    if insert_ip == 0:
        pieces.log(texto=f"[Func] -> create_key: IP da chave foi inserido com sucesso", level="DEBUG")
    else:
        pieces.log(texto=f"[End Func] -> create_key: Erro ao inserir IP da Chave. Erro: {insert_ip}", level="ERROR")
        return -7

    #Clica em criar chave
    click_create_key = pieces.lib_web.clicar_elemento(driver=driver, xpath=xpath_create_key)
    if click_create_key == 0:
        pieces.log(texto=f"[Func] -> create_key: Botão de Create Key foi clicado com sucesso", level="DEBUG")
    else:
        pieces.log(texto=f"[End Func] -> create_key: Erro ao clicar no botão de Create Key. Erro: {click_create_key}", level="ERROR")
        return -8

    #Verifica se a mensagem na tela foi de sucesso ou de erro
    verify_success = pieces.lib_web.verificar_elemento_valor_preenchido(driver=driver, xpath=xpath_success, texto_esperado=text_success)
    if verify_success:
        pieces.log(texto=f"[End Func] -> create_key: Key foi criada com sucesso", level="DEBUG")
        return 0
    else:
        pieces.log(texto=f"[End Func] -> create_key: Erro ao criar a Key. Erro: {verify_success}", level="ERROR")
        return -9


def get_my_token(*, driver):
    pieces.log(texto=f"[Func] -> get_my_token", level="DEBUG")

    #XPATHS
    xpath_key = '//*[@id="content"]/div/div[2]/div/div/section[2]/div/div/div[2]/ul/li'
    xpath_key_value = '//*[@id="content"]/div/div[2]/div/div/section/div/div/div[2]/form/div[1]/div'

    #Verifica se tem uma key criada
    verify_key = pieces.lib_web.verificar_elemento_existe(driver=driver, xpath=xpath_key, timeout=10)
    if verify_key != 0:
        pieces.log(texto=f"[End Func] -> get_my_token: Não está na página das keys. Error: {verify_key}", level="ERROR")
        return -1
    else:
        pieces.log(texto=f"[Func] -> get_my_token: Está na página das keys", level="DEBUG")

    #Clica na key criada
    click_key = pieces.lib_web.clicar_elemento(driver=driver, xpath=xpath_key)
    if click_key != 0:
        pieces.log(texto=f"[End Func] -> get_my_token: Não clicou na key existente", level="ERROR")
        return -2
    else:
        pieces.log(texto=f"[Func] -> get_my_token: Clicou na key existente", level="DEBUG")

    #Pega o TOKEN da key
    key_value = pieces.lib_web.obter_texto_elemento(driver=driver, xpath=xpath_key_value, timeout=10)
    if isinstance(key_value, str):
        pieces.log(texto=f"[End Func] -> get_my_token: Key foi encontrada com sucesso", level="DEBUG")
        return key_value
    else:
        pieces.log(texto=f"[End Func] -> get_my_token: Erro ao procurar a key. Erro: {key_value}", level="ERROR")
        return -3


def get_tag_of_cla(*, url, name, token, tag):
    pieces.log(texto=f"[Func] -> get_tag_of_cla", level="DEBUG")

    #Header da requisição
    header = {
        'Authorization': 'Bearer '+token,
        'name': name,
    }

    try:
        #Fazendo a requisição
        page_clans = pieces.requests.get(url, header)

        #Verifica se a requisição foi feita com sucesso
        status_code = page_clans.status_code
        if status_code != 200:
            pieces.log(
                texto=f"[End Func] -> get_members_of_cla: Erro na execução da API de buscar clans. Erro: {status_code}",
                level="ERROR")
            return -1

        #Transforma a requisição em JSON
        json_clans = page_clans.json()
        pieces.log(texto=f"[Func] -> get_tag_of_cla: Json dos clãs foi retornado", level="DEBUG")
    except Exception as error:
        pieces.log(texto=f"[End Func] -> get_tag_of_cla: Erro ao tentar buscar os clãs. Erro: {error}", level="ERROR")
        return -1

    try:
        #Cria um DataFrame dos Clans achados no JSON
        list_clans = pieces.pd.DataFrame(json_clans['items'])
    except Exception as error:
        pieces.log(texto=f"[End Func] -> get_tag_of_cla: Não transformou o JSON em DataFrame. Erro: {error}", level="ERROR")
        return -2

    try:
        #Verifica se o valor buscado existe e retorna o valor completo
        for value in list_clans.values:
            if tag in value[0]:
                pieces.log(texto=f"[Func] -> get_tag_of_cla: Tag foi encontrada com sucesso", level="DEBUG")
                return value[0]
        else:
            pieces.log(texto=f"[Func] -> get_tag_of_cla: Tag buscada não foi encontrada", level="DEBUG")
            return 1
    except Exception as error:
        pieces.log(texto=f"[End Func] -> get_tag_of_cla: Erro ao buscar TAG no DataFrame. Erro: {error}", level="ERROR")
        return -3


def get_members_of_cla(*, url, token, path_file):
    pieces.log(texto=f"[Func] -> get_members_of_cla", level="DEBUG")

    #Header da requisição
    header = {
        'Authorization': 'Bearer ' + token,
    }

    try:
        #Fazendo a requisição
        page_members = pieces.requests.get(url, header)

        #Verifica se a requisição foi feita com sucesso
        status_code = page_members.status_code
        if status_code != 200:
            pieces.log(
                texto=f"[End Func] -> get_members_of_cla: Erro na execução da API de buscar membros. Erro: {status_code}",
                level="ERROR")
            return -1

        #Transforma a requisição em JSON
        json_members = page_members.json()
        pieces.log(texto=f"[Func] -> get_members_of_cla: Json dos membros foi retornado.", level="DEBUG")
    except Exception as error:
        pieces.log(texto=f"[End Func] -> get_members_of_cla: Erro ao tentar buscar os membros do clã. Erro: {error}", level="ERROR")
        return -1

    try:
        #Cria um DataFrame dos dados do clã no JSON
        list_members = pieces.pd.DataFrame(json_members['items'], columns=['name', 'role', 'expLevel', 'trophies'])
    except Exception as error:
        pieces.log(texto=f"[End Func] -> get_members_of_cla: Não transformou o JSON em DataFrame. Erro: {error}", level="ERROR")
        return -2

    try:
        #Alterando o nome das colunas
        list_members.columns = ['nome', 'papel', 'level', 'troféus']
    except Exception as error:
        pieces.log(texto=f"[End Func] -> get_members_of_cla: Erro ao tentar alterar nome das colunas. Erro: {error}", level="ERROR")
        return -3

    try:
        #Criando o nome do arquivo com a data e horário para nao dar conflito de arquivo existente ser substituido
        date = pieces.datetime.datetime.now().strftime("%d.%m.%Y-%H.%M.%S")
        file = path_file + r"\members" + date + ".xlsx"
    except Exception as error:
        pieces.log(texto=f"[End Func] -> get_members_of_cla: Não criou o nome do arquivo. Erro: {error}", level="ERROR")
        return -4

    try:
        #Criando o excel com o resultado obtido
        list_members.to_excel(file, index=False)
        pieces.log(texto=f"[End Func] -> get_members_of_cla: Excel dos membros doi criado com sucesso.", level="DEBUG")
        return 0
    except Exception as error:
        pieces.log(texto=f"[End Func] -> get_members_of_cla: Não criou o arquivo Excel do membros. Erro: {error}", level="ERROR")
        return -5


def get_my_ip(*, url):
    pieces.log(texto=f"[Func] -> get_my_ip", level="DEBUG")

    # Pegando o resultado do IP público do usuário
    ip = pieces.requests.get(url).text

    #Verifica se retornou o IP
    if isinstance(ip, str):
        pieces.log(texto=f"[Func] -> get_my_ip: IP foi encontrado com sucesso. IP: {ip}", level="DEBUG")
        return ip
    else:
        pieces.log(texto=f"[End Func] -> get_my_ip: IP não foi encontrado. Erro: {ip}", level="ERROR")
        return -1


if __name__ == '__main__':
    clash_royale()
    #url = pieces.vars.url_api_clash_royale + r"/clans"
    #token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjMwMjdkYTRkLTFmN2MtNDUxMS1iZmMyLTM3M2Y5ODk1NGQyNCIsImlhdCI6MTYzODY4NDQyNywic3ViIjoiZGV2ZWxvcGVyLzljODFjYTY4LWUxYTEtYWVkYi00ZjRiLWNkZmVlYzc1N2E1NyIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNzcuMzcuMjU0LjIxOSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.ElxHUWLa7sa49VzXHrKXxzU4ptq1ShCYz95MZ6SbsoTBsWDQT6ROlr37YeyuUj3BbmOZbXT4P7Pi2D9cbkXgCA'
    #name = 'The resistance'
    #tag = '#9V2Y'
    #cla = get_tag_of_cla(url=url,name=name, token=token, tag=tag)
    #print(texto=cla)
    #url = 'https://api.clashroyale.com/v1/clans/%239V2YV8YJ/members'
    #members = get_members_of_cla(url=url, token=token, path_file=pieces.vars.path_files)
    #print(texto=members)