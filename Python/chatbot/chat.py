import random
import re
import unicodedata

ARQUIVO_BANCO = "info.txt"

# Quanto a pergunta precisa se parecer com a do banco (0.0 a 1.0)
# 0.45 = razoável | 0.60 = mais rigoroso | 0.30 = mais permissivo
LIMIAR_SIMILARIDADE = 0.45

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
# SIMILARIDADE (Jaccard)
# ==============================

def limpa_frase(frase):
    """Remove pontuação e deixa em minúsculas (para comparar palavras)."""
    frase = remover_acentos(frase.lower())
    for t in [".", ",", "!", "?", ";", ":", "-", "_",
              "(", ")", "[", "]", "{", "}", "'", '"', "\n"]:
        frase = frase.replace(t, "")
    return frase.strip()


def jaccard(texto1, texto2):
    """
    Similaridade de Jaccard entre duas frases.
    Retorna um número de 0.0 (diferentes) a 1.0 (iguais).
    """
    palavras1 = set(limpa_frase(texto1).split())
    palavras2 = set(limpa_frase(texto2).split())

    if not palavras1 or not palavras2:
        return 0.0

    intersecao = palavras1 & palavras2   # palavras em comum
    uniao = palavras1 | palavras2        # todas as palavras juntas

    return len(intersecao) / len(uniao)


def busca_por_similaridade(texto):
    """
    Percorre toda a base e devolve a melhor resposta
    se a similaridade for >= LIMIAR_SIMILARIDADE.
    Caso contrário devolve None.
    """
    melhor_score = 0.0
    melhor_resposta = None

    for pergunta_base, respostas in BASE.items():
        score = jaccard(texto, pergunta_base)

        if score > melhor_score:
            melhor_score = score
            melhor_resposta = random.choice(respostas)

    if melhor_score >= LIMIAR_SIMILARIDADE:
        return melhor_resposta

    return None

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
# BUSCAR RESPOSTA (console)
# ==============================

def buscaResposta(texto):
    global BASE

    pergunta = normalizar(texto)

    # Encerrar chatbot
    if pergunta in ["tchau", "adeus", "ate logo"]:
        return "fim"

    # 1) Tentativa de match EXATO
    if pergunta in BASE:
        return random.choice(BASE[pergunta])

    # 2) Tentativa por SIMILARIDADE (Jaccard)
    resposta_similar = busca_por_similaridade(texto)
    if resposta_similar is not None:
        return resposta_similar

    # 3) Não encontrou → aprende
    print("Maria: Não sei responder isso.")
    resposta = input("Qual deveria ser a resposta? ")
    salva_sugestao(texto, resposta)
    return "Obrigado! Aprendi uma nova resposta."

# ==============================
# BUSCAR RESPOSTA (GUI)
# ==============================

def buscaResposta_GUI(texto):
    global BASE

    pergunta = normalizar(texto)

    # 1) Match exato
    if pergunta in BASE:
        return random.choice(BASE[pergunta])

    # 2) Match por similaridade
    return busca_por_similaridade(texto)

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

def exibeResposta_GUI(resposta, nome):
    if resposta == "fim":
        return f"{nome}: Volte sempre!"
    return f"{nome}: {resposta}"
