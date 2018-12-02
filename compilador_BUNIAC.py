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
MAIN = "MAIN"
INT = "INT"
CHAR = "CHAR"
VOID = "VOID"
COMMA="COMMA"
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
class Id:
    constants= [
        "; constants",
        "SYS_EXIT equ 1",
        "SYS_READ equ 3",
        "SYS_WRITE equ 4",
        "STDIN equ 0",
        "STDOUT equ 1",
        "True equ 1",
        "False equ 0",
        "segment .data"
    ]

    variables = [
        "segment .bss ; variaveis"
    ]

    functions = [
        "res RESB 1",
        "section .text",
        "global _start",
        "print :  ; subrotina print",
        "POP EBX",
        "POP EAX",
        "PUSH EBX",
        "XOR ESI, ESI",
        "print_dec :",
        "MOV EDX, 0",
        "MOV EBX, 0x000A",
        "DIV EBX",
        "ADD EDX, '0'",
        "PUSH EDX",
        "INC ESI",
        "CMP EAX, 0",
        "JZ print_next",
        "JMP print_dec",
        "print_next :",
        "CMP ESI, 0",
        "JZ print_exit",
        "DEC ESI",
        "MOV EAX, SYS_WRITE",
        "MOV EBX, STDOUT",
        "POP ECX",
        "MOV [res], ECX",
        "MOV ECX, res",
        "MOV EDX, 1",
        "INT 0x80",
        "JMP print_next",
        "print_exit :",
        "RET",
        "; subrotinas if/while",
        "binop_je :",
        "JE binop_true",
        "JMP binop_false",
        "binop_jg :",
        "JG binop_true",
        "JMP binop_false",
        "binop_jl :",
        "JL binop_true",
        "JMP binop_false",
        "binop_false :",
        "MOV EBX, False",
        "JMP binop_exit",
        "binop_true :",
        "MOV EBX, True",
        "binop_exit :",
        "RET"
    ]

    commands=[
        "_start :",
        "; codigo gerado pelo compilador"
    ]

    end = [
        "; interrupcao de saida",
        "MOV EAX, 1",
        "INT 0x80"
    ]
    
    identificador = 0
    @staticmethod
    def get_new_ID():
        coloca = Id.identificador
        Id.identificador +=1
        return coloca
    @staticmethod
    def writecodeAssembly():
        with open("programa_codigo.asm", "w") as arqassemb:
            for lista in [Id.constants, Id.variables, Id.functions, Id.commands, Id.end]:
                for line in lista:
                    arqassemb.write(line + '\n')
                   
class SymbolTable:
    dictionary = {}
    def __init__(self):
        pass
    def get_nome(self,nome):
        return SymbolTable.dictionary[str(nome)]
        #return self.nome
    def set_nome_valor_tipo(self,nome,valor,tipo):
        SymbolTable.dictionary[str(nome)] = [int(valor),str(tipo)]
        #self.nome = valor

SymbolTable_n = SymbolTable()
      
class Node:
    # Constructor to create a new Node
    def __init__(self,valor,children):
        self.valor = valor
        self.children = children
        self.identificador = Id.get_new_ID()
    def Evaluate(self):
        pass

class Identifier(Node):#Identificador
    def __init__(self,nome,valor):#
        self.identificador = Id.get_new_ID()
        self.nome = nome
        self.valor = valor #valor do nó
    def Evaluate(self):
        #global SymbolTable
        r = "MOV EBX, [{0}_1]".format(self.nome)
        return [r]
        #return SymbolTable.get_nome(self.nome)#get do nome na symbol table

# if self.value == ASSIGNMENT:
#             res = self.children[1].Evaluate(SymbolTable)
#             assignment = "MOV [{0}_1], EBX".format(self.children[0].name)
#             res.append(assignment)

class Assign(Node):#Assign Operation
    def __init__(self,valor,children):
        self.identificador = Id.get_new_ID()
        self.valor = valor
        self.children = children
    def Evaluate(self):
        #gravando na symboltable o valor da atribuição
        coloca = self.children[1].Evaluate()
        assign = "MOV [{0}_1], EBX".format(self.children[0].nome)
        coloca.append(assign)
        # valor = self.children[1].Evaluate()
        # SymbolTable_n.set_nome_valor_tipo(self.children[0].nome, valor[0], valor[1])#valor dó nó é o nome da variavel 
        return coloca

class Comandos(Node):#comandos Operation
    def __init__(self,valor,children):
        self.identificador = Id.get_new_ID()
        self.valor = valor
        self.children = children
    def Evaluate(self):
        for child in self.children:
            coloca = child.Evaluate() #child percorre a lista de children e vai dando evaluate
            if type(child) is VarDec:
                for line in coloca or []:
                    Id.variables.append(line)  
            else:  
                for line in coloca or []:
                    Id.commands.append(line)

    def EvaluateBlock(self):
        r = []
        for child in self.children:
            coloca = child.Evaluate() #child percorre a lista de children e vai dando evaluate
            for line in coloca or []:
                r.append(line)
        return r
        
class BinOp(Node):#Binary Operation
    def __init__(self,valor,children):
        self.identificador = Id.get_new_ID()
        self.valor = valor
        self.children = children
    def Evaluate(self):
        coloca=self.children[0].Evaluate()
        coloca.append("PUSH EBX")
        val_dir=self.children[1].Evaluate()
        coloca += val_dir
        coloca.append("POP EAX")
        if(self.valor == 'PLUS'):
            coloca.append("ADD EAX, EBX")
            coloca.append("MOV EBX, EAX")
            # if val_esq[1] == val_dir[1] and val_esq[1] == INT:
            #     return [val_esq[0] + val_dir[0], INT]
            # else:
            #     raise Exception("Erro: tipos incompatíveis int PLUS")
        elif (self.valor == 'MINUS'):
            coloca.append("SUB EAX, EBX")
            coloca.append("MOV EBX, EAX")
            # if val_esq[1] == val_dir[1] and val_esq[1] == INT:
            #     return [val_esq[0] - val_dir[0], INT]
            # else:
            #     raise Exception("Erro: tipos incompatíveis int MINUS")
        elif (self.valor == 'MULT'):
            coloca.append("IMUL EBX")
            coloca.append("MOV EBX, EAX")
            # if val_esq[1] == val_dir[1] and val_esq[1] == INT:
            #     return [val_esq[0] * val_dir[0], INT]
            # else:
            #     raise Exception("Erro: tipos incompatíveis int MULT")
        elif (self.valor == 'DIV'):
            coloca.append("IDIV EAX, EBX")
            coloca.append("MOV EBX, EAX")

            # if val_esq[1] == val_dir[1] and val_esq[1] == INT:
            #     return [val_esq[0] // val_dir[0], INT]
            # else:
            #     raise Exception("Erro: tipos incompatíveis int DIV")
        elif self.valor == 'OR':
            coloca.append("OR EAX, EBX")
            coloca.append("MOV EBX, EAX")
            # if val_esq[1] == val_dir[1] and val_esq[1] == CHAR:
            #     return [val_esq[0] or val_dir[0], CHAR]
            # else:
            #     raise Exception("Erro: tipos incompatíveis char OR")
        elif self.valor == 'AND':
                coloca.append("AND EAX, EBX")
                coloca.append("MOV EBX, EAX")
            # if val_esq[1] == val_dir[1] and val_esq[1] == CHAR:
            #     return [val_esq[0] and val_dir[0], CHAR]
            # else:
            #     raise Exception("Erro: tipos incompatíveis char AND")    
        elif self.valor == 'BIGGER_THAN':
            coloca.append("CMP EAX, EBX")
            coloca.append("CALL binop_jg")
            # if val_esq[1] == val_dir[1] and val_esq[1] == INT:
            #     return [val_esq[0] > val_dir[0], CHAR]
            # else:
            #     raise Exception("Erro: tipos incompatíveis char BIGGER_THAN")
        elif self.valor == 'SMALLER_THAN':
            coloca.append("CMP EAX, EBX")
            coloca.append("CALL binop_jl")
            # if val_esq[1] == val_dir[1] and val_esq[1] == INT:
            #     return [val_esq[0] < val_dir[0], CHAR]
            # else:
            #     raise Exception("Erro: tipos incompatíveis char SMALLER_THAN")               
        elif self.valor == 'EQUAL_TO':
            coloca.append("CMP EAX, EBX")
            coloca.append("CALL binop_je")
            # if val_esq[1] == val_dir[1] and val_esq[1] == INT:
            #     return [val_esq[0] == val_dir[0], CHAR]
            # else:
            #     raise Exception("Erro: tipos incompatíveis char EQUAL_TO") 
        return coloca              
class Printf(Node):
    def __init__(self,valor,children):
        self.identificador = Id.get_new_ID()
        self.valor = valor
        self.children = children
    def Evaluate(self):
        coloca = self.children.Evaluate()
        coloca.append("PUSH EBX")
        coloca.append("CALL print")
        return coloca
        #print(self.children.Evaluate()[0])

class UnOp(Node):#Unary Operation
    def __init__(self,valor,children):
        self.identificador = Id.get_new_ID()
        self.valor = valor
        self.children = children
    def Evaluate(self):
        val_unico=self.children[0].Evaluate()
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
        self.identificador = Id.get_new_ID()
        self.valor = valor
    def Evaluate(self):
        r = "MOV EBX, {0}".format(self.valor)
        return [r]
        # return [self.valor, INT]

class NoOp(Node):#No Operation
    def Evaluate(self):
        return None

class Scanf(Node):
    def __init__(self,valor):
        self.identificador = Id.get_new_ID()
        self.valor = valor
    def Evaluate(self):
        return [input(""), INT]

class If(Node):
    def __init__(self,valor,children):
        self.identificador = Id.get_new_ID()
        self.valor = valor
        self.children = children
    def Evaluate(self):
        # val_esq=self.children[0].Evaluate()[0]
        # if val_esq == True:
        #     self.children[1].Evaluate()
        # else:
        #     self.children[2].Evaluate()
        coloca = ["IF_{0}".format(self.identificador)]
        coloca += self.children[0].Evaluate()
        coloca.append("CMP EBX, False")
        coloca.append("JE ELSE_{0}".format(self.identificador))
        coloca += self.children[1].EvaluateBlock()
        coloca.append("JMP EXIT_{0}".format(self.identificador))
        coloca = ["ELSE_{0}".format(self.identificador)]
        coloca += self.children[2].EvaluateBlock()
        coloca.append("EXIT_{0}".format(self.identificador))
        return coloca

class While(Node):
    def __init__(self,valor,children):
        self.identificador = Id.get_new_ID()
        self.valor = valor
        self.children = children
    def Evaluate(self):
        # while self.children[0].Evaluate()[0]==True:
        #     self.children[1].Evaluate()
        coloca = ["LOOP_{0}:".format(self.identificador)]
        coloca += self.children[0].Evaluate()
        coloca.append("CMP EBX, False")
        coloca.append("JE EXIT_{0}".format(self.identificador))
        coloca += self.children[1].EvaluateBlock()
        coloca.append("JMP LOOP_{0}".format(self.identificador))
        coloca.append("EXIT_{0}:".format(self.identificador) )
        return coloca

class Type(Node):#Type Def
    def __init__(self,valor):
        self.identificador = Id.get_new_ID()
        self.valor = valor
        self.children = None
    def Evaluate(self):
        if (self.valor == 'INT'):
            return [0, INT]#0 é valor default de int
        elif (self.valor == 'CHAR'):
            return [0, CHAR]
        elif self.valor == 'VOID':
            return [None, VOID]#MNone é valor default de char

class VarDec(Node):#Variable Declaration
    def __init__(self,valor,children):
        self.identificador = Id.get_new_ID()
        self.valor = valor
        self.children = children
    def Evaluate(self):
        tipo=self.children[0].Evaluate()
        for child in self.children:
            r = ["{0}_1 RESD 1".format(self.children[1].nome)]
        return r
        # tipo=self.children[0].Evaluate()
        # for child in self.children:
        #     SymbolTable_n.set_nome_valor_tipo(self.children[0].valor, tipo[0], tipo[1])#tipo [0] é o valor default e e tipo[1] é o tipo (ex: no nó Type return [0, CHAR])
        
#___________________________________________________________________________________________________
#Class Token
class Token:
    def __init__(self,tipo,valor):
        self.identificador = Id.get_new_ID()
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
                elif(fullString == "main"):    
                    token = Token('MAIN', fullString)
                elif(fullString == "int"):    
                    token = Token('INT', fullString)
                elif(fullString == "char"):    
                    token = Token('CHAR', fullString) 
                elif(fullString == "void"):    
                    token = Token('VOID', fullString)   
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
        # resultado=None
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
        return resultado
   
    # def analisarComandos():
    #    # resultado=None
    #     lista_comandos = []
    #     if (Analisador.tokens.atual.tipo == OPEN_KEY):#{
    #         Analisador.tokens.selecionarProximo()
    #         resultado = Analisador.analisarComando()
    #         if (Analisador.tokens.atual.tipo == SEMICOLON):#;;
    #             Analisador.tokens.selecionarProximo()
    #             lista_comandos.append(resultado)
    #         else:
    #             raise Exception("Erro: Comando Incorreto") 

    #         while (Analisador.tokens.atual.tipo != CLOSE_KEY):
    #             resultado = Analisador.analisarComando()
    #             if (resultado == None):
    #                 break
    #             lista_comandos.append(resultado)
    #             if (Analisador.tokens.atual.tipo == SEMICOLON):#;
    #                 Analisador.tokens.selecionarProximo()
    #             else:
    #                 raise Exception("Erro: Formato de comando incorreto")
    #         Analisador.tokens.selecionarProximo()
    #         #if (Analisador.tokens.atual.tipo == CLOSE_KEY):#} 
    #         return Comandos(None,lista_comandos)
    #     else:
    #         raise Exception("Erro: Formato de comando incorreto")
    #     #return resultado

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
        resultado = Analisador.analisarTipo()
        if (Analisador.tokens.atual.tipo == MAIN):#MAIN
            Analisador.tokens.selecionarProximo()
            if (Analisador.tokens.atual.tipo == OPEN_PAR):
                Analisador.tokens.selecionarProximo()
                if (Analisador.tokens.atual.tipo == CLOSE_PAR):
                        Analisador.tokens.selecionarProximo()
                        resultado = Analisador.analisarBloco() #Quando arrumar o ponto e virgula do comando, habilitar essa linha e remove a de baixo
                        #resultado = Analisador.analisarComandos()

                else:
                    raise Exception("Erro: Parentesês não fecha na main")
            else:
                raise Exception("formato da main incorreto")
        else:
            raise Exception("Erro: Expressão inválida (main) ")
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
            resultado = VarDec(None,[resultado, Identifier(Analisador.tokens.atual.valor,IDENTIFIER)])
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
            raise Exception("Erro: Tipo não reconheciddo, só aceita INT,CHAR,VOID")
        return resultado        
#___________________________________________________________________________________________________
def main():
    try:
        Analisador.inicializar(inputCompiler)
        raiz = Analisador.analisarPrograma()
        raiz.Evaluate()
        Id.writecodeAssembly()

    except Exception as erro:
       print(erro)

if __name__== "__main__":
    main()


