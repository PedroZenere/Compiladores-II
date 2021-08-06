# ALUNO: PEDRO VINICIUS SEMIN ZENERE
# RGA: 201711310054
import nltk

# Cria lista de palavras chaves
palavra_reservada = ['if', 'else', 'for', 'while', 'then', '$', 'do',
                     'write', 'read', 'begin', 'end', 'var', 'integer', 'real', 'procedure']
operador_relacional = ['<', '>', '==', '<=', '>=']
operador_aritmetico = ['+', '-', '*', '/']
delimitador = [';', ',']
atrib = ['=', ':=', ':']
num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# Expressões Regulares
ident = '[^\W\d_]+'
pont = '\(|\)|\;|\:|\$|\,'
numeros = '\d\.\d*|\.\d*|\d+'
decimal = '[-+]?\d*\.?\d+|[-+]?\d+'
comentarios = '/\*.*?\*/'
comentarios2 = '\{.*?\}'
op_arit = '\+|\-|\*|\/'
op_rel = '(?:<=?|>=?|==|!=)'
atrib = '\:='

# Abrindo arquivo
def readfile():
    with open('../exemplo.txt', 'r') as arq:
        texto = arq.readlines()
        return texto


def lexico():
    global tokenizer

    reg = atrib + '|' + ident + '|' + pont + '|' + decimal + '|' + \
        comentarios + '|' + comentarios2 + '|' + op_arit + '|' + op_rel

    # Separando cada Token e colocando em uma lista
    tokenizer = nltk.RegexpTokenizer(reg)

#Atualiza a lista de termos conforme passa pelas linhas do arquivo
def atualizaLista():
    global line
    global termList

    cont = 0
    for l in texto:
        termList = tokenizer.tokenize(l)
        if len(termList) == 0 and cont == line:
            line += 1
        if cont == line:
            break
        cont += 1

#Inicia as variaveis de controle
def iniciaVariaveis():
    global i
    global ch
    global texto
    global line

    texto = readfile()
    line = 0
    i = 0

    atualizaLista()
    ch = termList[0]

#Atualiza a lista de termo com a linha em análise
def proxLinha():
    global line
    global i

    line += 1
    i = 0

    atualizaLista()

 # Verifica se há comentarios e ignora
def coment(ch):
    t = list(ch)
    if len(t) > 2:
        if(t[0] == '/' and t[1] == '*' or t[0] == '{'):
            return True
    return False

def proxsimb():
    global i
    global ch
    global termList

    i += 1
    #Verifica se ainda exsitem tokens a serem analisados na lista de termos
    if(i <= (len(termList) - 1) and coment(termList[i])):
        i += 1

    #Verifica se ja chegou ao fim da linha e atualiza a lista de termos
    if(i > (len(termList) - 1)):
        proxLinha()
        #Verifica se há comentarios na nova lista de termos
        if coment(termList[i]):
            proxLinha()
    
    #Retorna o proximo simbolo
    ch = termList[i]
    return ch

# ------- Começa nessa Função
def programa():
    global ch

    if ch == 'program':
        ch = proxsimb()
        print(ch)
        if ch.isalpha() and ch not in palavra_reservada:
            print('Lista: ', termList)
            ch = proxsimb()
            corpo()
        else:
            raise Exception(
                'Esperado um identificador válido. Mas encontrado: ' + ch)

    else:
        raise Exception('Esperado iniciar com um identificador válido ' +
                        '"program"' + ' Mas encontrado: ' + ch)
# Ok

def corpo():
    global ch

    dc()
    if ch == 'begin':
        ch = proxsimb()
        comandos()

        if ch == 'end':
            ch = proxsimb()
        else:
            raise Exception('Esperado encontrar ' + '"end"' +
                            ' Mas encontrado: ' + ch)

    else:
        raise Exception('Esperado encontrar ' + '"begin"' +
                        ' Mas encontrado: ' + ch)
# Ok

def dc():
    global ch

    if ch == 'var':
        dc_v()
        print("Voltei")
        print('CH no DC: ', ch)
        mais_dc()
    elif ch == 'procedure':
        dc_p()
        mais_dc()
    else:
        raise Exception('Esperado um identificador de variável ' + '"var"' +
                        ' ou de função ' + '"procedure"' + ' válido. Mas encontrado: ' + ch)

# Ok

def mais_dc():
    global ch
    print('ch: ', ch)
    if ch == ';':
        ch = proxsimb()
        dc()
    # Verificar ;
# Ok

def dc_v():
    global ch

    if ch == 'var':
        ch = proxsimb()
        variaveis()
        if ch == ':':
            ch = proxsimb()
            tipo_var()
        else:
            raise Exception('Esperado ' + '":"' + '. Mas encontrado: ' + ch)
    else:
        raise Exception('Esperado um identificador de variável ' +
                        '"var"' + ' válido. Mas encontrado: ' + ch)
# Ok

def variaveis():
    global ch

    print("CH VARIAVEIS: ", ch)

    if ch.isalpha() and ch not in palavra_reservada:
        ch = proxsimb()
        mais_var()
    # else:
    #   raise Exception('Esperado um identificador válido. Mas encontrado: ' + ch)
# Ok

def mais_var():
    global ch

    if ch == ',':
        ch = proxsimb()
        variaveis()
    # checar virgula?
# OK

def tipo_var():
    global ch

    if(ch == 'integer'):
        ch = proxsimb()
    elif(ch == 'real'):
        ch = proxsimb()
    else:
        raise Exception('Esperado um tipo ' +
                        '"integer ou real"' + ' Mas encontrado: ' + ch)
# Ok

def dc_p():
    global ch

    if ch == 'procedure':
        ch = proxsimb()
        if ch.isalpha() and ch not in palavra_reservada:
            ch = proxsimb()
            parametros()
            ch = proxsimb()
            corpo_p()
        else:
            raise Exception(
                'Esperado um identificador válido. Mas encontrado: ' + ch)
    else:
        raise Exception('Esperado um identificador de procedimento ' +
                        '"procedure"' + ' válido. Mas encontrado: ' + ch)
# Ok

def parametros():
    global ch

    if ch == '(':
        ch = proxsimb()
        lista_par()

        if ch != ')':
            raise Exception('Esperado um ' + '")"' + ' Mas encontrado: ' + ch)
    else:
        raise Exception('Esperado um ' + '"("' + ' Mas encontrado: ' + ch)
# Ok

def lista_par():
    global ch

    variaveis()
    if ch == ':':
        ch = proxsimb()
        tipo_var()
        mais_par()
# Ok

def mais_par():
    global ch

    if ch == ';':
        ch = proxsimb()
        lista_par()
    # Verificar ;

def corpo_p():
    global ch

    print('CH no pente: ', ch)
    dc_loc()
    if ch == 'begin':
        ch = proxsimb()
        comandos()
        if ch == 'end':
            ch = proxsimb()
        else:
            raise Exception('Esperado encontrar ' + '"end"' +
                            ' Mas encontrado: ' + ch)
    else:
        raise Exception('Esperado encontrar ' + '"begin"' +
                        ' Mas encontrado: ' + ch)

def dc_loc():
    global ch

    dc_v()
    # ch = proxsimb()
    mais_dcloc()
    # Ok

def mais_dcloc():
    global ch

    if ch == ';':
        ch = proxsimb()
        dc_loc()
    # Verificar ;
    # Ok

def lista_arg():
    global ch

    if ch == '(':
        ch = proxsimb()
        argumentos()

        if ch == ')':
            ch = proxsimb()
        else:
            raise Exception('Esperado encontrar ' + '")"' +
                            ' Mas encontrado: ' + ch)
    # Ok

def argumentos():
    global ch

    if ch.isalpha() and ch not in palavra_reservada:
        ch = proxsimb()
        mais_ident()
    # Ok

def mais_ident():
    global ch

    if ch == ';':
        ch = proxsimb()
        argumentos()
    # Ok

def p_falsa():
    global ch

    if ch == 'else':
        ch = proxsimb()
        comandos()
    # Ok

def comandos():
    comando()
    mais_comandos()
    # Ok

def mais_comandos():
    global ch

    if ch == ';':
        ch = proxsimb()
        comandos()
    # Ok

def comando():
    global ch

    if ch == 'read':
        ch = proxsimb()
        if ch == '(':
            ch = proxsimb()
            variaveis()

            if ch == ')':
                ch = proxsimb()
                print('CH PROX DO READ: ', ch)
            else:
                raise Exception('Esperado um ' + '")"' +
                                ' Mas encontrado: ' + ch)
        else:
            raise Exception('Esperado um ' + '"("' + ' Mas encontrado: ' + ch)

    elif ch == 'write':
        print('Entrei no write: ', ch)
        ch = proxsimb()
        if ch == '(':
            ch = proxsimb()
            variaveis()

            if ch == ')':
                ch = proxsimb()
            else:
                raise Exception('Esperado um ' + '")"' +
                                ' Mas encontrado: ' + ch)
        else:
            raise Exception('Esperado um ' + '"("' + ' Mas encontrado: ' + ch)

    elif ch == 'while':
        print('Entrei no WHILE: ', ch)
        ch = proxsimb()
        condicao()
        print('CH DO while: ', ch)
        if ch == 'do':
            ch = proxsimb()
            comandos()
            print('DEPOIS COMANDOS DO while: ', ch)
            if ch == '$':
                ch = proxsimb()
            else:
                raise Exception('Esperado o simbolo ' +
                                '"$"' + ' Mas encontrado: ' + ch)
        else:
            raise Exception('Esperado o comando ' + '"do"' +
                            ' Mas encontrado: ' + ch)

    elif ch == 'if':
        print('Entrei no IF: ', ch)
        ch = proxsimb()
        condicao()
        print('CH DO IF: ', ch)
        if ch == 'then':
            ch = proxsimb()
            comandos()
            p_falsa()

            if ch == '$':
                ch = proxsimb()
            else:
                raise Exception('Esperado o simbolo ' +
                                '"$"' + ' Mas encontrado: ' + ch)
        else:
            raise Exception('Esperado o comando ' +
                            '"then"' + ' Mas encontrado: ' + ch)

    elif ch.isalpha() and ch not in palavra_reservada:
        ch = proxsimb()
        restoIdent()
    # Ok

def restoIdent():
    global ch

    if ch == ':=':
        ch = proxsimb()
        expressao()
    else:
        lista_arg()
    # Ok

def condicao():
    global ch

    expressao()
    relacao()
    expressao()
    # Ok

def relacao():
    global ch

    if ch in operador_relacional:
        ch = proxsimb()
    else:
        raise Exception(
            'Esperado encontrar um operador relacional valido. Mas encontrado: ' + ch)
        # Ok

def expressao():
    global ch

    termo()
    if ch != ';' and ch not in operador_relacional and ch not in palavra_reservada:
        outros_termos()
    # Ok

def op_un():
    global ch

    if ch in operador_aritmetico:
        ch = proxsimb()
    # Ok

def outros_termos():
    global ch

    op_ad()
    termo()
    if ch != ';' and ch != ')' and ch not in palavra_reservada:
        outros_termos()
    # OK - checar melhor - (recursao infinita)

def op_ad():
    global ch

    if ch == '+' or ch == '-':
        ch = proxsimb()
    else:
        raise Exception(
            'Esperado encontrar um operador aritmetico valido. Mas encontrado: ' + ch)
    # Ok

def termo():
    global ch

    op_un()
    fator()
    mais_fatores()
    # Ok

def mais_fatores():
    global ch

    if ch != ';' and ch != '+' and ch != "-" and ch != ')' and ch not in operador_relacional and ch not in palavra_reservada:
        op_mul()
        fator()
        mais_fatores()
       # OK - checar melhor - (recursao infinita)

def op_mul():
    global ch

    print('CH NO MUL: ', ch)
    if ch == '*' or ch == '/':
        ch = proxsimb()
    # else:
    #   raise Exception('Esperado encontrar um operador aritmetico valido. Mas encontrado: ' + ch)
       # OK

def fator():
    global ch

    if ch.isalpha():
        ch = proxsimb()

    elif ch == '(':
        ch = proxsimb()
        expressao()

        if ch == ')':
            ch = proxsimb()
        else:
            raise Exception('Esperado um ' + '")"' + ' Mas encontrado: ' + ch)

        print('O que chegou no fator: ', ch)

    elif(ch not in delimitador and ch not in operador_aritmetico and ch not in operador_relacional and float(ch)):
        print('CH NUM FLOAT: ', ch)
        ch = proxsimb()

    elif (ch not in delimitador and ch not in operador_aritmetico and ch not in operador_relacional and int(ch)):
        print('CH NUM: ', ch)
        ch = proxsimb()

if __name__ == "__main__":
    lexico()
    # removeComentarios()
    iniciaVariaveis()
    programa()
    print('Cadeia Aceita')

    # print (" \n============== Lista de Tokens Classificados  =================\n\n")

    # countLines = 1
    # for line in texto:
    #     termList = tokenizer.tokenize(line)
    #print('TermList: ', termList)
    # if len(termList) != 0:
    #     classifaTokens(termList, countLines)
    # countLines += 1

    # return tokenizer

    #print('Lista: ', texto)

# def lexico():
#   # Identificando palavras chaves


#   # Abrindo arquivo
#   with open('exemplo.txt', 'r') as arq:
#       texto = arq.read()
#       # print ("============== Arquivo  =================\n\n")
#       # print(texto)


#   # Expressões Regulares
#   ident = '[^\W\d_]+'
#   pont = '\(|\)|\;|\:|\$|\,'
#   numeros = '\d\.\d*|\.\d*|\d+'
#   decimal = '[-+]?\d*\.?\d+|[-+]?\d+'
#   comentarios = '/\*.*?\*/'
#   comentarios2 = '\{.*?\}'
#   op_arit = '\+|\-|\*|\/'
#   op_rel = '(?:<=?|>=?|==|!=)'
#   atrib = '\:='


#   reg = atrib + '|' + ident + '|' + pont + '|' + decimal + '|' + comentarios + '|' + comentarios2 + '|' + op_arit + '|' + op_rel
#   #reg = atrib + '|' + ident + '|' +  decimal
#   # Separando cada Token e colocando em uma lista
#   global termList
#   tokenizer = nltk.RegexpTokenizer(reg)
#   termList = tokenizer.tokenize(texto)
#   print(" \n============== Lista de Tokens Classificados  =================\n\n")

# def removeComentarios():
#   global termList
#   listDelete = []
#   cont = 0
#   for ch in termList:
#     t = ch.split('/*')
#     if(len(t) > 1):
#       listDelete.append(cont)
#     else:
#       t = ch.split('{')
#       if(len(t) > 1):
#         listDelete.append(cont)
#     cont += 1

#   cont = 0
#   pos = 1
#   for i in listDelete:
#     del(termList[i])
#     if cont+1 < len(listDelete):
#       listDelete[cont+1] = listDelete[cont+1] - pos
#     cont += 1
#     pos += 1

    # print('Tamanho: ', len(termList))
    # print('LISTA ATUALIZADAA: ', termList)

# print(termList)
# termList
