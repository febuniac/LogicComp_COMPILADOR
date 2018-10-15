#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re #importing regular expression

#___________________________________________________________________________________________________
#Tipos de Token (constantes)
INT = "INT"
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
#___________________________________________________________________________________________________
#Leitura de Arquivo
#entrada = (str(input("Conta: ")))#entrada do usuário
with open('inputCompiler.txt') as entrada:
  inputCompiler = entrada.read()
  inputCompiler = inputCompiler.replace("\n"," ")
  inputCompiler = inputCompiler.replace("   "," ")
  inputCompiler = inputCompiler.replace(" ","")

#___________________________________________________________________________________________________
class SymbolTable:
    dictionary = {}
    def __init__(self):
        pass
    def get_nome(self,nome):
        return SymbolTable.dictionary[str(nome)]
        #return self.nome
    def set_nome_valor(self,nome,valor):
        SymbolTable.dictionary[str(nome)] = int(valor)
        #self.nome = valor

SymbolTable = SymbolTable()
      
class Node:
    # Constructor to create a new Node
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self):
        pass

class Identifier(Node):#Identificador
    def __init__(self,nome,valor):#
        self.nome = nome
        self.valor = valor #valor do nó
    def Evaluate(self):
        #global SymbolTable
        return SymbolTable.get_nome(self.nome)#get do nome na symbol table



class Assign(Node):#Assign Operation
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self):
        #gravando na symboltable o valor da atribuição
        SymbolTable.set_nome_valor(self.children[0].nome,self.children[1].Evaluate())#valor dó nó é o nome da variavel 


class Comandos(Node):#Comandos Operation
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self):
        print(self.children)
        for child in self.children:
            child.Evaluate()#child percorre a lista de children e vai dando evaluate
        
        
class BinOp(Node):#Binary Operation
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self):
        val_esq=self.children[0].Evaluate()
        val_dir=self.children[1].Evaluate()
        if(self.valor == 'PLUS'):
            return val_esq + val_dir
        elif (self.valor == 'MINUS'):
            return val_esq - val_dir
        elif (self.valor == 'MULT'):
            return val_esq * val_dir
        elif (self.valor == 'DIV'):
            return val_esq // val_dir
        elif self.valor == 'OR':
            return val_esq or val_dir
        elif self.valor == 'AND':
            return val_esq and val_dir
        elif self.valor == 'BIGGER_THAN':
            return val_esq > val_dir
        elif self.valor == 'SMALLER_THAN':
            return val_esq < val_dir    
        elif self.valor == 'EQUAL_TO':
            return val_esq == val_dir      
class Printf(Node):
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self):
        print(self.children.Evaluate())

class UnOp(Node):#Unary Operation
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self):
        val_unico=self.children[0].Evaluate()
        if (self.valor == 'PLUS'):
            return +val_unico
        elif (self.valor == 'MINUS'):
            return -val_unico
        elif self.valor == 'NOT':
            return not val_unico 

class IntVal(Node):#Integer Value
    def __init__(self,valor):
        self.valor = valor
    def Evaluate(self):
        return self.valor

class NoOp(Node):#No Operation
    def Evaluate(self):
        return None

class Scanf(Node):
    def __init__(self,valor):
        self.valor = valor
    def Evaluate(self):
        return (input(""))
class If(Node):
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self):
        val_esq=self.children[0].Evaluate()
        if val_esq == True:
            self.children[1].Evaluate()
        else:
            self.children[2].Evaluate()

class While(Node):
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
    def Evaluate(self):
        while self.children[0].Evaluate()==True:
            self.children[1].Evaluate()

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
    #lê o próximo token e atualiza o atributo atual
    def selecionarProximo(self):
        digito =""#Para numeros com mais de 1 digito
        string=[]#Para palvras com mais de 1 char
        #sempre aqui pois pega um token de cada vez
        while self.posicao < len(self.origem) and (self.origem[self.posicao] == " "):#limpando os espaços
            self.posicao+=1#atualiza a posição
            if re.search('[0-9] +[0-9]', entrada):
                raise Exception("Erro: Digito seguido de digito")
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
                if re.search('[0-9] +[0-9]', entrada):
                    raise Exception("Erro: Digito seguido de digito")
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
            resultado = Identifier(Analisador.tokens.atual.valor, Analisador.tokens.atual.tipo)
            Analisador.tokens.selecionarProximo()
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
                resultado = Assign(op,[resultado, Analisador.analisarExpressao()])
            elif(Analisador.tokens.atual.tipo == SCANF):#=
                
                resultado = Analisador.analisarScanf()
            else:
                raise Exception("Erro: Atribuição inválida (atribuição)")
        return resultado
   
    def analisarComando():
        # resultado=None
        if (Analisador.tokens.atual.tipo == OPEN_KEY):#{
            resultado = Analisador.analisarComandos()
        elif (Analisador.tokens.atual.tipo == IDENTIFIER):#id
            resultado = Analisador.analisarAtribuicao()
        elif (Analisador.tokens.atual.tipo == PRINTF):#id
            resultado = Analisador.analisarPrintf()
        elif (Analisador.tokens.atual.tipo == IF):#id
            resultado = Analisador.analisarIf()
        elif (Analisador.tokens.atual.tipo == WHILE):#id
            resultado = Analisador.analisarWhile()
        return resultado
   
    def analisarComandos():
       # resultado=None
        lista_comandos = []
        if (Analisador.tokens.atual.tipo == OPEN_KEY):#{
            Analisador.tokens.selecionarProximo()
            resultado = Analisador.analisarComando()
            if (Analisador.tokens.atual.tipo == SEMICOLON):#;;
                Analisador.tokens.selecionarProximo()
                lista_comandos.append(resultado)
            else:
                raise Exception("Erro: Comando Incorreto") 

            while (Analisador.tokens.atual.tipo != CLOSE_KEY):
                resultado = Analisador.analisarComando()
                if (resultado == None):
                    break
                lista_comandos.append(resultado)
                if (Analisador.tokens.atual.tipo == SEMICOLON):#;
                    Analisador.tokens.selecionarProximo()
                else:
                    raise Exception("Erro: Formato de comando incorreto")
            Analisador.tokens.selecionarProximo()
            #if (Analisador.tokens.atual.tipo == CLOSE_KEY):#} 
            return Comandos(None,lista_comandos)
        else:
            raise Exception("Erro: Formato de comando incorreto")
        #return resultado

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
                    resultado.append(Analisador.analisarComandos())
                    if (Analisador.tokens.atual.tipo == ELSE):#Else
                        Analisador.tokens.selecionarProximo()
                        resultado.append(Analisador.analisarComandos())
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
                    resultado = While(WHILE,[resultado, Analisador.analisarComandos()])
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
#___________________________________________________________________________________________________
def main():
    #try:
    Analisador.inicializar(inputCompiler)
    raiz = Analisador.analisarComandos()
    raiz.Evaluate()

    #except Exception as erro:
    #    print(erro)

if __name__== "__main__":
    main()


