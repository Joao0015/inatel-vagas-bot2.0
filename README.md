# 🤖 Bot de Vagas de Estágio - Inatel (Telegram)

Este projeto é uma automação desenvolvida para monitorar o portal de carreiras do Inatel e notificar instantaneamente os alunos sobre novas oportunidades de estágio.

## 🚀 Como receber as vagas?

Você não precisa instalar nada! Basta entrar no canal oficial do bot no Telegram. O robô envia as vagas lá assim que elas são detectadas.

👉 **[CLIQUE AQUI PARA ENTRAR NO CANAL](https://t.me/inatelvagasbot)** *(Ou procure por `@inatelvagasbot` no Telegram)*

---

## ⚙️ Como funciona?

O robô "lê" o site do Inatel automaticamente em horários estratégicos do dia. Se ele encontrar uma vaga que ainda não foi postada, ele envia para o canal. Se não houver nada novo, ele permanece em silêncio para não gerar spam.

### 🕒 Horários de Atualização
O robô verifica o portal 4 vezes ao dia (Horário de Brasília):
- **09:00** (Início do dia)
- **13:00** (Pós-almoço)
- **17:00** (Fim de expediente)
- **21:00** (Resumo da noite)

### ✨ Funcionalidades
- **Monitoramento Automático:** Varredura das primeiras páginas do portal de carreiras.
- **Filtro de Duplicidade:** Só envia vagas que realmente são novidade (baseado no histórico).
- **Formatação Limpa:** A mensagem chega com Título, Empresa e o Link direto para a vaga.

---

## 🛠️ Tecnologias Utilizadas

Este projeto roda 100% na nuvem e sem custos de servidor, utilizando a infraestrutura do GitHub.

- **Linguagem:** Python 3.10
- **Bibliotecas:** `BeautifulSoup4` (Web Scraping), `Requests`, `CSV`.
- **Infraestrutura:** GitHub Actions (Agendamento via Cron Job).
- **Notificação:** Telegram Bot API.

## ⚠️ Aviso Legal

Este é um projeto desenvolvido por aluno e **não possui vínculo oficial** com o Inatel ou com o setor de estágios (NESP). A ferramenta serve apenas para facilitar o acesso à informação que já é pública no site da instituição.

---

Made with 🐍 and ☕ by **João Victor Simões**.
