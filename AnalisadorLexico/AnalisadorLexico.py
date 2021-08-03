# ALUNO: PEDRO VINICIUS SEMIN ZENERE
# RGA: 201711310054
import nltk

#Cria lista de palavras chaves
palavra_reservada = ['if', 'else', 'for', 'while', 'then', '$', 'do', 'write', 'read', 'begin', 'end', 'var', 'integer', 'real', 'procedure']
operador_relacional = ['<', '>', '==', '<=', '>=']
operador_aritmetico = ['+', '-', '*', '/']
delimitador = [';', ',']
atrib = ['=', ':=', ':']
num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

#Expressões Regulares 
ident = '[^\W\d_]+'
pont = '\(|\)|\;|\:|\$|\,'
numeros = '\d\.\d*|\.\d*|\d+'
decimal = '[-+]?\d*\.?\d+|[-+]?\d+'
comentarios = '/\*.*?\*/'
comentarios2 = '\{.*?\}'
op_arit = '\+|\-|\*|\/'
op_rel = '(?:<=?|>=?|==|!=)'
atrib = '\:='

#Abrindo arquivo
def readfile():
    with open('exemplo.txt', 'r') as arq:
        texto = arq.readlines()
        return texto
    
def separaTokens():
    texto = readfile()
    reg = atrib + '|' + ident + '|' + pont + '|' + decimal + '|' + comentarios + '|' + comentarios2 + '|' + op_arit + '|' + op_rel

    #Separando cada Token e colocando em uma lista
    tokenizer = nltk.RegexpTokenizer(reg)
    print (" \n============== Lista de Tokens Classificados  =================\n\n")
    
    countLines = 1
    for line in texto:
        termList = tokenizer.tokenize(line)
        if len(termList) != 0:
            classifaTokens(termList, countLines)
        countLines += 1
        
def classifaTokens(line, countLines):
    for w in line:
        if(w in palavra_reservada):
            print(w + ', Palavra Reservada')
        elif(w.isalpha() and w not in palavra_reservada):
            print(w + ', Identificador')
        elif(w in operador_relacional):
            print(w + ', Operador Relacional')
        elif(w in atrib):
            print(w + ', Atribuição')
        elif(w in delimitador):
                print(w + ', Delimitador')
        elif(w in operador_aritmetico):
            print(w + ', Operador Aritmetico')
        elif(w == '('):
            print(w + ', Abre parenteses')
        elif(w == ')'):
            print(w + ', Fecha parenteses')
        else:
            t = list(w)
            if(t[0] in num):
                if('.' in t):
                    print(w+', Numero real')
                else:
                    print(w + ', Numero Inteiro')
            elif(t[0] == '/' and t[1] == '*' or t[0] == '{'):
                print(w + ', Comentario')
            else:
                print(w + ', Erro Léxico')
                raise Exception('Erro Léxico na linha ' + str(countLines) + '. O token ' + w + ' não pertence a gramatica')
                break

def main():
    separaTokens()

if __name__ == "__main__":
    main()   