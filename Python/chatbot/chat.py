import random
import re
import unicodedata

ARQUIVO_BANCO = "info.txt"

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
# SAUDAÇÕES
# ==============================

def saudacoes(nome):
    frases = [
        f"Bom dia! Meu nome é {nome}. Como vai você?",
        f"Olá! Eu sou {nome}.",
        f"Oi! Eu sou {nome}. Como posso ajudar?"
    ]
    print(random.choice(frases))

def saudacoes_GUI(nome):
    frases = [
        f"Bom dia! Meu nome é {nome}. Como vai você?",
        f"Olá! Eu sou {nome}.",
        f"Oi! Eu sou {nome}. Como posso ajudar?"
    ]
    return random.choice(frases)

# ==============================
# RECEBER TEXTO
# ==============================

def recebeTexto():

    texto = input("Cliente: ").strip()

    texto_normalizado = normalizar(texto)

    for palavra in PALAVRAS_PROIBIDAS:
        if re.search(rf"\b{re.escape(remover_acentos(palavra.lower()))}\b",
                     texto_normalizado):

            print("Maria: Desculpe, não posso responder esse tipo de mensagem.")
            return None

    return texto

# ==============================
# CARREGAR BASE
# ==============================

def carregar_base():

    base = {}

    try:

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

    except FileNotFoundError:

        open(ARQUIVO_BANCO, "w", encoding="utf-8").close()

    return base

# ==============================
# BASE EM MEMÓRIA
# ==============================

BASE = carregar_base()


# ==============================
# BUSCAR RESPOSTA
# ==============================

def buscaResposta(texto):

    global BASE

    pergunta = normalizar(texto)

    # Encerrar chatbot
    if pergunta in ["tchau", "adeus", "até logo", "ate logo"]:
        return "fim"

    # Procura resposta
    if pergunta in BASE:
        return random.choice(BASE[pergunta])

    # Não encontrou
    print("Maria: Não sei responder isso.")

    resposta = input("Qual deveria ser a resposta? ")

    salva_sugestao(texto, resposta)

    return "Obrigado! Aprendi uma nova resposta."


# ==============================
# VERSÃO PARA GUI
# ==============================

def buscaResposta_GUI(texto):

    global BASE

    pergunta = normalizar(texto)

    if pergunta in BASE:
        return random.choice(BASE[pergunta])

    return None


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
# EXIBIR RESPOSTA
# ==============================

def exibeResposta(resposta, nome):

    if resposta == "fim":
        print(f"{nome}: Volte sempre!")
        return "fim"

    print(f"{nome}: {resposta}")

    return "continua"


# ==============================
# VERSÃO GUI
# ==============================

def exibeResposta_GUI(resposta, nome):

    if resposta == "fim":
        return f"{nome}: Volte sempre!"

    return f"{nome}: {resposta}"