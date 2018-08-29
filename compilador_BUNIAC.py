#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re #importing regular expression
#os três tipos que um token pode ter (constantes)
INT = "INT"
PLUS = "PLUS"
MINUS = "MINUS"
MULT = "MULT"
DIV = "DIV"
EOF = "EOF" #end of file
OPEN_PAR = "OPEN_PAR"
CLOSE_PAR = "CLOSE_PAR"
entrada = (str(input("Conta: ")))#entrada do usuário

#Classe Token

class Token:
    def __init__(self,tipo,valor):
        self.tipo=tipo#tipo (string-tipo do token);
        self.valor=valor#valor (integer-valor do token);

#Classe Tokenizador

class Tokenizador:
    def __init__(self,origem):
        self.origem = origem#origem (string-codigo fonte tokenizado)-> conta matemática(entrada do usuario)
        self.posicao = 0#posição (integer-posição atual que tokenizador irá separar);
        self.atual = Token(EOF,EOF)#atual (token-ultimo token separado);
    #lê o próximo token e atualiza o atributo atual
    def selecionarProximo(self):
        digito =""#Para numeros com mais de 1 digito
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
                # print(self.origem[self.posicao])
                while (self.posicao<(len(self.origem)) and (self.origem[self.posicao]).isdigit()):
                    # print(self.origem[self.posicao])
                    digito +=self.origem[self.posicao]
                    self.posicao+=1

                token = Token(INT,int(digito))
                self.atual=token

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
        #while (Analisador.tokens.atual.tipo != EOF):

            if (Analisador.tokens.atual.tipo == PLUS):
                Analisador.tokens.selecionarProximo()
                resultado+=Analisador.analisarTermo()

            elif (Analisador.tokens.atual.tipo == MINUS):
                Analisador.tokens.selecionarProximo()
                resultado-=Analisador.analisarTermo()
        return resultado

    def analisarTermo():
        resultado = Analisador.analisarFator()

        while (Analisador.tokens.atual.tipo == MULT or Analisador.tokens.atual.tipo == DIV):
            if (Analisador.tokens.atual.tipo == MULT):
                Analisador.tokens.selecionarProximo()
                resultado*=Analisador.analisarFator()

            elif (Analisador.tokens.atual.tipo == DIV):
                Analisador.tokens.selecionarProximo()
                resultado//=Analisador.analisarFator()
        return resultado
    
    def analisarFator():
        resultado = 0
        if Analisador.tokens.atual.tipo == INT:
            resultado = Analisador.tokens.atual.valor
            Analisador.tokens.selecionarProximo()

        elif (Analisador.tokens.atual.tipo == PLUS):#Este plus é unário ( é um sinal de +)
            Analisador.tokens.selecionarProximo()
            resultado=Analisador.analisarFator() # 1* Analisador.analisarFator()
        
        elif (Analisador.tokens.atual.tipo == MINUS):#Este minus é unário ( é um sinal de - ex: -2+1= -1)
            Analisador.tokens.selecionarProximo()
            resultado=-Analisador.analisarFator() # -1 *Analisador.analisarFator()
    
        elif (Analisador.tokens.atual.tipo == OPEN_PAR):
           Analisador.tokens.selecionarProximo()
           resultado = Analisador.analisarExpressao()
           if (Analisador.tokens.atual.tipo == CLOSE_PAR):
               Analisador.tokens.selecionarProximo()
           else:
                raise Exception("Erro: Parentesês não fecha") 
        else:
             raise Exception("Erro: Expressão inválida")
        return resultado


def main():
    try:
        Analisador.inicializar(entrada)
        print("Resultado:",Analisador.analisarExpressao())

    except Exception as erro:
        print(erro)

if __name__== "__main__":
    main()


