import os
import random
import re

# ==========================================
# Caminho correto do arquivo de conhecimento
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_INFO = os.path.join(BASE_DIR, "info.txt")

# ==========================================
# Lista de palavras proibidas
# ==========================================

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

# ==========================================
# Saudação
# ==========================================

def saudacoes(nome):
    frases = [
        f"Olá! Eu sou {nome}. Como posso ajudar?",
        "Olá! Tudo bem?",
        "Oi! Em que posso ajudar?"
    ]

    print(random.choice(frases))


# ==========================================
# Recebe texto
# ==========================================

def recebeTexto():

    texto = input("Cliente: ").strip().lower()

    if texto == "":
        return None

    for palavra in PALAVRAS_PROIBIDAS:

        if re.search(rf"\b{re.escape(palavra)}\b", texto):
            print("Maria: Desculpe, não posso responder esse tipo de mensagem.")
            return None

    return texto


# ==========================================
# Carrega base de conhecimento
# ==========================================

def carregar_base():

    base = {}

    if not os.path.exists(ARQUIVO_INFO):

        with open(ARQUIVO_INFO, "w", encoding="utf-8"):
            pass

        return base

    with open(ARQUIVO_INFO, "r", encoding="utf-8") as arquivo:

        for linha in arquivo:

            linha = linha.strip()

            if linha == "":
                continue

            if ";" not in linha:
                continue

            pergunta, resposta = linha.split(";", 1)

            base[pergunta.strip().lower()] = resposta.strip()

    return base


# ==========================================
# Salva nova pergunta
# ==========================================

def salvar(pergunta, resposta):

    with open(ARQUIVO_INFO, "a", encoding="utf-8") as arquivo:

        arquivo.write(f"\n{pergunta};{resposta}")


# ==========================================
# Busca resposta
# ==========================================

def buscaResposta(nome, texto):

    if texto == "tchau":
        return "fim"

    base = carregar_base()

    if texto in base:
        return "Chatbot: " + base[texto]

    print("Maria: Ainda não sei responder essa pergunta.")

    resposta = input("Digite a resposta correta: ").strip()

    salvar(texto, resposta)

    return "Chatbot: Obrigado! Aprendi uma nova resposta."


# ==========================================
# Exibe resposta
# ==========================================

def exibeResposta(resposta, nome):

    if resposta == "fim":
        print(f"{nome}: Volte sempre!")
        return "fim"

    print(resposta.replace("Chatbot:", nome + ":"))

    return "continua"