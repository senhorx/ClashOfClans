import pieces


def iniciar_web_driver(diretorio_download=""):
    """
    input:
        diretorio_download            #define a pasta onde serão salvos os downloads
    output:
        driver                        #sucesso
    """

    path_driver = pieces.vars.web_driver
    path_idchrome = pieces.vars.web_driver_id
    chrome = True
    while chrome:
        session_id, ip_pag = False, False
        if pieces.lib.os.path.isfile(path_idchrome):
            with open(path_idchrome, "r") as f:
                processados = f.read()
                try:
                    ip_pag, session_id = processados.replace('"', "").split(" ")
                except:
                    pass

        if not session_id:

            options = pieces.webdriver.ChromeOptions()
            options.binary_location = pieces.vars.web_browser_executavel
            options.add_argument("--start-maximized")
            options.add_argument("--enable-javascript")
            options.add_experimental_option('prefs', {
                "download.default_directory": diretorio_download,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True
            },)

            global driver
            driver = pieces.webdriver.Chrome(executable_path=path_driver, options=options)
            driver.maximize_window()

            url = driver.command_executor._url
            session_id = driver.session_id
            endereco = str(url) + " " + str(session_id)

            chrome = False
            with open(path_idchrome, "w") as f:
                pieces.json.dump(endereco, f)
            return driver

        else:

            driver = attach_to_session(ip_pag, session_id)
            try:
                for handle in driver.window_handles:
                    driver.switch_to.window(handle)
                    return driver
            except:
                with open(path_idchrome, "w") as f:
                    pieces.json.dump("", f)


def attach_to_session(executor_url, session_id):
    try:
        driver = pieces.webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        driver.close()
        driver.session_id = session_id
        driver.implicitly_wait(0)
        return driver
    except:
        pass


# In[ ]:


def acessar_url(url, driver=None, diretorio_download="", timeout=30):
    """
    input:
        url                                #url do site
        driver                             #caso exista um driver browser em execução
        diretorio_download                 #define a pasta onde serão salvos os downloads
        timeout                            #tempo utilizado para tentar realizar um processo
    output:
        driver                             #sucesso
        -1                                 #erro
    """

    # ---------- acessar site ----------
    try:
        if driver == None:
            driver = iniciar_web_driver(diretorio_download)
        driver.get(url)
    except:
        return -1

    # ---------- aguardar site carregar ----------
    try:
        pieces.WebDriverWait(driver, timeout).until(pieces.EC.presence_of_all_elements_located)
        return driver
    except:
        return -1


# In[ ]:


def clicar_elemento(driver, xpath, timeout=30):
    """
    input:
        driver                              #browser sendo utilizado
        xpath                               #xpath do elemento na pagina web
        timeout                             #tempo utilizado para tentar realizar um processo
    output:
        0                                   #sucesso
        -1                                  #erro
    """

    # ---------- clicar elemento ----------
    timer = pieces.lib.Timer(timeout)
    while timer.not_expired:
        try:
            elemento = pieces.WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_xpath(xpath))
            elemento.click()
            return 0
        except:
            pass
    return -1


# In[ ]:


def preencher_campo(driver, xpath, texto, verify=True, timer_for_check=1, timeout=10):
    """
    input:
        driver                              #browser sendo utilizado
        xpath                               #xpath do elemento na pagina web
        texto                               #texto para inserir no campo
        verify                              #Informa se a função deve verificar se o valor foi preenchido
        timer_for_check                     #define de quanto em quanto tempo o valor preenchido será verificado
        timeout                             #tempo utilizado para tentar realizar um processo
    output:
        0                                   #sucesso
        -1                                  #erro
    """

    # ---------- preencher campo ----------
    timer = pieces.lib.Timer(timeout)
    while timer.not_expired:
        try:

            campo = pieces.WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_xpath(xpath))
            campo.clear()
            campo.send_keys(texto)
            if verify:
                if verificar_elemento_valor_preenchido(driver, xpath, texto) == True:
                    return 0
            else:
                return 0
        except:
            pass

    return -1


# In[ ]:


def obter_texto_elemento(driver, xpath, timeout=30):
    """
    input:
        driver                            #browser sendo utilizado
        xpath                             #caminho identificando elemento no site
        timeout                           #tempo utilizado para tentar realizar um processo
    output:
        elemento_texto                    #sucesso
        -1                                #erro
    """

    timer = pieces.lib.Timer(timeout)
    while timer.not_expired:
        # ---------- verificar existencia elemento ----------
        elemento_existe = verificar_elemento_existe(driver, xpath, timeout)

        # ---------- obter texto elemento ----------
        if elemento_existe == 0:
            conteudo = ""
            try:
                elemento = pieces.WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_xpath(xpath))

                if elemento.get_attribute('value') != None and len(str(elemento.get_attribute('value'))) > 0:
                    conteudo = elemento.get_attribute('value')

                if elemento.get_attribute('innerText') != None and len(str(elemento.get_attribute('innerText'))) > 0:
                    conteudo = elemento.get_attribute('innerText')

                if conteudo != "":
                    return conteudo
            except:
                continue

        elif elemento_existe == -1:
            continue

    if timer.expired:
        return -1


# In[ ]:


def verificar_elemento_existe(driver, xpath, timeout=30):
    """
    input:
        driver                              #browser sendo utilizado
        xpath                               #caminho identificando elemento no site
        timeout                             #tempo utilizado para tentar realizar um processo
    output:
        0                                   #sucesso
        -1                                  #erro
    """

    # ---------- verificar elemento existe ----------
    try:
        pieces.WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_xpath(xpath))
        return 0
    except:
        return -1


# In[3]:


def verificar_elemento_valor_preenchido(driver, xpath, texto_esperado, timeout=30):
    """
    input:
        driver                              #browser sendo utilizado
        xpath                               #caminho identificando elemento no site
        texto_esperado                      #texto utilizado para comparacao
        timeout                             #tempo utilizado para tentar realizar um processo
    output:
        texto_igual                         #sucesso
        -1                                  #erro
    """
    texto_igual = False

    # ---------- verificar elemento texto ----------
    try:
        elemento = pieces.WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_xpath(xpath))

        if elemento.get_attribute('value') != None and len(str(elemento.get_attribute('value'))) > 0:
            if str(texto_esperado).lower().strip().split() == str(
                    elemento.get_attribute('value')).lower().strip().split():
                texto_igual = True

        if elemento.get_attribute('innerText') != None and len(str(elemento.get_attribute('innerText'))) > 0:
            if str(texto_esperado).lower().strip().split() == str(
                    elemento.get_attribute('innerText')).lower().strip().split():
                texto_igual = True

        if texto_igual == True:
            return texto_igual
    except:
        return -1


# In[ ]:


def wait_by_execute_script(driver, script, *, timeout=30, wait_for=1, log_timeout=True):
    """
    Entradas:
        timeout (int/float) : timeout para retornar 0, numero de segundos
    """

    time_begin = int(round(pieces.time.time() * 1000))
    while True:  # loop infinito
        try:
            time_now = int(round(pieces.time.time() * 1000))
            if ((time_now - time_begin) / 1000 >= timeout):
                if log_timeout:
                    print(f"Timeout após {(time_now - time_begin) / 1000} segundos")
                return False

            r = driver.execute_script(script)
            if r != '':
                return r
        except:
            pieces.time.sleep(wait_for)
    return -1


# In[4]:


def alter_window_change(driver, title, timeout=30):
    timer = pieces.lib.Timer(timeout)

    while timer.not_expired:
        try:
            # acessar aba especificada
            for handle in driver.window_handles:
                driver.switch_to.window(handle)

                if str(title) in str(driver.title):
                    return 0
                else:
                    print(f"Janela não encontrada:{driver.title}")

        except pieces.NoSuchWindowException as error:
            return -1

    if timer.expired:
        return -2


# <h3>func: verificar_alerta_pagina_insegura()</h3>
# <p style="text-indent :5em;">Verifica se abriu uma pagina de alerta, indicando que a pagina que tentamos abrir é insegura, clica em exibir link, e clica no link que foi exibido para prosseguir (essa pagina aparece apenas quando o robô está rodando em maquinas fora da porto).<br></p>
# <img src="img_doc/login_inseguro.PNG" width=640 heigth=400>

# In[ ]:


def verificar_alerta_pagina_insegura(driver, timeout=60):
    """
    Desenvolvido para Google Chrome.

    input:
        driver                       #webdriver sendo utilizado
        timeout                      #tempo utilizado para tentar realizar um processo
    output:
        0                            #sucesso
        -1                           #erro
    """

    xpath_exibir_link = '//button[@id="details-button"]'
    xpath_acessar_link = '//a[@id="proceed-link"]'

    # -------------------- caso seja aberta uma pagina de aviso de segurança, acessa link nao seguro --------------------
    clicou_exibir_link = pieces.lib_web.clicar_elemento(driver, xpath_exibir_link, timeout)

    if clicou_exibir_link == 0:

        clicou_acessar_link = pieces.lib_web.clicar_elemento(driver, xpath_acessar_link, timeout)
        if clicou_acessar_link == 0:
            return 0
        elif clicou_acessar_link == -1:
            return -1

    elif clicou_exibir_link == -1:
        return 0

    return -1