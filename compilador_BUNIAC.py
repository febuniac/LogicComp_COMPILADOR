#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re #importing regular expression

#___________________________________________________________________________________________________
#Tipos de Token (constantes)
INT = "INT"
FUNC = "FUNC"
PLUS = "PLUS"
MINUS = "MINUS"
MULT = "MULT"
DIV = "DIV"
EOF = "EOF" #end of file
OPEN_PAR = "OPEN_PAR"
CLOSE_PAR = "CLOSE_PAR"
OPEN_KEY = "OPEN_KEY"
CLOSE_KEY = "CLOSE_KEY"
ASSIGN = "ASSIGN"
PRINTF ="PRINTF"
IDENTIFIER = "IDENTIFIER"
SEMICOLON ="SEMICOLON"
OR= "OR"
AND= "AND"
IF= "IF"
BIGGER_THAN= "BIGGER_THAN"
SMALLER_THAN= "SMALLER_THAN"
EQUAL_TO= "EQUAL_TO"
ELSE= "ELSE"
WHILE = "WHILE"
SCANF = "SCANF"
NOT = "NOT"
MAIN = "MAIN"
CHAR = "CHAR"
VOID = "VOID"
COMMA="COMMA"
FUNCCALL="FUNCCALL"
RETURN="RETURN"
TYPES = ["VOID","INT","CHAR"]

#___________________________________________________________________________________________________
#Leitura de Arquivo
#entrada = (str(input("Conta: ")))#entrada do usuário
with open('inputCompiler.txt') as entrada:
  inputCompiler = entrada.read()
  inputCompiler = inputCompiler.replace("\n"," ")
  inputCompiler = inputCompiler.replace("   "," ")
  #inputCompiler = inputCompiler.replace(" ","")
#   while ("  ") in inputCompiler:
#     inputCompiler.replace("  "," ")
#___________________________________________________________________________________________________
class SymbolTable:
    dictionary = {}
    def __init__(self,ancestor):
        pass
    def get_nome(self,nome):
        #recursivamente olhar para todas as symboltables
        return SymbolTable.dictionary[str(nome)]
        #return self.nome
    def set_nome_valor_tipo(self,nome,valor,tipo):
        SymbolTable.dictionary[nome] = [valor,tipo]
        #self.nome = valor

# SymbolTable = SymbolTable()
      
class Node:
    # Constructor to create a new Node
    def __init__(self,valor,children):
        self.valor = valor  
        self.children = children
    def Evaluate(self,SymbTab):
        pass

class Identifier(Node):#Identificador
    def __init__(self,nome,valor):#
        self.nome = nome
        self.valor = valor #valor do nó
    def Evaluate(self,SymbTab):
        #global SymbolTable
        return SymbolTable.get_nome(self.nome)#get do nome na symbol table


class Assign(Node):#Assign Operation
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self,SymbTab):
        #gravando na symboltable o valor da atribuição
        valor = self.children[1].Evaluate()
        SymbolTable.set_nome_valor_tipo(self.children[0].nome, valor[0], valor[1])#valor dó nó é o nome da variavel 


class Comandos(Node):#Comandos Operation
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self,SymbTab):
        #print(self.children)
        for child in self.children:
            child.Evaluate(SymbTab)#child percorre a lista de children e vai dando evaluate
        
        
class BinOp(Node):#Binary Operation
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self,SymbTab):
        val_esq=self.children[0].Evaluate(SymbTab)
        val_dir=self.children[1].Evaluate(SymbTab)
        if(self.valor == 'PLUS'):
            if val_esq[1] == val_dir[1] and val_esq[1] == INT:
                return [val_esq[0] + val_dir[0], INT]
            else:
                raise Exception("Erro: tipos incompatíveis int PLUS")
        elif (self.valor == 'MINUS'):
            if val_esq[1] == val_dir[1] and val_esq[1] == INT:
                return [val_esq[0] - val_dir[0], INT]
            else:
                raise Exception("Erro: tipos incompatíveis int MINUS")
        elif (self.valor == 'MULT'):
            if val_esq[1] == val_dir[1] and val_esq[1] == INT:
                return [val_esq[0] * val_dir[0], INT]
            else:
                raise Exception("Erro: tipos incompatíveis int MULT")
        elif (self.valor == 'DIV'):
            if val_esq[1] == val_dir[1] and val_esq[1] == INT:
                return [val_esq[0] // val_dir[0], INT]
            else:
                raise Exception("Erro: tipos incompatíveis int DIV")
        elif self.valor == 'OR':
            if val_esq[1] == val_dir[1] and val_esq[1] == CHAR:
                return [val_esq[0] or val_dir[0], CHAR]
            else:
                raise Exception("Erro: tipos incompatíveis char OR")
        elif self.valor == 'AND':
            if val_esq[1] == val_dir[1] and val_esq[1] == CHAR:
                return [val_esq[0] and val_dir[0], CHAR]
            else:
                raise Exception("Erro: tipos incompatíveis char AND")    
        elif self.valor == 'BIGGER_THAN':
            if val_esq[1] == val_dir[1] and val_esq[1] == INT:
                return [val_esq[0] > val_dir[0], CHAR]
            else:
                raise Exception("Erro: tipos incompatíveis char BIGGER_THAN")
        elif self.valor == 'SMALLER_THAN':
            if val_esq[1] == val_dir[1] and val_esq[1] == INT:
                return [val_esq[0] < val_dir[0], CHAR]
            else:
                raise Exception("Erro: tipos incompatíveis char SMALLER_THAN")               
        elif self.valor == 'EQUAL_TO':
            if val_esq[1] == val_dir[1] and val_esq[1] == INT:
                return [val_esq[0] == val_dir[0], CHAR]
            else:
                raise Exception("Erro: tipos incompatíveis char EQUAL_TO")               
class Printf(Node):
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self,SymbTab):
        print(self.children.Evaluate(SymbTab)[0])

class UnOp(Node):#Unary Operation
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self,SymbTab):
        val_unico=self.children[0].Evaluate(SymbTab)
        if (self.valor == 'PLUS'):
            if val_unico[1] == INT:
                return [+val_unico,INT]
            else:
                raise Exception("Erro: tipos incompatíveis char PLUS")
        elif (self.valor == 'MINUS'):
            if val_unico[1] == INT:
                return [-val_unico,INT]
            else:
                raise Exception("Erro: tipos incompatíveis char MINUS") 
        elif self.valor == 'NOT':
            if val_unico[1] == CHAR:
                return [not val_unico, CHAR]
            else:
                raise Exception("Erro: tipos incompatíveis char NOT") 

class IntVal(Node):#Integer Value
    def __init__(self,valor):
        self.valor = valor
    def Evaluate(self,SymbTab):
        return [self.valor, INT]

class NoOp(Node):#No Operation
    def Evaluate(self,SymbTab):
        return None

class Scanf(Node):
    def __init__(self,valor):
        self.valor = valor
    def Evaluate(self,SymbTab):
        return [input(""), INT]

class If(Node):
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self,SymbTab):
        val_esq=self.children[0].Evaluate(SymbTab)[0]
        if val_esq == True:
            self.children[1].Evaluate(SymbTab)
        else:
            self.children[2].Evaluate(SymbTab)

class While(Node):
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self,SymbTab):
        while self.children[0].Evaluate(SymbTab)[0]==True:
            self.children[1].Evaluate(SymbTab)

class Type(Node):#Type Def
    def __init__(self,valor):
        self.valor = valor
        self.children = None
    def Evaluate(self,SymbTab):
        if (self.valor == 'INT'):
            return [0, INT]#0 é valor default de int
        elif (self.valor == 'CHAR'):
            return [0, CHAR]
        elif self.valor == 'VOID':
            return [None, VOID]#MNone é valor default de char
        # elif self.valor == 'FUNC':
        #     return [None, FUNC]#MNone é valor default de char

class VarDec(Node):#Variable Declaration
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self,SymbTab):
        tipo=self.children[0].Evaluate(SymbTab)
        for child in self.children:
            SymbolTable.set_nome_valor_tipo(self.children[0].valor, tipo[0], tipo[1])#tipo [0] é o valor default e e tipo[1] é o tipo (ex: no nó Type return [0, CHAR])

class FuncDec(Node):
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self,SymbTab):
       SymbolTable.set_nome_valor_tipo(self.valor, self, FUNC)#valor é o nome da função e vai pegar ele mesmo e se colocar como valor(self)

class FuncCall(Node):
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self,SymbTab):

        dec = SymbolTable.get_nome(self.valor)[0]
        #Criar uma nova symboltable
        # Criar uma variavel com o nome da funcao e tipo correto.
        tipo = dec.children[0].Evaluate(SymbTab)
        SymbolTable.set_nome_valor_tipo(self.valor, tipo[0], tipo[1])#cria uma nova symboltable
        if len(self.children) != len(dec.children)-2:#se o num de argumentos passados for diferente
            raise Exception("Erro: Número de argumentos inválidos")
        # Declarar os argumentos da função 
        for i in range(1, len(dec.children)-1):#primeiro é o tipo e ultimo é comandos (são ignorados)
            dec.children[i].Evaluate(SymbTab) #declara os argumento
            arg = self.children[i-1].Evaluate(SymbTab) # resolve os argumentos
            SymbolTable.set_nome_valor_tipo(dec.children[i].valor, arg[0], arg[1]) #seta o valor dos argumentos arg[0]=valor e arg[1]=tipo

        for child in dec.children[-1].children:
            if type(child) is Return:
                ret = child.Evaluate(SymbTab)
                SymbolTable.set_nome_valor_tipo(self.valor,ret[0],ret[1])
                return ret
            else:
                child.Evaluate(SymbTab)

        #dec.children[-1].Evaluate()#Executando o comandos    

class Return(Node):
    def __init__(self,children):
        self.children = children
    def Evaluate(self,SymbTab):
        #dec = SymbolTable.get_nome(self.valor)[0]
        return self.children[0].Evaluate(SymbTab)
#___________________________________________________________________________________________________
#Class Token
class Token:
    def __init__(self,tipo,valor):
        self.tipo=tipo#tipo (string-token type);
        self.valor=valor#valor (integer-token value);
#___________________________________________________________________________________________________
#Classe Tokenizador
class Tokenizador:
    def __init__(self,origem):
        self.origem = origem#origem (string-codigo fonte tokenizado)-> conta matemática(entrada do usuario)
        self.posicao = 0#posição (integer-posição atual que tokenizador irá separar);
        self.atual = Token(EOF,EOF)#atual (token-ultimo token separado);
    
    def olhaProximo(self):
        posicao = self.posicao

        digito =""#Para numeros com mais de 1 digito
        string=[]#Para palvras com mais de 1 char
        #sempre aqui pois pega um token de cada vez
        
        while posicao < len(self.origem) and (self.origem[posicao] == " "):#limpando os espaços
            posicao+=1#atualiza a posição
        if posicao >= len(self.origem):#checa o tamanho da string de entrada
            token = Token(EOF,'null')#Para o fim da string
            self.atual=token#atualiza o atual
        else:
            #Tratando comentários
            if ((self.origem[posicao])=="/"): #(p and q) ao negar (not p or not q) # era antes :  if ((self.origem[self.posicao])=="/" and (self.origem[self.posicao])=="*")
                posicao+=1
                if (self.origem[posicao])=="*":
                    posicao+=1
                    comentario = True #flag de comentarios
                    while (comentario):
                        while (self.origem[posicao]!="*"): # era antes :  while not (self.origem[self.posicao]=="*" and self.origem[self.posicao+1]=="/"):
                            posicao+=1
                            if(posicao >= len(self.origem)):
                                raise Exception("Erro: Comentário sem fim")
                        posicao+=1
                        if(self.origem[posicao]=="/"):
                            comentario = False    
                            posicao+=1
                else:
                    token = Token(DIV,"/")
                    self.atual=token
                    return
            
            while posicao < len(self.origem) and (self.origem[posicao] == " "):#limpando os espaços
                posicao+=1#atualiza a posição
            #    if re.search('[0-9] +[0-9]', entrada):
            #        raise Exception("Erro: Digito seguido de digito")
            if posicao >= len(self.origem):#checa o tamanho da string de entrada
                token = Token(EOF,'null')#Para o fim da string
                self.atual=token#atualiza o atual
            elif (self.origem[posicao]).isdigit():#se for digito
               
                while (posicao<(len(self.origem)) and (self.origem[posicao]).isdigit()):
                    
                    digito +=self.origem[posicao]
                    posicao+=1

                token = Token(INT,int(digito))
                self.atual=token

            elif (self.origem[posicao]).isalpha():#se for string

                while(self.origem[posicao].isalpha() or self.origem[posicao].isdigit() or self.origem[posicao] == "_"):
                    string.append(self.origem[posicao])
                    posicao+=1
                
                fullString = ''.join(map(str, string))#converte a lista de chars para uma string
                if(fullString == "printf"):    
                    token = Token('PRINTF', fullString)
                elif(fullString == "if"):    
                    token = Token('IF', fullString)
                elif(fullString == "else"):    
                    token = Token('ELSE', fullString)
                elif(fullString == "while"):    
                    token = Token('WHILE', fullString)
                elif(fullString == "scanf"):    
                    token = Token('SCANF', fullString)
                # elif(fullString == "main"):    
                #     token = Token('MAIN', fullString)
                elif(fullString == "int"):    
                    token = Token('INT', fullString)
                elif(fullString == "char"):    
                    token = Token('CHAR', fullString) 
                elif(fullString == "void"):    
                    token = Token('VOID', fullString)
                elif(fullString == "return"):    
                    token = Token('RETURN', fullString)          
                else:
                    token = Token('IDENTIFIER', fullString)
                return token

            elif self.origem[posicao] == '+':
                token = Token(PLUS,"+")
                posicao+=1
                return token

            elif self.origem[posicao] == '-':
                token = Token(MINUS,"-")
                posicao+=1
                return token

            elif self.origem[posicao] == '*':
                token = Token(MULT,"*")
                posicao+=1
                return token
           
            elif self.origem[posicao] == '(':
                token = Token(OPEN_PAR,"")
                posicao+=1
                return token
            
            elif self.origem[posicao] == ')':
                token = Token(CLOSE_PAR,"")
                posicao+=1
                return token
            
            elif self.origem[posicao] == '{':
                token = Token(OPEN_KEY,"")
                posicao+=1
                return token
            
            elif self.origem[posicao] == '}':
                token = Token(CLOSE_KEY,"")
                posicao+=1
                return token
            
            elif self.origem[posicao] == '=':
                token = Token(ASSIGN,"")
                posicao+=1
                return token

            elif self.origem[posicao] == ';':
                token = Token(SEMICOLON,"")
                posicao+=1
                return token
            
            elif self.origem[posicao] == '||':
                token = Token(OR,"")
                posicao+=1
                return token
            
            elif self.origem[posicao] == '&&':
                token = Token(AND,"")
                posicao+=1
                return token
            
            elif self.origem[posicao] == '>':
                token = Token(BIGGER_THAN,"")
                posicao+=1
                return token
            
            elif self.origem[posicao] == '<':
                token = Token(SMALLER_THAN,"")
                self.posicao+=1
                return token
            
            elif self.origem[posicao] == '==':
                token = Token(EQUAL_TO,"")
                posicao+=1
                return token
            
            elif self.origem[posicao] == "!":
                token = Token(NOT,"")
                posicao+=1
                return token
           
            elif self.origem[posicao] == ',':
                token = Token(COMMA,"")
                posicao+=1
                return token


    #lê o próximo token e atualiza o atributo atual
    def selecionarProximo(self):
        digito =""#Para numeros com mais de 1 digito
        string=[]#Para palvras com mais de 1 char
        #sempre aqui pois pega um token de cada vez
        
        while self.posicao < len(self.origem) and (self.origem[self.posicao] == " "):#limpando os espaços
            self.posicao+=1#atualiza a posição
            #if re.search('[0-9]+[0-9]', entrada):
            #    raise Exception("Erro: Digito seguido de digito")
        if self.posicao >= len(self.origem):#checa o tamanho da string de entrada
            token = Token(EOF,'null')#Para o fim da string
            self.atual=token#atualiza o atual
        else:
            #Tratando comentários
            if ((self.origem[self.posicao])=="/"): #(p and q) ao negar (not p or not q) # era antes :  if ((self.origem[self.posicao])=="/" and (self.origem[self.posicao])=="*")
                self.posicao+=1
                if (self.origem[self.posicao])=="*":
                    self.posicao+=1
                    comentario = True #flag de comentarios
                    while (comentario):
                        while (self.origem[self.posicao]!="*"): # era antes :  while not (self.origem[self.posicao]=="*" and self.origem[self.posicao+1]=="/"):
                            self.posicao+=1
                            if(self.posicao >= len(self.origem)):
                                raise Exception("Erro: Comentário sem fim")
                        self.posicao+=1
                        if(self.origem[self.posicao]=="/"):
                            comentario = False    
                            self.posicao+=1
                else:
                    token = Token(DIV,"/")
                    self.atual=token
                    return
            
            while self.posicao < len(self.origem) and (self.origem[self.posicao] == " "):#limpando os espaços
                self.posicao+=1#atualiza a posição
            #    if re.search('[0-9] +[0-9]', entrada):
            #        raise Exception("Erro: Digito seguido de digito")
            if self.posicao >= len(self.origem):#checa o tamanho da string de entrada
                token = Token(EOF,'null')#Para o fim da string
                self.atual=token#atualiza o atual
            elif (self.origem[self.posicao]).isdigit():#se for digito
               
                while (self.posicao<(len(self.origem)) and (self.origem[self.posicao]).isdigit()):
                    
                    digito +=self.origem[self.posicao]
                    self.posicao+=1

                token = Token(INT,int(digito))
                self.atual=token

            elif (self.origem[self.posicao]).isalpha():#se for string

                while(self.origem[self.posicao].isalpha() or self.origem[self.posicao].isdigit() or self.origem[self.posicao] == "_"):
                    string.append(self.origem[self.posicao])
                    self.posicao+=1
                
                fullString = ''.join(map(str, string))#converte a lista de chars para uma string
                if(fullString == "printf"):    
                    token = Token('PRINTF', fullString)
                elif(fullString == "if"):    
                    token = Token('IF', fullString)
                elif(fullString == "else"):    
                    token = Token('ELSE', fullString)
                elif(fullString == "while"):    
                    token = Token('WHILE', fullString)
                elif(fullString == "scanf"):    
                    token = Token('SCANF', fullString)
                # elif(fullString == "main"):    
                #     token = Token('MAIN', fullString)
                elif(fullString == "int"):    
                    token = Token('INT', fullString)
                elif(fullString == "char"):    
                    token = Token('CHAR', fullString) 
                elif(fullString == "void"):    
                    token = Token('VOID', fullString)  
                elif(fullString == "return"):    
                    token = Token('RETURN', fullString) 
                else:
                    token = Token('IDENTIFIER', fullString)
                self.atual = token

            elif self.origem[self.posicao] == '+':
                token = Token(PLUS,"+")
                self.posicao+=1
                self.atual=token

            elif self.origem[self.posicao] == '-':
                token = Token(MINUS,"-")
                self.posicao+=1
                self.atual=token

            elif self.origem[self.posicao] == '*':
                token = Token(MULT,"*")
                self.posicao+=1
                self.atual=token
           
            elif self.origem[self.posicao] == '(':
                token = Token(OPEN_PAR,"")
                self.posicao+=1
                self.atual=token
            
            elif self.origem[self.posicao] == ')':
                token = Token(CLOSE_PAR,"")
                self.posicao+=1
                self.atual=token
            
            elif self.origem[self.posicao] == '{':
                token = Token(OPEN_KEY,"")
                self.posicao+=1
                self.atual=token
            
            elif self.origem[self.posicao] == '}':
                token = Token(CLOSE_KEY,"")
                self.posicao+=1
                self.atual=token
            
            elif self.origem[self.posicao] == '=':
                token = Token(ASSIGN,"")
                self.posicao+=1
                self.atual=token

            elif self.origem[self.posicao] == ';':
                token = Token(SEMICOLON,"")
                self.posicao+=1
                self.atual=token
            
            elif self.origem[self.posicao] == '||':
                token = Token(OR,"")
                self.posicao+=1
                self.atual=token
            
            elif self.origem[self.posicao] == '&&':
                token = Token(AND,"")
                self.posicao+=1
                self.atual=token
            
            elif self.origem[self.posicao] == '>':
                token = Token(BIGGER_THAN,"")
                self.posicao+=1
                self.atual=token
            
            elif self.origem[self.posicao] == '<':
                token = Token(SMALLER_THAN,"")
                self.posicao+=1
                self.atual=token
            
            elif self.origem[self.posicao] == '==':
                token = Token(EQUAL_TO,"")
                self.posicao+=1
                self.atual=token
            
            elif self.origem[self.posicao] == "!":
                token = Token(NOT,"")
                self.posicao+=1
                self.atual=token
           
            elif self.origem[self.posicao] == ',':
                token = Token(COMMA,"")
                self.posicao+=1
                self.atual=token

#___________________________________________________________________________________________________
#Classe Analisador(estática)
#tokens (Tokenizador-ler código fonte e alimentar o Analisador)
class Analisador:
    tokens = None
    #consome tokens do Tokenizador e análisa se a sintaxe está aderente à grámatica proposta
    def inicializar(texto):
        Analisador.tokens = Tokenizador(texto)#inicializa o atributo Tokenizador dentro da classe Analisador(classe estatica por isso é necessário)
        Analisador.tokens.selecionarProximo()

    def analisarExpressao():
        resultado = Analisador.analisarTermo()

        while (Analisador.tokens.atual.tipo == PLUS or Analisador.tokens.atual.tipo == MINUS):
            op = Analisador.tokens.atual.tipo
            Analisador.tokens.selecionarProximo()
            resultado = BinOp(op,[resultado, Analisador.analisarTermo()])
        return resultado

    def analisarTermo():
        resultado = Analisador.analisarFator()
        while (Analisador.tokens.atual.tipo == MULT or Analisador.tokens.atual.tipo == DIV):
            op = Analisador.tokens.atual.tipo
            Analisador.tokens.selecionarProximo()
            resultado = BinOp(op,[resultado, Analisador.analisarFator()])
        return resultado

    def analisarFator():
        #resultado=None
        if Analisador.tokens.atual.tipo == INT:
            resultado = IntVal(Analisador.tokens.atual.valor)
            Analisador.tokens.selecionarProximo()

        elif (Analisador.tokens.atual.tipo == PLUS or Analisador.tokens.atual.tipo == MINUS):#Plus e Minus unários ( sinais positivo e negativo)
            op = Analisador.tokens.atual.tipo
            Analisador.tokens.selecionarProximo()
            resultado = UnOp(op,[Analisador.analisarFator()])

        elif (Analisador.tokens.atual.tipo == OPEN_PAR):
           Analisador.tokens.selecionarProximo()
           resultado = Analisador.analisarExpressao()
           if (Analisador.tokens.atual.tipo == CLOSE_PAR):
               Analisador.tokens.selecionarProximo()
           else:
                raise Exception("Erro: Parentesês não fecha") 
        elif (Analisador.tokens.atual.tipo == IDENTIFIER):
            #resultado = Identifier(Analisador.tokens.atual.valor, Analisador.tokens.atual.tipo)
            #Analisador.tokens.selecionarProximo()
            if (Analisador.tokens.olhaProximo().tipo == OPEN_PAR):
               #Analisador.tokens.selecionarProximo()
               resultado = Analisador.analisarFuncCall()#funccall
            else:
                resultado = Identifier(Analisador.tokens.atual.valor, Analisador.tokens.atual.tipo)
                Analisador.tokens.selecionarProximo()
        # elif (Analisador.tokens.atual.tipo == FUNCCALL):
        #     Analisador.tokens.selecionarProximo()
        #     resultado = Analisador.analisarFuncCall()#funccall
        else:
            raise Exception("Erro: Expressão inválida (fator)")

        return resultado
    def analisarPrintf():
        #resultado=None
        if (Analisador.tokens.atual.tipo == PRINTF):#Printf
            Analisador.tokens.selecionarProximo()
            if (Analisador.tokens.atual.tipo == OPEN_PAR):
                Analisador.tokens.selecionarProximo()
                resultado = Analisador.analisarExpressao()
                if (Analisador.tokens.atual.tipo == CLOSE_PAR):
                    Analisador.tokens.selecionarProximo()
                    resultado = Printf(PRINTF,resultado)
                    if (Analisador.tokens.atual.tipo == SEMICOLON):#;;
                        Analisador.tokens.selecionarProximo()
                    else:
                        raise Exception("Erro: Expressão inválida (printf)")
                else:
                    raise Exception("Erro: Parentesês não fecha")
            else:
                raise Exception("printf incorreto")
        else:
            raise Exception("Erro: Expressão inválida (printf) ")
        return resultado

    def analisarAtribuicao():
        #resultado=None
        if (Analisador.tokens.atual.tipo == IDENTIFIER):#Atribuição
            resultado = Identifier(Analisador.tokens.atual.valor, Analisador.tokens.atual.tipo)
            Analisador.tokens.selecionarProximo()
            if(Analisador.tokens.atual.tipo == ASSIGN):#=
                op = Analisador.tokens.atual.tipo
                Analisador.tokens.selecionarProximo()                
                # if (Analisador.tokens.olhaProximo().tipo ==  OPEN_PAR):
                #     resultado = Analisador.analisarFuncCall()#funccall
                # else:
                #     op = Analisador.tokens.atual.tipo
                #     Analisador.tokens.selecionarProximo()
                resultado = Assign(op,[resultado, Analisador.analisarExpressao()])
            elif(Analisador.tokens.atual.tipo == SCANF):#scanf
                resultado = Analisador.analisarScanf()
            else:
                raise Exception("Erro: Atribuição inválida (atribuição)")
            if (Analisador.tokens.atual.tipo == SEMICOLON):#;;
                Analisador.tokens.selecionarProximo()
            else:
                raise Exception("Erro: Atribuição inválida (atribuição)")
        return resultado
   
    def analisarComando():
        resultado = None
        if (Analisador.tokens.atual.tipo == OPEN_KEY):#{
            resultado = Analisador.analisarBloco()
        elif (Analisador.tokens.atual.tipo == IDENTIFIER):#id
            resultado = Analisador.analisarAtribuicao()
        elif (Analisador.tokens.atual.tipo == PRINTF):#printf
            resultado = Analisador.analisarPrintf()
        elif (Analisador.tokens.atual.tipo == IF):#if
            resultado = Analisador.analisarIf()
        elif (Analisador.tokens.atual.tipo == WHILE):#while
            resultado = Analisador.analisarWhile()
        elif (Analisador.tokens.atual.tipo in TYPES):#vardec
            resultado = Analisador.analisarVarDec()
        elif (Analisador.tokens.atual.tipo == RETURN):#return
            Analisador.tokens.selecionarProximo()
            if (Analisador.tokens.atual.tipo == OPEN_PAR): 
                Analisador.tokens.selecionarProximo()
                resultado = Return([Analisador.analisarExpressao()])
                if (Analisador.tokens.atual.tipo == CLOSE_PAR): 
                    Analisador.tokens.selecionarProximo()
                    if (Analisador.tokens.atual.tipo == SEMICOLON): 
                        Analisador.tokens.selecionarProximo()
                    else:
                        raise Exception("Erro: Return Incorreto")
                else:
                    raise Exception("Erro:Return Incorreto")
            else:
                raise Exception("Erro: Return Incorreto")
            
        return resultado

    def analisarExpressao_Boolean():
        resultado = Analisador.analisarTermo_Boolean()

        while (Analisador.tokens.atual.tipo == OR):
            op = Analisador.tokens.atual.tipo
            Analisador.tokens.selecionarProximo()
            resultado = BinOp(op,[resultado, Analisador.analisarTermo_Boolean()])
        return resultado

    def analisarTermo_Boolean():
        resultado = Analisador.analisarFator_Boolean()

        while (Analisador.tokens.atual.tipo == AND):
            op = Analisador.tokens.atual.tipo
            Analisador.tokens.selecionarProximo()
            resultado = BinOp(op,[resultado, Analisador.analisarFator_Boolean()])
        return resultado
    def analisarFator_Boolean():
        resultado = Analisador.analisarExpressao_Relacional()

        while (Analisador.tokens.atual.tipo == NOT):
            op = Analisador.tokens.atual.tipo
            Analisador.tokens.selecionarProximo()
            resultado = BinOp(op,[resultado, Analisador.analisarExpressao_Relacional()])
        return resultado
    def analisarExpressao_Relacional():
        resultado = Analisador.analisarExpressao()

        if (Analisador.tokens.atual.tipo == BIGGER_THAN):
            op = Analisador.tokens.atual.tipo
            Analisador.tokens.selecionarProximo()
            resultado = BinOp(op,[resultado, Analisador.analisarExpressao()])
        elif (Analisador.tokens.atual.tipo == SMALLER_THAN):
            op = Analisador.tokens.atual.tipo
            Analisador.tokens.selecionarProximo()
            resultado = BinOp(op,[resultado, Analisador.analisarExpressao()])
        elif (Analisador.tokens.atual.tipo == EQUAL_TO):
            op = Analisador.tokens.atual.tipo
            Analisador.tokens.selecionarProximo()
            resultado = BinOp(op,[resultado, Analisador.analisarExpressao()])
        return resultado
    
    def analisarIf():
        #resultado=None
        if (Analisador.tokens.atual.tipo == IF):#If
            Analisador.tokens.selecionarProximo()
            if (Analisador.tokens.atual.tipo == OPEN_PAR):
                Analisador.tokens.selecionarProximo()
                resultado = [Analisador.analisarExpressao_Boolean()]
                if (Analisador.tokens.atual.tipo == CLOSE_PAR):
                    Analisador.tokens.selecionarProximo()
                    resultado.append(Analisador.analisarBloco())
                    if (Analisador.tokens.atual.tipo == ELSE):#Else
                        Analisador.tokens.selecionarProximo()
                        resultado.append(Analisador.analisarBloco())
                        #resultado = If(IF,resultado)
                    
                    resultado = If(IF,resultado)
                else:
                    raise Exception("Erro: Parentesês não fecha")
            else:
                raise Exception("printf incorreto")
        else:
            raise Exception("Erro: Expressão inválida (printf) ")
        return resultado    
    def analisarWhile():
        #resultado=None
        if (Analisador.tokens.atual.tipo == WHILE):#WHILE
            Analisador.tokens.selecionarProximo()
            if (Analisador.tokens.atual.tipo == OPEN_PAR):
                Analisador.tokens.selecionarProximo()
                resultado = Analisador.analisarExpressao_Boolean()
                if (Analisador.tokens.atual.tipo == CLOSE_PAR):
                    Analisador.tokens.selecionarProximo()
                    resultado = While(WHILE,[resultado, Analisador.analisarBloco()])
                else:
                    raise Exception("Erro: Parentesês não fecha")
            # resultado = Assign(WHILE,[resultado, Analisador.analisarComandos()])#WHILE LÁ EM CIMA
            else:
                raise Exception("while incorreto")
        else:
            raise Exception("Erro: Expressão inválida (while) ")
        return resultado   
    def analisarScanf(): 
        resultado=None
        if (Analisador.tokens.atual.tipo == SCANF):#Scanf
            Analisador.tokens.selecionarProximo()
            if (Analisador.tokens.atual.tipo == OPEN_PAR):
                Analisador.tokens.selecionarProximo()
                if (Analisador.tokens.atual.tipo == CLOSE_PAR):
                    Analisador.tokens.selecionarProximo()
                    resultado = Scanf(SCANF)#SCANF LÁ EM CIMA
                else:
                    raise Exception("Erro: Parentesês não fecha")
            else:
                raise Exception("scanf incorreto")
        else:
            raise Exception("Erro: Expressão inválida (scanf) ")
        return resultado 

    def analisarPrograma():
        resultado = Comandos(None,[])
        while(Analisador.tokens.atual.tipo != EOF):
            tipoA = Analisador.analisarTipo()
            if (Analisador.tokens.atual.tipo == IDENTIFIER):#MAIN
                Func =FuncDec(Analisador.tokens.atual.valor,[tipoA])
                Analisador.tokens.selecionarProximo()
                if (Analisador.tokens.atual.tipo == OPEN_PAR):
                    Analisador.tokens.selecionarProximo()
                    if (Analisador.tokens.atual.tipo == CLOSE_PAR):
                        Analisador.tokens.selecionarProximo()
                        Func.children.append(Analisador.analisarBloco())

                    else:
                        tipoA = Analisador.analisarTipo()
                        if( Analisador.tokens.atual.tipo == IDENTIFIER):
                            Func.children.append(VarDec(Analisador.tokens.atual.valor,[tipoA, Identifier(Analisador.tokens.atual.valor,IDENTIFIER)]))
                            Analisador.tokens.selecionarProximo()
                            while(Analisador.tokens.atual.tipo == COMMA):
                                Analisador.tokens.selecionarProximo()
                                tipoA = Analisador.analisarTipo()
                                #Analisador.tokens.selecionarProximo()
                                if(Analisador.tokens.atual.tipo == IDENTIFIER):
                                    Func.children.append(VarDec(Analisador.tokens.atual.valor,[tipoA, Identifier(Analisador.tokens.atual.valor,IDENTIFIER)]))
                                    Analisador.tokens.selecionarProximo()
                                else:
                                    Exception("Erro: Programa Incorreto")
                            if (Analisador.tokens.atual.tipo == CLOSE_PAR):
                                Analisador.tokens.selecionarProximo()
                                Func.children.append(Analisador.analisarBloco())  
                            else:
                                raise Exception("Erro: Programa Incorreto ")
                        else:
                            raise Exception("Erro: Programa Incorreto ")
                else:
                    raise Exception("Erro: Programa Incorreto ")  
            else:
                raise Exception("Erro: Programa Incorreto ")  
            resultado.children.append(Func)
        # colocar um FuncCall em resultados (Para MAIN)
        resultado.children.append(FuncCall("main",[]))
        return resultado  

    def analisarBloco():
        resultado =  Comandos(None,[])
        if (Analisador.tokens.atual.tipo == OPEN_KEY):#{
            Analisador.tokens.selecionarProximo()
            resultado.children.append(Analisador.analisarComando())
            while (Analisador.tokens.atual.tipo != CLOSE_KEY):#}
                resultado.children.append(Analisador.analisarComando())
                if (resultado == None):
                    break
            Analisador.tokens.selecionarProximo()
        else:
            raise Exception("Erro: Formato de bloco de comando incorreto")
        return resultado

    def analisarVarDec(): 
        resultado = Analisador.analisarTipo()
        if (Analisador.tokens.atual.tipo == IDENTIFIER):#{
            resultado = VarDec(Analisador.tokens.atual.valor,[resultado, Identifier(Analisador.tokens.atual.valor,IDENTIFIER)])
            Analisador.tokens.selecionarProximo()
            while (Analisador.tokens.atual.tipo != SEMICOLON):
                if (Analisador.tokens.atual.tipo == COMMA):#;
                    Analisador.tokens.selecionarProximo()
                    if (Analisador.tokens.atual.tipo == IDENTIFIER):
                        resultado.children.append(Identifier(Analisador.tokens.atual.nome,IDENTIFIER))
                        Analisador.tokens.selecionarProximo()
                    else:
                        raise Exception("Erro: Formato de vardec incorreto")
                else:
                    raise Exception("Erro: Formato de vardec incorreto")
            Analisador.tokens.selecionarProximo()
        else:
            raise Exception("Erro: Formato de vardec incorreto")
        return resultado

    def analisarTipo():
        if (Analisador.tokens.atual.tipo == INT):
            Analisador.tokens.selecionarProximo()
            resultado = Type(INT)

        elif (Analisador.tokens.atual.tipo == CHAR):
            Analisador.tokens.selecionarProximo()
            resultado = Type(CHAR)

        elif (Analisador.tokens.atual.tipo == VOID):
            Analisador.tokens.selecionarProximo()
            resultado = Type(VOID)
        else:
            raise Exception("Erro: Tipo não reconhecido, só aceita INT,CHAR,VOID")
        return resultado        

    def analisarFuncCall():
        resultado = None
        if (Analisador.tokens.atual.tipo == IDENTIFIER):
            resultado = FuncCall(Analisador.tokens.atual.valor,[])
            Analisador.tokens.selecionarProximo()
            if (Analisador.tokens.atual.tipo == OPEN_PAR):
                Analisador.tokens.selecionarProximo()
                if (Analisador.tokens.atual.tipo == CLOSE_PAR):
                    Analisador.tokens.selecionarProximo()
                else:
                    resultado.children.append(Analisador.analisarExpressao())
                    while(Analisador.tokens.atual.tipo == COMMA):
                        Analisador.tokens.selecionarProximo()
                        resultado.children.append(Analisador.analisarExpressao())
                    if (Analisador.tokens.atual.tipo == CLOSE_PAR):
                        Analisador.tokens.selecionarProximo()
                    else:
                        Exception("Erro: FuncCall Incorreto")        
            else:
                Exception("Erro: FuncCall Incorreto")
        else:
            raise Exception("Erro: FuncCall Incorreto ")
        return resultado

            

#___________________________________________________________________________________________________
def main():
    #try:
    Analisador.inicializar(inputCompiler)
    raiz = Analisador.analisarPrograma()
    raiz.Evaluate(SymbTab)

    #except Exception as erro:
    #    print(erro)

if __name__== "__main__":
    main()
 





