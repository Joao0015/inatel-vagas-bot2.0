from bs4 import BeautifulSoup
from datetime import date
import requests
import csv
import os
import time

# --- CONFIGURAÇÃO DO BOT (Do GitHub Secrets) ---
TOKEN_BOT = os.getenv("TELEGRAM_TOKEN")
# O ID do seu Canal (ex: @InatelVagasBot)
CANAL_ID = os.getenv("CANAL_ID") 

def enviar_telegram(mensagem):
    # Se não tiver token ou canal configurado, não tenta enviar
    if not TOKEN_BOT or not CANAL_ID:
        print("⚠️ Erro: Token ou Canal não configurados.")
        return

    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    dados = {
        "chat_id": CANAL_ID, 
        "text": mensagem, 
        "parse_mode": "Markdown",
        "disable_web_page_preview": False # Mostra o link preview
    }
    try:
        requests.post(url, data=dados)
    except Exception as e:
        print(f"Erro ao avisar no Telegram: {e}")

# --- CONFIGURAÇÕES GERAIS ---
base_url = "https://inatel.br"
url_inicial = "https://inatel.br/estudante/vagas/estagio?page="
historico = "vagas_estagio_inatel.csv"
links_antigos = set()

# 1. Carregar links antigos para saber o que já foi avisado
if os.path.exists(historico):
    with open(historico, "r", encoding="utf-8") as arquivo:
        reader = csv.DictReader(arquivo)
        for linha in reader:
            if "Link" in linha:
                links_antigos.add(linha["Link"])

# 2. Listas para guardar o que vamos encontrar hoje
todas_as_vagas_atuais = []
novas_vagas_count = 0

print("INICIANDO SCRAPING...")

start = 1
while start <= 10:
    url_final = url_inicial + str(start)
    try:
        requisicao = requests.get(url_final, timeout=10)
        if requisicao.status_code != 200: 
            print(f"Página {start} inacessível.")
            break
    except Exception as e:
        print(f"Erro de conexão na página {start}: {e}")
        break

    site = BeautifulSoup(requisicao.content, "html.parser")
    vagas = site.find_all("a", class_="boxLink")

    if not vagas: 
        break
    
    for vaga in vagas:
        texto = vaga.text.strip()
        link_completo = base_url + vaga.get("href")

        # Lógica para separar Título da Empresa
        if "/" in texto:
            titulo, empresa = texto.split("/", 1)
        else:
            titulo, empresa = texto, "Não informado" 

        # Colocamos os dados em um dicionario
        dados_vaga = {
            "Titulo": titulo.strip(),
            "Empresa": empresa.strip(),
            "Link": link_completo,
            "Página": start
        }
        
        # Guardamos na nossa lista de "Vagas que estão no site agora"
        # Isso serve para reescrever o CSV depois
        todas_as_vagas_atuais.append(dados_vaga)

        # SE FOR NOVA: Avisa no Telegram
        if link_completo not in links_antigos:
            print(f"🆕 NOVIDADE: {titulo.strip()}")
            
            # Trava de segurança para a primeira execução (não spammar 100 vagas)
            if novas_vagas_count < 12:
                msg = (
                    f"🚀 *NOVA VAGA NO INATEL!*\n\n"
                    f"📌 *Vaga:* {titulo.strip()}\n"
                    f"🏢 *Empresa:* {empresa.strip()}\n"
                    f"🔗 [Clique aqui para ver]({link_completo})"
                )
                enviar_telegram(msg)
                # Pausa para o Telegram não bloquear o envio
                time.sleep(3) 
            
            novas_vagas_count += 1

    print(f"Página {start} processada.")
    start += 1


# 3. Agora reescrevemos o histórico do zero ("w") apenas com o que encontramos na run atual
# Isso mantém o CSV sempre limpo, apenas com vagas ativas.
campos = ["Titulo", "Empresa", "Link", "Página"]

def salvar_csv(nome_arquivo, lista_dados):
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(lista_dados)

# Salvamos o Histórico Principal
salvar_csv(historico, todas_as_vagas_atuais)

print("Processo finalizado")

if novas_vagas_count > 12:
    print(f"⚠️ {novas_vagas_count} vagas encontradas, mas limitamos o envio a 12 por segurança.")
else:
    print(f"🚀 {novas_vagas_count} novas vagas enviadas no telegram.")
