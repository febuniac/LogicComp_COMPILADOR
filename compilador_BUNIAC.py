#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Analisa a string de Input do usuário e joga em uma lista o que são digitos e o que são operadores
def analise(math_op,lista_num,lista_ops):
    digoff ="" #inicializando o digoff como uma string vazia
    # Loop over string.
    for i in math_op:
        if i.isdigit():
            digoff+=i #salvando digito em uma variavel para o caso de numeros com 1+ digitos
            #print("nums",lista_num)
        elif i == "+" or i == "-":
            lista_ops.append(i)
            x = int(digoff) #conversão da string do digito para um int
            lista_num.append(x)
            digoff=""#limapndo o digoff para estar limpo quando for add um novo num
            #print("ops",lista_ops)
        elif i == " ":
            continue
        else:
            print("Isto não faz parte da Matemática")
            break
    x = int(digoff) #conversão da string do digito para um int
    lista_num.append(x)#colocando o ultimo dig da oeperacao na lista como um numero

#Pega os digitos em ordem, checa a operação e faz a operação matemática
def operations(num1,num2,operador):# fazer recursivo 1+1 resultado  depoius resultado +1
    if operador ==  "+" :
        resultado = num1 + num2
    elif operador ==  "-" :
        resultado = num1 - num2
    return resultado
#resultado operacao num 3

math_op = (str(input("Enter a math operation:")))#Entrada do usuário
lista_num=[] #lista de digitos
lista_ops=[] #lista de operadores
analise(math_op,lista_num,lista_ops)
while len(lista_num)>1:#o ultimo valor empilhado é o resultado final
    num1 = lista_num.pop(0)#primeiro digito da operação
    print("primeiro", num1)
    num2 = lista_num.pop(0)#segundo digito da operação
    print("segundo", num2)
    operador = lista_ops.pop(0) #operador da operação
    res = operations(num1,num2,operador)
    lista_num.insert(0,res)#insere o resultado na posic'ão da lista (posição 0 = topo
print("Resultado=", lista_num[0])#printa o resukltado apenas no final
