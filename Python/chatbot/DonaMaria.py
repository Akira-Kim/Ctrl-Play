#!/usr/bin/env python3
# ============================================================
#  Chatbot Dona Maria - Arquivo único (tudo em um só lugar)
#  Basta executar:  python DonaMaria_Completo.py
# ============================================================

import random
import re
import unicodedata
import os
from tkinter import *

# ==============================
# CONFIGURAÇÃO
# ==============================

NOME_MAQUINA = "Maria"

# Caminho do info.txt SEMPRE ao lado deste arquivo .py
# (não importa de qual pasta você execute o programa)
_PASTA_DO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_BANCO = os.path.join(_PASTA_DO_SCRIPT, "info.txt")

# Usa o info.txt que está na MESMA PASTA deste arquivo .py
# (não cria arquivo novo – só lê o que você já tem)

# ==============================
# PALAVRAS PROIBIDAS
# ==============================

PALAVRAS_PROIBIDAS = [
    "idiota", "burro", "otario", "otário", "babaca",
    "imbecil", "otaria", "otária", "palhaço", "palhaco",
    "trouxa", "retardado", "animal", "tapado",

    "merda", "bosta", "porra", "caralho",
    "cacete", "puta", "puta que pariu", "fdp",
    "filho da puta", "desgraçado", "desgracado",
    "arrombado", "arrombada", "cu", "cú",

    "vagabundo", "vagabunda", "lixo",
    "escroto", "escrota", "nojento", "nojenta",

    "gostosa", "gostoso", "delicia", "delícia",
    "manda nude", "nudes", "pelada", "pelado",

    "http://", "https://", "www.",
    ".com", ".net", ".xyz",

    "pix urgente", "ganhe dinheiro",
    "aposta", "cassino", "jogo do tigrinho",

    "cocaina", "cocaína", "maconha",
    "crack", "heroina", "heroína",

    "sexo", "porno", "pornografia",
    "hentai", "onlyfans"
]

# ==============================
# FUNÇÕES AUXILIARES
# ==============================

def remover_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def normalizar(texto):
    texto = texto.lower().strip()
    texto = remover_acentos(texto)
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

# ==============================
# CARREGAR BASE (info.txt existente)
# ==============================

def carregar_base():
    """Carrega o info.txt que já está na mesma pasta do programa."""
    if not os.path.exists(ARQUIVO_BANCO):
        print("=" * 50)
        print("ERRO: Arquivo info.txt não encontrado!")
        print(f"Coloque o info.txt nesta pasta:")
        print(f"  {os.path.dirname(ARQUIVO_BANCO)}")
        print("=" * 50)
        input("Pressione Enter para sair...")
        raise SystemExit(1)

    base = {}
    with open(ARQUIVO_BANCO, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if ";" not in linha:
                continue
            pergunta, resposta = linha.split(";", 1)
            pergunta = normalizar(pergunta)
            if pergunta not in base:
                base[pergunta] = []
            base[pergunta].append(resposta)

    print(f"[Dona Maria] Base carregada: {len(base)} perguntas")
    print(f"             ({ARQUIVO_BANCO})")
    return base

BASE = carregar_base()

# ==============================
# SALVAR NOVA RESPOSTA
# ==============================

def salva_sugestao(pergunta, resposta):
    global BASE
    pergunta = normalizar(pergunta)
    with open(ARQUIVO_BANCO, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"\n{pergunta};{resposta}")
    if pergunta not in BASE:
        BASE[pergunta] = []
    BASE[pergunta].append(resposta)

# ==============================
# BUSCA DE RESPOSTA
# ==============================

def busca_resposta(texto):
    pergunta = normalizar(texto)
    if pergunta in BASE:
        return random.choice(BASE[pergunta])
    return None

def contem_palavra_proibida(texto):
    texto_normalizado = normalizar(texto)
    for palavra in PALAVRAS_PROIBIDAS:
        if re.search(rf"\b{re.escape(remover_acentos(palavra.lower()))}\b",
                     texto_normalizado):
            return True
    return False

# ==============================
# SAUDAÇÃO
# ==============================

def saudacao():
    frases = [
        f"Bom dia! Meu nome é {NOME_MAQUINA}. Como vai você?",
        f"Olá! Eu sou {NOME_MAQUINA}.",
        f"Oi! Eu sou {NOME_MAQUINA}. Como posso ajudar?"
    ]
    return random.choice(frases)

# ==============================
# INTERFACE GRÁFICA
# ==============================

def iniciar_gui():
    main_window = Tk()
    main_window.title("Chatbot Dona Maria")
    main_window.geometry("700x600")
    main_window.resizable(True, True)

    entrada_sugestao = False
    ultima_pergunta = ""

    texto_conversa = Text(
        main_window,
        width=80,
        height=25,
        state=DISABLED,
        wrap=WORD,
        font=("Segoe UI", 10)
    )
    texto_conversa.pack(pady=10, padx=10, fill=BOTH, expand=True)

    frame = Frame(main_window)
    frame.pack(pady=5, padx=10, fill=X)

    entrada = Entry(frame, width=60, font=("Segoe UI", 11))
    entrada.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))

    def escrever(mensagem):
        texto_conversa.config(state=NORMAL)
        texto_conversa.insert(END, mensagem + "\n")
        texto_conversa.config(state=DISABLED)
        texto_conversa.see(END)

    def enviar(event=None):
        nonlocal entrada_sugestao, ultima_pergunta

        texto = entrada.get().strip()
        if texto == "":
            return

        entrada.delete(0, END)
        escrever("Você: " + texto)

        # Filtro de palavras proibidas (não aplica quando está aprendendo)
        if not entrada_sugestao and contem_palavra_proibida(texto):
            escrever(f"{NOME_MAQUINA}: Desculpe, não posso responder esse tipo de mensagem.")
            return

        if entrada_sugestao:
            salva_sugestao(ultima_pergunta, texto)
            escrever(f"{NOME_MAQUINA}: Obrigado! Aprendi uma nova resposta.")
            entrada_sugestao = False
            return

        # Despedida
        pergunta = normalizar(texto)
        if pergunta in ["tchau", "adeus", "ate logo", "até logo"]:
            escrever(f"{NOME_MAQUINA}: Volte sempre!")
            return

        resposta = busca_resposta(texto)

        if resposta is None:
            escrever(f"{NOME_MAQUINA}: Não sei responder isso.")
            escrever(f"{NOME_MAQUINA}: Qual deveria ser a resposta?")
            ultima_pergunta = texto
            entrada_sugestao = True
        else:
            escrever(f"{NOME_MAQUINA}: {resposta}")

    Button(frame, text="Enviar", command=enviar, font=("Segoe UI", 10)).pack(side=LEFT)
    entrada.bind("<Return>", enviar)

    # Mensagem inicial
    escrever(saudacao())
    entrada.focus()

    main_window.mainloop()

# ==============================
# VERSÃO CONSOLE (opcional)
# ==============================

def iniciar_console():
    print(saudacao())
    while True:
        try:
            texto = input("Cliente: ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{NOME_MAQUINA}: Volte sempre!")
            break

        if not texto:
            continue

        if contem_palavra_proibida(texto):
            print(f"{NOME_MAQUINA}: Desculpe, não posso responder esse tipo de mensagem.")
            continue

        pergunta = normalizar(texto)
        if pergunta in ["tchau", "adeus", "ate logo", "até logo"]:
            print(f"{NOME_MAQUINA}: Volte sempre!")
            break

        resposta = busca_resposta(texto)
        if resposta is None:
            print(f"{NOME_MAQUINA}: Não sei responder isso.")
            try:
                nova = input("Qual deveria ser a resposta? ").strip()
            except (EOFError, KeyboardInterrupt):
                print(f"\n{NOME_MAQUINA}: Volte sempre!")
                break
            if nova:
                salva_sugestao(texto, nova)
                print(f"{NOME_MAQUINA}: Obrigado! Aprendi uma nova resposta.")
        else:
            print(f"{NOME_MAQUINA}: {resposta}")

# ==============================
# PONTO DE ENTRADA
# ==============================

if __name__ == "__main__":
    import sys

    # Se passar "console" como argumento → modo texto
    # Caso contrário → abre a interface gráfica
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("console", "-c", "--console"):
        iniciar_console()
    else:
        iniciar_gui()
