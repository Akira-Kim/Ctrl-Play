import random
import re

# Lista de palavras proibidas
PALAVRAS_PROIBIDAS = [
    # Xingamentos leves
    "idiota", "burro", "otario", "otário", "babaca",
    "imbecil", "otaria", "otária", "palhaço", "palhaco",
    "trouxa", "retardado", "animal", "tapado",

    # Palavrões
    "merda", "bosta", "porra", "caralho",
    "cacete", "puta", "puta que pariu", "fdp",
    "filho da puta", "desgraçado", "desgracado",
    "arrombado", "arrombada", "cu", "cú",

    # Ofensas
    "vagabundo", "vagabunda", "lixo",
    "escroto", "escrota", "nojento", "nojenta",

    # Assédio
    "gostosa", "gostoso", "delicia", "delícia",
    "manda nude", "nudes", "pelada", "pelado",

    # Spam
    "http://", "https://", "www.",
    ".com", ".net", ".xyz",

    # Golpes
    "pix urgente", "ganhe dinheiro",
    "aposta", "cassino", "jogo do tigrinho",

    # Drogas
    "cocaina", "cocaína", "maconha",
    "crack", "heroina", "heroína",

    # Conteúdo adulto
    "sexo", "porno", "pornografia",
    "hentai", "onlyfans"
]


def saudacoes(nome):
    frases = [
        f"Bom dia! Meu nome é {nome}. Como vai você?",
        "Olá!",
        "Oi, tudo bem?"
    ]
    print(random.choice(frases))


def recebeTexto():
    texto = "Cliente: " + input("Cliente: ").strip().lower()

    for palavra in PALAVRAS_PROIBIDAS:
        if re.search(rf"\b{re.escape(palavra)}\b", texto):
            print("Maria: Desculpe, mas não posso responder esse tipo de mensagem.")
            return None

    return texto


def buscaResposta(nome, texto):
    with open("BaseDeConhecimento.txt", "a+", encoding="utf-8") as conhecimento:
        conhecimento.seek(0)

        # Encerrar chatbot
        if texto.replace("Cliente: ", "").strip().lower() == "tchau":
            return "fim"

        while True:
            linha = conhecimento.readline()

            if linha != "":
                if linha.strip().lower() == texto.strip().lower():
                    resposta = conhecimento.readline()

                    if resposta.startswith("Chatbot:"):
                        return resposta

            else:
                print("Maria: Não sei responder isso.")

                conhecimento.write("\n" + texto)

                resposta_usuario = input("Qual deveria ser a resposta? ")

                conhecimento.write("\nChatbot: " + resposta_usuario)

                return "Chatbot: Obrigado! Aprendi uma nova resposta."


def exibeResposta(resposta, nome):
    if resposta == "fim":
        print(f"{nome}: Volte sempre!")
        return "fim"

    print(resposta.replace("Chatbot:", nome + ":"))
    return "continua"