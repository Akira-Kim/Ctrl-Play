def saudacoes(nome):
    import random
    frases = ["Bom dia! Meu nome é " + nome + ". Como vai você?", "Ola!", "Oi, tudo bem?"]
    print(frases[random.randint(0,2)])

def recebeTexto():
    texto = "Cliente: " + input("Cliente: ")
    palavraProibida = [# Xingamentos leves
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
    "hentai", "onlyfans"]

    for p in palavraProibida:
        if p in texto:
            print("Desculpe, mas não posso responder a isso.")
            return texto

def buscaResposta(nome, texto):
    with open("BaseDeConhecimento.txt", "a+") as conhecimento:
        conhecimento.seek(0)
        while True:
            viu = conhecimento.readline()
            if viu != "":
                if texto.replace("Cliente: ","") == "Tchau":
                    print(nome+ ": volte sempre!")
                    return "fim"
                elif viu.strip() == texto.strip():
                    proximalinha = conhecimento.readline()
                    if "Chatbot: " in proximalinha:
                        return proximalinha
            else:
                print("Me desculpe, não sei o que falar")
                conhecimento.write("\n" +" texto")
                resposta_user = input("O que esperava?\n")
                conhecimento.write("\n" + "Chatbot: " + resposta_user)
                return "Hum..."

def exibeResposta(resposta, nome):
    print(resposta.replace("Chatbot: ", nome))
    if resposta == "fim":
        return "fim"
    return "continua"