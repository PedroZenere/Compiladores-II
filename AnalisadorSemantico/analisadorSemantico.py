# ALUNO: PEDRO VINICIUS SEMIN ZENERE
# RGA: 201711310054
import nltk
import decimal
import numbers
from prettytable import PrettyTable

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
decimals = '[-+]?\d*\.?\d+|[-+]?\d+'
comentarios = '/\*.*?\*/'
comentarios2 = '\{.*?\}'
op_arit = '\+|\-|\*|\/'
op_rel = '(?:<=?|>=?|==|!=)'
atrib = '\:='

#----------- Legendas:
# 1. Tipos Token:
#   1.1 - Identificador
#   1.2 - Numero
#
# 2. Tipos Categoria:
#   2.1 - Variavel
#   2.2 - Procedimento
#
# 3. Tipos:
#   3.1 - Integer
#   3.2 - Real

# Abrindo arquivo
def readfile():
    with open('../exemplo.txt', 'r') as arq:
        texto = arq.readlines()
        return texto

#-------------------- Definindo estrutura da TS ------------------
class TSimbolos:
    def setEscopo(self, escopo):
        self.escopo = escopo
    def setCadeia(self, cadeia):
        self.cadeia = cadeia
    def setToken(self, token):
        self.token = token
    def setCategoria(self, categoria):
        self.categoria = categoria
    def setTipo(self, tipo):
        self.tipo = tipo
    def setValor(self, valor):
        self.valor = valor
    def setExcluido(self, excluido):
        self.excluido = excluido

    def getEscopo(self):
        return self.escopo
    def getCadeia(self):
        return self.cadeia
    def getToken(self):
        return self.token
    def getCategoria(self):
        return self.categoria
    def getTipo(self):
        return self.tipo
    def getValor(self):
        return self.valor
    def getExcluido(self):
        return self.excluido
#--------------------------------------------------------------------------

#------------------ Construtores de Objetos ---------------------------------
def montaObjeto(escopo, cadeia, token, categoria, tipo, valor='-'):
    descritor = TSimbolos()

    descritor.setEscopo(escopo)
    descritor.setCadeia(cadeia)
    descritor.setToken(token)
    descritor.setCategoria(categoria)
    descritor.setTipo(tipo)
    descritor.setValor(valor)
    descritor.setExcluido(0)

    return descritor

def montaObjetoTSVariaveis(escopo, cadeia, token, categoria):
    obj = TSimbolos()

    obj.setEscopo(escopo)
    obj.setCadeia(cadeia)
    obj.setToken(token)
    obj.setCategoria(categoria)
    obj.setValor('-')
    obj.setExcluido(0)

    return obj

#-------------------------------------------------------------------------

#---------------- Tabela de Simbolos ---------------------------
def inserirTS(escopo, cadeia, token, categoria, tipo, valor='-'):
    global matriz
    
    obj = montaObjeto(escopo, cadeia, token, categoria, tipo, valor)
    matriz.append(obj)

def inserirTSVariaveis(escopo, cadeia, token, categoria):
    global matriz

    obj = montaObjetoTSVariaveis(escopo, cadeia, token, categoria)
    matriz.append(obj)

def updateTSTipoVariavies(escopo, cadeia, categoria, tipo):
    for obj in matriz:
        for var in cadeia:
            if obj.getEscopo() == escopo and obj.getCadeia() == var and obj.getCategoria() == categoria:
                obj.setTipo(tipo)
        
def buscarTS(escopo, cadeia):
    #Retorna True se encontrar
    #Retorna False se não encontrar
    for obj in matriz:
        if obj.getCadeia() == cadeia and obj.getExcluido() == 0 and obj.getEscopo() == escopo:
            return True
    return False

def buscaTSTipo(escopo, cadeia):
     for obj in matriz:
        if obj.getCadeia() == cadeia and obj.getEscopo() == escopo:
            return obj.getTipo()

def buscaTSToken(escopo, cadeia):
    for obj in matriz:
        if obj.getCadeia() == cadeia and obj.getEscopo() == escopo:
            return obj.getToken()

def removerTS(escopo):
    #Colocando 1 para coluna "excluido" tornando a linha inacessível
    for i in matriz:
        if i.getEscopo() == escopo:
            i.setExcluido(1)

def imprimirTS():
    print('----------------- TABELA DE SIMBOLOS --------------------\n')

    t = PrettyTable(['Escopo', 'Cadeia', 'Token', 'Categoria', 'Tipo', 'Valor'])
    for i in matriz:
        t.add_row([i.getEscopo(), i.getCadeia(), i.getToken(), i.getCategoria(), i.getTipo(), i.getValor()])
    print(t)

#----------------------------------------------------------------------------------

#------------------- Analisador Semantico -----------------------------------------
def verificaParametros(escopoLocal, escopoAtual):
    contParametros = 0
    #Verificar tamanho
    for i in matriz:
        if i.getEscopo() == escopoLocal and i.getCategoria() == 'parametro':
            contParametros += 1

    #Numero
    if contParametros != len(parametrosPassados):
        raise Exception(
                'Linha: ' + str(line+1) + '. ' + 'Quantidade de parametros inválido')

    #Ordem e Tipo
    cont = 0
    for j in matriz:
        if i.getEscopo() == escopoAtual and i.getCadeia() == i:
            tipoDeclarado = buscaTSTipo(escopoAtual, parametrosPassados[cont])
            if i.getTipo() != tipoDeclarado:
                raise Exception(
                'Linha: ' + str(line+1) + '. ' + 'Tipo dos parâmetros não corresponde ao que foi declarado no escopo desta função')
            cont += 1

    parametrosPassados.clear()

def verificaTipoExpressao(variavelRecebedora, escopo):
    tipoRecebedora = buscaTSTipo(escopo, variavelRecebedora)

    if tipoRecebedora == 'integer':
        for i in variaveisExpressao:
            token = buscaTSTipo(escopo, i)
            if token == num:
                if isFloat(i):
                    raise Exception(
                'Linha: ' + str(line+1) + '. ' + 'Impossível converter um real para inteiro')
            else:
                tipoVariaviesExpressao = buscaTSTipo(escopo, i)
                if tipoRecebedora != tipoVariaviesExpressao:
                    raise Exception(
                'Linha: ' + str(line+1) + '. ' + 'Impossível converter um real para inteiro')
    
    variaveisExpressao.clear()

def verificarDivisao(escopo):
    for i in variaveisExpressao:
        tipoVariaviesExpressao = buscaTSTipo(escopo, i)
        if tipoVariaviesExpressao != 'integer':
            raise Exception(
                'Linha: ' + str(line+1) + '. ' + 'A divisão é permitida somente entre numero inteiros')

#------------------- Analisador Léxico --------------------------------------------
def lexico():
    global tokenizer

    print("Realizando Análise Léxica....")

    reg = atrib + '|' + ident + '|' + pont + '|' + decimals + '|' + \
        comentarios + '|' + comentarios2 + '|' + op_arit + '|' + op_rel

    # Separando cada Token e colocando em uma lista
    tokenizer = nltk.RegexpTokenizer(reg)

#----------------------------------------------------------------------------------

#------------------ Funções que percorrrem os tokens e auxiliares ------------------------------
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
    global lista_varTS, parametrosPassados, variaveisExpressao, temDivisao

    texto = readfile()
    matriz = []
    lista_varTS = [] 
    variaveisExpressao = [] # Buffer para guardar variáveis de expressões
    parametrosPassados = [] # Buffer para guardar variáveis de argumentos de funcoes
    temDivisao = False
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

def voltaSimb():
    return termList[i-1]

def isFloat(ch):
    num = list(ch)

    for element in num:
        if element == '.':
            return True
    return False
#--------------------------------------------------------------------------------------

# --------------------- Analisador Sintatico ------------------------------------------
#escopo, cadeia, token, categoria, tipo
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
                'Linha: ' + str(line+1) + '. ' + 'Esperado um identificador válido. Mas encontrado: ' + ch)

    else:
        raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado iniciar com um identificador válido ' +
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
            raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado encontrar ' + '"end"' +
                            ' Mas encontrado: ' + ch)

    else:
        raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado encontrar ' + '"begin"' +
                        ' Mas encontrado: ' + ch)

def dc():
    global ch
    global catTS
    global escopoTS

    escopoTS = 'global'
    if ch == 'var':
        catTS = 'var'
        dc_v()
        mais_dc()
    elif ch == 'procedure':
        catTS = 'proc'
        dc_p()
        mais_dc()
    else:
        raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado um identificador de variável ' + '"var"' +
                        ' ou de função ' + '"procedure"' + ' válido. Mas encontrado: ' + ch)

def mais_dc():
    global ch

    if ch == ';':
        ch = proxsimb()
        dc()

def dc_v():
    global ch
    global tokenTS
    global catTS

    if ch == 'var':
        tokenTS = 'ident'
        catTS = 'var'
        ch = proxsimb()
        
        variaveis()
        if ch == ':':
            ch = proxsimb()
            tipo_var()

            #-------------- TABELA DE SIMBOLOS ------------
            #Atualiza tabela de simbolos com o tipo das variaiveis, após passar as verificações
            updateTSTipoVariavies(escopoTS, lista_varTS, catTS, tipoVariavelTS)
            #Limpa Buffer de variaveis apos terminar as declaracoes
            lista_varTS.clear()
            #-----------------------------------------------

        else:
            raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado ' + '":"' + '. Mas encontrado: ' + ch)
    else:
        raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado um identificador de variável ' +
                        '"var"' + ' válido. Mas encontrado: ' + ch)

def variaveis(contexto='semcomando'):
    global ch
    global lista_varTS

    if ch.isalpha() and ch not in palavra_reservada:
        #Verifica na tabela de simbolos se o token ja foi inserido
        if contexto == 'semcomando':
            if not buscarTS(escopoTS, ch):
                #inserindo na lista as variaveis
                lista_varTS.append(ch)
                #Inserindo na tabela de simbolos
                inserirTSVariaveis(escopoTS, ch, tokenTS, catTS)
                ch = proxsimb()
                mais_var()
            else:
                raise Exception(
                    'Linha: ' + str(line+1) + '. ' + 'Identificador: ' + "'"+ch+"'" + ' ja declarado anteriormente.')
        elif contexto == 'comando':
            if buscarTS(escopoTS, ch):
                #Função para verificar o tipo - read e write
                ch = proxsimb()
                #restoIdent()
            else:
                raise Exception(
                    'Linha: ' + str(line+1) + '. ' + 'Identificador: ' + "'"+ch+"'" + ' usado mas não refenciado neste escopo')
    else:
      raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado um identificador válido. Mas encontrado: ' + ch)

def mais_var():
    global ch

    if ch == ',':
        ch = proxsimb()
        variaveis()

def tipo_var():
    global ch
    global tipoVariavelTS

    if(ch == 'integer'):
        tipoVariavelTS = ch
        ch = proxsimb()
    elif(ch == 'real'):
        tipoVariavelTS = ch
        ch = proxsimb()
    else:
        raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado um tipo ' +
                        '"integer ou real"' + ' Mas encontrado: ' + ch)

def dc_p():
    global ch
    global escopoTS

    if ch == 'procedure':
        ch = proxsimb()
        if ch.isalpha() and ch not in palavra_reservada:
           #Verifica se o procedimento ja foi declarado anteriormente
            if not buscarTS(escopoTS, ch):
                #insere nome do procedimento na TS
                inserirTS(escopoTS, ch, 'ident', 'proc', '-')

                #Muda o nome do escopo para o nome do procedimento -- inicia-se um escopo local
                escopoTS = ch

                ch = proxsimb()
                parametros()
                ch = proxsimb()
                corpo_p()
            else:
                raise Exception(
                'Linha: ' + str(line+1) + '. ' + 'Procedimento: ' + ch + ' ja declarado anteriormente.')
        else:
            raise Exception(
                'Linha: ' + str(line+1) + '. ' + 'Esperado um identificador válido. Mas encontrado: ' + ch)
    else:
        raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado um identificador de procedimento ' +
                        '"procedure"' + ' válido. Mas encontrado: ' + ch)

def parametros():
    global ch

    if ch == '(':
        ch = proxsimb()
        lista_par()

        if ch != ')':
            raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado um ' + '")"' + ' Mas encontrado: ' + ch)
    else:
        raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado um ' + '"("' + ' Mas encontrado: ' + ch)


def lista_par():
    global ch
    global catTS

    catTS = 'parametro'
    variaveis()
    if ch == ':':
        ch = proxsimb()
        tipo_var()

        #-------------- TABELA DE SIMBOLOS ------------
        #Atualiza tabela de simbolos com o tipo das variaiveis, após passar as verificações
        updateTSTipoVariavies(escopoTS, lista_varTS, catTS, tipoVariavelTS)
        #Limpa Buffer de variaveis apos terminar as declaracoes
        lista_varTS.clear()
        #-----------------------------------------------
        mais_par()

def mais_par():
    global ch

    if ch == ';':
        ch = proxsimb()
        lista_par()

def corpo_p():
    global ch
    global escopoTS

    dc_loc()
    if ch == 'begin':
        ch = proxsimb()
        comandos()
        if ch == 'end':
            #Deletar as variaveis de contexto local
            removerTS(escopoTS)
            #Voltar escopo para global
            escopoTS = 'global'
            ch = proxsimb()
        else:
            raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado encontrar ' + '"end"' +
                            ' Mas encontrado: ' + ch)
    else:
        raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado encontrar ' + '"begin"' +
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

def lista_arg(escopoLocal):
    global ch

    if ch == '(':
        ch = proxsimb()
        argumentos()

        verificaParametros(escopoLocal, escopoTS)
        if ch == ')':
            ch = proxsimb()
        else:
            raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado encontrar ' + '")"' +
                            ' Mas encontrado: ' + ch)

def argumentos():
    global ch, parametrosPassados

    if ch.isalpha() and ch not in palavra_reservada:
        #Buscar na TS se cadeia foi declarada anteriormente
        #Verificar se a quantidade de argumentos declarada corresponde ao que esta sendo enviado
        #Verificar o tipo declarado na TS com o tipo passado
        if buscarTS(escopoTS, ch):
            parametrosPassados.append(ch)
            ch = proxsimb()
            mais_ident()
        else:
            raise Exception(
                        'Linha: ' + str(line+1) + '. ' + 'Identificador: ' + "'"+ch+"'" + ' não refenciado')

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
    global ch, temDivisao

    if ch == 'read':
        ch = proxsimb()
        if ch == '(':
            ch = proxsimb()
            variaveis('comando')

            if ch == ')':
                ch = proxsimb()
            else:
                raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado um ' + '")"' +
                                ' Mas encontrado: ' + ch)
        else:
            raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado um ' + '"("' + ' Mas encontrado: ' + ch)

    elif ch == 'write':
        ch = proxsimb()
        if ch == '(':
            ch = proxsimb()
            variaveis('comando')
            
            if ch == ')':
                ch = proxsimb()
            else:
                raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado um ' + '")"' +
                                ' Mas encontrado: ' + ch)
        else:
            raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado um ' + '"("' + ' Mas encontrado: ' + ch)

    elif ch == 'while':
        ch = proxsimb()
        condicao()
        #Se existir uma divisão na expressão, verificar se os numeros são todos inteiros
        if temDivisao == True:
            verificarDivisao(escopoTS)
            temDivisao = False
        #limpando o buffer pois neste contexto não existe uma variavel para receber o tipo da expressão
        variaveisExpressao.clear()
        if ch == 'do':
            ch = proxsimb()
            comandos()
            if ch == '$':
                ch = proxsimb()
            else:
                raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado o simbolo ' +
                                '"$"' + ' Mas encontrado: ' + ch)
        else:
            raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado o comando ' + '"do"' +
                            ' Mas encontrado: ' + ch)

    elif ch == 'if':
        ch = proxsimb()
        condicao()
        #Se existir uma divisão na expressão, verificar se os numeros são todos inteiros
        if temDivisao == True:
            verificarDivisao(escopoTS)
            temDivisao = False
        #limpando o buffer pois neste contexto não existe uma variavel para receber o tipo da expressão
        variaveisExpressao.clear()
        if ch == 'then':
            ch = proxsimb()
            comandos()
            p_falsa()

            if ch == '$':
                ch = proxsimb()
            else:
                raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado o simbolo ' +
                                '"$"' + ' Mas encontrado: ' + ch)
        else:
            raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado o comando ' +
                            '"then"' + ' Mas encontrado: ' + ch)

    elif ch.isalpha() and ch not in palavra_reservada:
        #Verificar se essa cadeia ja foi declarada para ser usada
        #Verificar o escopo quando ela estiver sendo utilizada
        if buscarTS(escopoTS, ch):
            ch = proxsimb()
            restoIdent()
        else:
            raise Exception(
                'Linha: ' + str(line+1) + '. ' + 'Variavel ou procedimento: ' + "'"+ch+"'" + ' referenciado mas não declarado')

def restoIdent():
    global ch, temDivisao

    if ch == ':=':
        variavelRecebedora = voltaSimb()
        ch = proxsimb()
        expressao()
        #Se existir uma divisão na expressão, verificar se os numeros são todos inteiros
        if temDivisao == True:
            verificarDivisao(escopoTS)
            temDivisao = False
        # Verificar se o valor que a expressão retorna é compativel com a variavel declarada
        verificaTipoExpressao(variavelRecebedora, escopoTS)
    else:
        #Verificar se esse token é proc
        ch_ant = voltaSimb()
        lista_arg(ch_ant)

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
            'Linha: ' + str(line+1) + '. ' + 'Esperado encontrar um operador relacional valido. Mas encontrado: ' + ch)

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
            'Linha: ' + str(line+1) + '. ' + 'Esperado encontrar um operador aritmetico valido. Mas encontrado: ' + ch)

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
    global ch, temDivisao

    if ch == '*' or ch == '/':
        if ch == '/':
            temDivisao = True
        ch = proxsimb()
    else:
      raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado encontrar um operador aritmetico valido. Mas encontrado: ' + ch)

def fator():
    global ch

    if ch.isalpha():
        if buscarTS(escopoTS, ch):
            #Realizar verificação de escopo quando a variavel for declarada ou estiver sendo usada
            variaveisExpressao.append(ch)
            ch = proxsimb()
        else:
            raise Exception(
                'Linha: ' + str(line+1) + '. ' + 'Identificador: ' + "'"+ch+"'" + ' não refenciado')

    elif ch == '(':
        ch = proxsimb()
        expressao()

        if ch == ')':
            ch = proxsimb()
        else:
            raise Exception('Linha: ' + str(line+1) + '. ' + 'Esperado um ' + '")"' + ' Mas encontrado: ' + ch)
    
    elif (ch not in delimitador and ch not in operador_aritmetico and ch not in operador_relacional and not isFloat(ch)):
        inserirTS(escopoTS, ch, 'num', '-', 'integer', ch)
        variaveisExpressao.append(ch)
        ch = proxsimb()

    elif(ch not in delimitador and ch not in operador_aritmetico and ch not in operador_relacional and isFloat(ch)):
        inserirTS(escopoTS, ch, 'num', '-', 'float', ch)
        variaveisExpressao.append(ch)
        ch = proxsimb()
    
#--------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    lexico()
    iniciaVariaveis()
    programa()
    print('\nCadeia Aceita!!!\n\n')
    imprimirTS()
    