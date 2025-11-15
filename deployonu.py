####################################################################################################
# Criado por: Giovana Sato
# Programa para deploy de CPE em Lote - FIX FIBRA
####################################################################################################

## Bibliotecas
import time
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import *
from tkinter import ttk, filedialog, messagebox

############################ FUNÇÃO PRINCIPAL ##########################################
def comecar():
    # Verifica se o XML foi selecionado
    if not caminho_xml.get():
        print("Nenhum arquivo XML selecionado.")
        messagebox.showwarning("Atenção", "Por favor, selecione um arquivo XML antes de iniciar o deploy.")
        return

    ip_equipamento = cb_equipamentos.get()

    # Se for Lote MP-X, também precisa de CSV
    if ip_equipamento == "Lote MP-X" and not caminho_csv.get():
        print("Nenhum arquivo CSV selecionado.")
        messagebox.showwarning("Atenção", "Por favor, selecione um arquivo CSV antes de iniciar o deploy do lote.")
        return

    # Configurações do Firefox
    firefox_options = Options()
    # firefox_options.add_argument("--headless")  # descomente se quiser rodar sem abrir janela
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")

    # Cria o driver usando webdriver-manager
    page = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    try:
        if ip_equipamento == "Huawei HG":
            page.get("http://192.168.100.1/")
            page.find_element(By.XPATH, '//*[@id="txt_Username"]').send_keys("telecomadmin")
            page.find_element(By.XPATH, '//*[@id="txt_Password"]').send_keys("admintelecom" + Keys.RETURN)
            page.find_element(By.XPATH, '//*[@id="headerTab"]/ul/li[11]/div[2]').click()
            page.find_element(By.XPATH, '//*[@id="nav"]/ul/li[2]/div').click()
            iframe = page.find_element(By.XPATH, '//*[@id="frameContent"]')
            page.switch_to.frame(iframe)
            page.find_element(By.XPATH, '//*[@id="t_file"]').send_keys(caminho_xml.get())
            page.find_element(By.XPATH, '//*[@id="btnSubmit"]').click()
            Alert(page).accept()
            time.sleep(10)

        elif ip_equipamento == "Huawei EG":
            page.get("http://192.168.100.1/")
            page.find_element(By.XPATH, '//*[@id="txt_Username"]').send_keys("telecomadmin")
            page.find_element(By.XPATH, '//*[@id="txt_Password"]').send_keys("admintelecom" + Keys.RETURN)
            page.find_element(By.XPATH, '//*[@id="addconfig"]').click()
            page.find_element(By.XPATH, '//*[@id="name_maintaininfo"]').click()
            page.find_element(By.XPATH, '//*[@id="cfgconfig"]').click()
            iframe = page.find_element(By.XPATH, '//*[@id="menuIframe"]')
            page.switch_to.frame(iframe)
            page.find_element(By.XPATH, '//*[@id="t_file"]').send_keys(caminho_xml.get())
            page.find_element(By.XPATH, '//*[@id="btnSubmit"]').click()
            Alert(page).accept()
            time.sleep(10)

        elif ip_equipamento == "Stavix MP-X":
            page.get("http://192.168.1.1/")
            try:
                page.find_element(By.XPATH, "/html/body/div/div/form/ul/li[1]/input").send_keys("telecomadmin")
                page.find_element(By.NAME, 'password').send_keys("admintelecom" + Keys.RETURN)
            except:
                page.find_element(By.XPATH, "/html/body/div/div/form/ul/li[1]/input").send_keys("Unee")
                page.find_element(By.NAME, 'password').send_keys("Changeme_123" + Keys.RETURN)
            WebDriverWait(page, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Admin")))
            page.find_element(By.LINK_TEXT, 'Admin').click()
            page.find_element(By.LINK_TEXT, 'Backup/Restore').click()
            iframe = page.find_element(By.XPATH, '//*[@id="contentIframe"]')
            page.switch_to.frame(iframe)
            page.find_element(By.NAME, "binary").send_keys(os.path.abspath(caminho_xml.get()))
            page.find_element(By.XPATH, '/html/body/form[2]/div/table/tbody/tr/td/input[2]').click()
            time.sleep(10)

        elif ip_equipamento == "Stavix MP-G":
            page.get("http://192.168.1.1/")
            try:
                page.find_element(By.XPATH, "/html/body/div/div/form/ul/li[1]/input").send_keys("telecomadmin")
                page.find_element(By.NAME, 'password').send_keys("admintelecom" + Keys.RETURN)
            except:
                page.find_element(By.XPATH, "/html/body/div/div/form/ul/li[1]/input").send_keys("root")
                page.find_element(By.NAME, 'password').send_keys("admintelecom" + Keys.RETURN)
            WebDriverWait(page, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Admin")))
            page.find_element(By.LINK_TEXT, 'Admin').click()
            page.find_element(By.LINK_TEXT, 'Backup/Restore').click()
            iframe = page.find_element(By.XPATH, '//*[@id="contentIframe"]')
            page.switch_to.frame(iframe)
            page.find_element(By.NAME, "binary").send_keys(os.path.abspath(caminho_xml.get()))
            page.find_element(By.XPATH, '/html/body/form[2]/div/table/tbody/tr/td/input[2]').click()
            time.sleep(10)


        elif ip_equipamento == "Lote MP-X":
            DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

            # Lê o CSV
            with open(caminho_csv.get(), newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=',')
                linhas = list(reader)

            # Remove cabeçalho
            linhas = linhas[1:]
            total = len(linhas)
            erros = []

            # Mapeamento das linhas esperadas e seus "names"
            linhas_names_esperados = {
                91: "SSID",
                1287: "ssid",
                131: "WLAN_WPA_PSK",
                383: "WSC_PSK",
                1278: "wpaPSK",
                1316: "wscPsk",
                176: "WLAN1_SSID",
                1659: "ssid",
                215: "WLAN1_WPA_PSK",
                256: "WLAN1_WSC_PSK",
                1650: "wpaPSK",
                1688: "wscPsk",
                598: "pppUser",
                599: "pppPasswd",
                625: "vid",
                2592: "vid",
                2618: "vid"
            }

            def validar_linhas(backup_lines):
                """Valida se as linhas do backup possuem os names esperados."""
                for num, name in linhas_names_esperados.items():
                    idx = num - 1
                    if idx >= len(backup_lines):
                        return False, f"Linha {num} ausente no backup"
                    linha_str = backup_lines[idx].decode(errors="ignore").strip()
                    if f'Name="{name}"' not in linha_str:
                        return False, f"Linha {num} não contém Name esperado ({name})"
                return True, "ok"

            for i, linha in enumerate(linhas, start=1):
                try:
                    ip = linha[4].strip()  # Coluna E = índice 4
                    ip_equipamento = f"http://{ip}/"
                    print(f"\nProcessando {ip} ({i} de {total})...")

# Login com detecção de falha e retorno à tela anterior
                    try:
                        page.get(ip_equipamento)
                        WebDriverWait(page, 15).until(
                            EC.presence_of_element_located((By.NAME, "username"))
                        )
                        page.find_element(By.XPATH, "/html/body/div/div/form/ul/li[1]/input").send_keys("telecomadmin")
                        page.find_element(By.NAME, "password").send_keys("admintelecom" + Keys.RETURN)
                        time.sleep(2)
                        
                        # Verifica se login falhou (busca por texto ou elemento típico da tela de erro)
                        if "login" in page.title.lower() or "error" in page.page_source.lower():
                            print("⚠️ Login telecomadmin falhou, tentando próxima opção...")
                            page.get(ip_equipamento)  # volta pra página de login
                            raise Exception("Login incorreto")

                    except:
                        try:
                            page.find_element(By.XPATH, "/html/body/div/div/form/ul/li[1]/input").send_keys("unee")
                            page.find_element(By.NAME, "password").send_keys("admintelecom" + Keys.RETURN)
                            time.sleep(2)
                            if "login" in page.title.lower() or "error" in page.page_source.lower():
                                print("⚠️ Login unee falhou, tentando próxima opção...")
                                page.get(ip_equipamento)
                                raise Exception("Login incorreto")
                        except:
                            page.find_element(By.XPATH, "/html/body/div/div/form/ul/li[1]/input").send_keys("root")
                            page.find_element(By.NAME, "password").send_keys("Changeme_123" + Keys.RETURN)
                            time.sleep(2)
                            if "login" in page.title.lower() or "error" in page.page_source.lower():
                                raise Exception("❌ Todas as tentativas de login falharam!")




                    # Admin / Backup
                    WebDriverWait(page, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "Admin"))).click()
                    WebDriverWait(page, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "Backup/Restore"))).click()
                    iframe = WebDriverWait(page, 20).until(EC.presence_of_element_located((By.ID, "contentIframe")))
                    page.switch_to.frame(iframe)

                    # Download backup
                    backup_btn = WebDriverWait(page, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@value="Backup..." and @name="save_cs"]'))
                    )
                    backup_btn.click()
                    time.sleep(5)

                    # Pega último backup da pasta Downloads
                    xml_files = [os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR) if f.lower().endswith(".xml")]
                    if not xml_files:
                        raise FileNotFoundError("Nenhum arquivo .xml encontrado na pasta Downloads.")
                    backup_file = max(xml_files, key=os.path.getctime)

                    # Lê backup e template
                    with open(backup_file, "rb") as f:
                        backup_lines = f.readlines()
                    with open(caminho_xml.get(), "rb") as f:
                        tpl_lines = f.readlines()

                    # Validação das linhas do backup
                    valido, motivo = validar_linhas(backup_lines)
                    if not valido:
                        raise ValueError(f"Backup incompatível ({motivo})")

                    # Substitui linhas específicas
                    linhas_para_substituir = list(linhas_names_esperados.keys())
                    for num in linhas_para_substituir:
                        idx = num - 1
                        if idx < len(backup_lines) and idx < len(tpl_lines):
                            tpl_lines[idx] = backup_lines[idx]

                    # Salva template alterado
                    with open(caminho_xml.get(), "wb") as f:
                        f.writelines(tpl_lines)

                    # Upload
                    page.switch_to.default_content()
                    page.find_element(By.LINK_TEXT, 'Admin').click()
                    page.find_element(By.LINK_TEXT, 'Backup/Restore').click()
                    iframe = WebDriverWait(page, 20).until(EC.presence_of_element_located((By.ID, "contentIframe")))
                    page.switch_to.frame(iframe)
                    WebDriverWait(page, 10).until(EC.presence_of_element_located((By.NAME, "binary")))
                    page.find_element(By.NAME, "binary").send_keys(os.path.abspath(caminho_xml.get()))
                    page.find_element(By.NAME, "load").click()
                    time.sleep(10)

                    print(f"✅ Sucesso em {ip}")

                except Exception as e:
                    erro_msg = f"{ip} - {e}"
                    erros.append(erro_msg)
                    print(f"❌ Erro em {ip}: {e}")
                    continue

            if erros:
                with open("erros_lote.txt", "w", encoding="utf-8") as f:
                    f.write("\n".join(erros))
                print(f"\n⚠️ Processo concluído com erros em {len(erros)} equipamentos. Ver erros_lote.txt")
            else:
                print("\n✅ Lote concluído com sucesso! Nenhum erro encontrado.")

    except Exception as e:
        if 'erros' not in locals():
            erros = []
        erros.append(f"Erro geral: {e}")
        print(f"❌ Erro geral: {e}")

    finally:
        if 'erros' in locals() and erros:
            log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "erros_lote.txt")
            try:
                with open(log_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(erros))
                print(f"\n⚠️ Log salvo em: {log_path}")
            except Exception as log_err:
                print(f"❌ Falha ao salvar log: {log_err}")
        else:
            print("\n✅ Nenhum erro encontrado. Lote concluído com sucesso!")

        try:
            page.quit()
        except:
            pass


############################ GUI ##########################################
janela = Tk()
janela.title("Deploy CPE")

Label(janela, text="Selecione o modelo do equipamento para passar o Script").grid(column=0, row=0, padx=10, pady=10)

lista_equipamentos = ["", "Huawei EG", "Huawei HG", "Stavix MP-X", "Stavix MP-G", "Lote MP-X"]
Label(janela, text="Equipamentos:").grid(column=0, row=1, padx=10, pady=5)

cb_equipamentos = ttk.Combobox(janela, values=lista_equipamentos)
cb_equipamentos.set("")
cb_equipamentos.grid(column=0, row=2, padx=5, pady=5)

# Selecionar XML
def selecionar_xml():
    arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo XML",
        filetypes=[("Arquivos XML", "*.xml")]
    )
    if arquivo:
        caminho_xml.set(arquivo)
        print(f"XML selecionado: {arquivo}")
        lbl_xml.config(text=os.path.basename(arquivo))

caminho_xml = StringVar()
Button(janela, text="Selecionar XML", command=selecionar_xml).grid(column=0, row=3, padx=5, pady=5)
lbl_xml = Label(janela, text="")
lbl_xml.grid(column=0, row=4)

# Selecionar CSV (apenas para Lote MP-X)
def selecionar_csv():
    arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo CSV",
        filetypes=[("Arquivos CSV", "*.csv")]
    )
    if arquivo:
        caminho_csv.set(arquivo)
        print(f"CSV selecionado: {arquivo}")
        lbl_csv.config(text=os.path.basename(arquivo))

def habilitar_csv(*args):
    if cb_equipamentos.get() == "Lote MP-X":
        btn_csv.config(state="normal")
    else:
        btn_csv.config(state="disabled")

caminho_csv = StringVar()
btn_csv = Button(janela, text="Selecionar CSV", command=selecionar_csv, state="disabled")
btn_csv.grid(column=0, row=5, padx=5, pady=5)
lbl_csv = Label(janela, text="")
lbl_csv.grid(column=0, row=6)

cb_equipamentos.bind("<<ComboboxSelected>>", habilitar_csv)

# Botão principal
Button(janela, text="Deploy", command=comecar).grid(column=0, row=7, padx=5, pady=10)

janela.mainloop()
