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

#Tabela de Simbolos
def inserirTS(cadeia, token, categoria, tipo):
    if not buscarTS(token):
        global matriz
        global linha

        linha = []

        linha.append(cadeia)
        linha.append(token)
        linha.append(categoria)
        linha.append(tipo)
        linha.append(0)

        matriz.append(linha)
    else:
        #Se ja ta inserido faz o que ?
        raise Exception(
                'Linha: ' + str(line) + '. ' + 'Identificador ' + ch + ' já inserido.')

def buscarTS(token):
    #Retorna True se encontrar
    #Retorna False se não encontrar
    for i in range(len(matriz)):
        if matriz[i][1] == token and matriz[i][5] == 0:
            return True

    return False

def removerTS(token):
    #Colocando 1 para coluna "excluido" tornando a linha inacessível
    for i in range(len(matriz)):
        if matriz[i][1] == token:
            matriz[i][5] = 1

def imprimirTS():
    print('-------------- TABELA DE SIMBOLOS ------------------\n\n')
    for i in range(len(matriz)):
        print(matriz[i])

def lexico():
    global tokenizer

    print("Realizando Análise Léxica....")

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
    global matriz
    global linha

    #texto = readfile()
    matriz = []
    line = 0
    i = 0

    # atualizaLista()
    # ch = termList[0]

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

    print("Realizando Análise Sintática....")

    if ch == 'program':
        ch = proxsimb()
        
        if ch.isalpha() and ch not in palavra_reservada:
            ch = proxsimb()
            corpo()

        else:
            raise Exception(
                'Linha: ' + str(line) + '. ' + 'Esperado um identificador válido. Mas encontrado: ' + ch)

    else:
        raise Exception('Linha: ' + str(line) + '. ' + 'Esperado iniciar com um identificador válido ' +
                        '"program"' + ' Mas encontrado: ' + ch)

def corpo():
    global ch

    dc()
    if ch == 'begin':
        ch = proxsimb()
        comandos()

        if ch == 'end':
            ch = proxsimb()
        else:
            raise Exception('Linha: ' + str(line) + '. ' + 'Esperado encontrar ' + '"end"' +
                            ' Mas encontrado: ' + ch)

    else:
        raise Exception('Linha: ' + str(line) + '. ' + 'Esperado encontrar ' + '"begin"' +
                        ' Mas encontrado: ' + ch)

def dc():
    global ch

    if ch == 'var':
        dc_v()
        mais_dc()
    elif ch == 'procedure':
        dc_p()
        mais_dc()
    else:
        raise Exception('Linha: ' + str(line) + '. ' + 'Esperado um identificador de variável ' + '"var"' +
                        ' ou de função ' + '"procedure"' + ' válido. Mas encontrado: ' + ch)

def mais_dc():
    global ch

    if ch == ';':
        ch = proxsimb()
        dc()

def dc_v():
    global ch

    if ch == 'var':
        ch = proxsimb()
        variaveis()
        if ch == ':':
            ch = proxsimb()
            tipo_var()
        else:
            raise Exception('Linha: ' + str(line) + '. ' + 'Esperado ' + '":"' + '. Mas encontrado: ' + ch)
    else:
        raise Exception('Linha: ' + str(line) + '. ' + 'Esperado um identificador de variável ' +
                        '"var"' + ' válido. Mas encontrado: ' + ch)

def variaveis():
    global ch

    if ch.isalpha() and ch not in palavra_reservada:
        ch = proxsimb()
        mais_var()
    else:
      raise Exception('Linha: ' + str(line) + '. ' + 'Esperado um identificador válido. Mas encontrado: ' + ch)

def mais_var():
    global ch

    if ch == ',':
        ch = proxsimb()
        variaveis()

def tipo_var():
    global ch

    if(ch == 'integer'):
        ch = proxsimb()
    elif(ch == 'real'):
        ch = proxsimb()
    else:
        raise Exception('Linha: ' + str(line) + '. ' + 'Esperado um tipo ' +
                        '"integer ou real"' + ' Mas encontrado: ' + ch)

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
                'Linha: ' + str(line) + '. ' + 'Esperado um identificador válido. Mas encontrado: ' + ch)
    else:
        raise Exception('Linha: ' + str(line) + '. ' + 'Esperado um identificador de procedimento ' +
                        '"procedure"' + ' válido. Mas encontrado: ' + ch)

def parametros():
    global ch

    if ch == '(':
        ch = proxsimb()
        lista_par()

        if ch != ')':
            raise Exception('Linha: ' + str(line) + '. ' + 'Esperado um ' + '")"' + ' Mas encontrado: ' + ch)
    else:
        raise Exception('Linha: ' + str(line) + '. ' + 'Esperado um ' + '"("' + ' Mas encontrado: ' + ch)


def lista_par():
    global ch

    variaveis()
    if ch == ':':
        ch = proxsimb()
        tipo_var()
        mais_par()

def mais_par():
    global ch

    if ch == ';':
        ch = proxsimb()
        lista_par()

def corpo_p():
    global ch

    dc_loc()
    if ch == 'begin':
        ch = proxsimb()
        comandos()
        if ch == 'end':
            ch = proxsimb()
        else:
            raise Exception('Linha: ' + str(line) + '. ' + 'Esperado encontrar ' + '"end"' +
                            ' Mas encontrado: ' + ch)
    else:
        raise Exception('Linha: ' + str(line) + '. ' + 'Esperado encontrar ' + '"begin"' +
                        ' Mas encontrado: ' + ch)

def dc_loc():
    global ch

    dc_v()
    mais_dcloc()

def mais_dcloc():
    global ch

    if ch == ';':
        ch = proxsimb()
        dc_loc()

def lista_arg():
    global ch

    if ch == '(':
        ch = proxsimb()
        argumentos()

        if ch == ')':
            ch = proxsimb()
        else:
            raise Exception('Linha: ' + str(line) + '. ' + 'Esperado encontrar ' + '")"' +
                            ' Mas encontrado: ' + ch)

def argumentos():
    global ch

    if ch.isalpha() and ch not in palavra_reservada:
        ch = proxsimb()
        mais_ident()

def mais_ident():
    global ch

    if ch == ';':
        ch = proxsimb()
        argumentos()

def p_falsa():
    global ch

    if ch == 'else':
        ch = proxsimb()
        comandos()

def comandos():
    comando()
    mais_comandos()

def mais_comandos():
    global ch

    if ch == ';':
        ch = proxsimb()
        comandos()

def comando():
    global ch

    if ch == 'read':
        ch = proxsimb()
        if ch == '(':
            ch = proxsimb()
            variaveis()

            if ch == ')':
                ch = proxsimb()
            else:
                raise Exception('Linha: ' + str(line) + '. ' + 'Esperado um ' + '")"' +
                                ' Mas encontrado: ' + ch)
        else:
            raise Exception('Linha: ' + str(line) + '. ' + 'Esperado um ' + '"("' + ' Mas encontrado: ' + ch)

    elif ch == 'write':
        ch = proxsimb()
        if ch == '(':
            ch = proxsimb()
            variaveis()

            if ch == ')':
                ch = proxsimb()
            else:
                raise Exception('Linha: ' + str(line) + '. ' + 'Esperado um ' + '")"' +
                                ' Mas encontrado: ' + ch)
        else:
            raise Exception('Linha: ' + str(line) + '. ' + 'Esperado um ' + '"("' + ' Mas encontrado: ' + ch)

    elif ch == 'while':
        ch = proxsimb()
        condicao()
        if ch == 'do':
            ch = proxsimb()
            comandos()
            if ch == '$':
                ch = proxsimb()
            else:
                raise Exception('Linha: ' + str(line) + '. ' + 'Esperado o simbolo ' +
                                '"$"' + ' Mas encontrado: ' + ch)
        else:
            raise Exception('Linha: ' + str(line) + '. ' + 'Esperado o comando ' + '"do"' +
                            ' Mas encontrado: ' + ch)

    elif ch == 'if':
        ch = proxsimb()
        condicao()
        if ch == 'then':
            ch = proxsimb()
            comandos()
            p_falsa()

            if ch == '$':
                ch = proxsimb()
            else:
                raise Exception('Linha: ' + str(line) + '. ' + 'Esperado o simbolo ' +
                                '"$"' + ' Mas encontrado: ' + ch)
        else:
            raise Exception('Linha: ' + str(line) + '. ' + 'Esperado o comando ' +
                            '"then"' + ' Mas encontrado: ' + ch)

    elif ch.isalpha() and ch not in palavra_reservada:
        ch = proxsimb()
        restoIdent()

def restoIdent():
    global ch

    if ch == ':=':
        ch = proxsimb()
        expressao()
    else:
        lista_arg()

def condicao():
    global ch

    expressao()
    relacao()
    expressao()

def relacao():
    global ch

    if ch in operador_relacional:
        ch = proxsimb()
    else:
        raise Exception(
            'Linha: ' + str(line) + '. ' + 'Esperado encontrar um operador relacional valido. Mas encontrado: ' + ch)

def expressao():
    global ch

    termo()
    if ch != ';' and ch not in operador_relacional and ch not in palavra_reservada:
        outros_termos()

def op_un():
    global ch

    if ch in operador_aritmetico:
        ch = proxsimb()

def outros_termos():
    global ch

    op_ad()
    termo()
    if ch != ';' and ch != ')' and ch not in palavra_reservada:
        outros_termos()

def op_ad():
    global ch

    if ch == '+' or ch == '-':
        ch = proxsimb()
    else:
        raise Exception(
            'Linha: ' + str(line) + '. ' + 'Esperado encontrar um operador aritmetico valido. Mas encontrado: ' + ch)

def termo():
    global ch

    op_un()
    fator()
    mais_fatores()

def mais_fatores():
    global ch

    if ch != ';' and ch != '+' and ch != "-" and ch != ')' and ch not in operador_relacional and ch not in palavra_reservada:
        op_mul()
        fator()
        mais_fatores()

def op_mul():
    global ch

    if ch == '*' or ch == '/':
        ch = proxsimb()
    else:
      raise Exception('Linha: ' + str(line) + '. ' + 'Esperado encontrar um operador aritmetico valido. Mas encontrado: ' + ch)

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
            raise Exception('Linha: ' + str(line) + '. ' + 'Esperado um ' + '")"' + ' Mas encontrado: ' + ch)

    elif(ch not in delimitador and ch not in operador_aritmetico and ch not in operador_relacional and float(ch)):
        ch = proxsimb()

    elif (ch not in delimitador and ch not in operador_aritmetico and ch not in operador_relacional and int(ch)):
        ch = proxsimb()

if __name__ == "__main__":
    # lexico()
    iniciaVariaveis()
    # programa()
    # print('Cadeia Aceita')

    inserirTS('program', 'id', 'var', 'integer')
    inserirTS('procedure', 'id', 'var', 'real')
    imprimirTS()