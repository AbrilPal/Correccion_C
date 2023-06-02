"""
    Andrea Abril Palencia Gutierrez, 18198
    Diseño de Lenguajes de Programacion
    23 de febrero del 2023

    Convertir de INFIX a POSTFIX: usa como parametro una cadena ya
    formateada y devolver una cadena POSTFIX para luego contruir el
    arbol.
"""

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

def construir_arbol(expresion_postfix):
    stack = []

    for caracter in expresion_postfix:
        if caracter.isalnum():
            nodo = Nodo(caracter)
            stack.append(nodo)
        else:
            nodo = Nodo(caracter)
            nodo.derecha = stack.pop()
            nodo.izquierda = stack.pop()
            stack.append(nodo)

    raiz = stack.pop()
    return raiz

def Formatear(expresion_reg):
    expresion_form = []
    todosOperadores = ['|', '?', '+', '*', '^']
    operadoresBinarios = ['|', '^']
    if len(expresion_reg) > 0:
        i = 0
        while i < len(expresion_reg):
            c1 = expresion_reg[i]
            if (i + 1) < len(expresion_reg):
                c2 = expresion_reg[i + 1]
                expresion_form.append(c1)
                if (c1 != '(') and (c2 != ')') and (c2 not in todosOperadores) and (c1 not in operadoresBinarios) and (c2 != '\\'):
                    expresion_form.append('.')
                elif (c1 == '\\'):
                    expresion_form.append(c2)
                    i += 1
            i += 1
        expresion_form.append(expresion_reg[len(expresion_reg) - 1])
        expresion_form_final = ''.join(expresion_form)
        print("La expresion regular formateada es: ", expresion_form_final, "\n")
        return expresion_form_final
    else:
        print("La Expresion Regular ingresada esta vacia\n")
        return None


class Stack: 
    def __init__(self): 
        self.elements = [] 
    
    def push(self, data): 
        self.elements.append(data) 
        return data 
    
    def pop(self): 
        return self.elements.pop() 
        
    def peek(self): 
        return self.elements[-1] 
        
    def is_empty(self): 
        return len(self.elements) == 0

def getPrecedence(caracter):
    if(caracter == '(' or caracter == ')'):
        return 1
    elif(caracter == '|'):
        return 2
    elif(caracter == '.'):
        return 3
    elif(caracter == '?' or caracter == '*' or caracter == '+'):
        return 4
    elif(caracter == '^'):
        return 5
    else:
        return 6

def Infix_Postfix(expresion_re):
    postfix = []
    stack = []
    expresion_form = Formatear(expresion_re)

    for c in expresion_form:
        if c == '(':
            stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()  # Desapilar el paréntesis de apertura
        else:
            while stack and stack[-1] != '(':
                peekedChar = stack[-1]
                if peekedChar == '\\' and len(stack) >= 2:
                    postfix.append(stack.pop())
                    postfix.append(stack.pop())
                elif getPrecedence(peekedChar) >= getPrecedence(c):
                    postfix.append(stack.pop())
                else:
                    break
            stack.append(c)

    while stack:
        postfix.append(stack.pop())

    postfixFinal = ''.join(postfix)
    print("La expresion POSTFIX es: ", postfixFinal, "\n")
    return postfixFinal


expresion_regular = "(0|1|2|3|4|5|6|7|8|9|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)+(\+)+(\*)+(\()+(\))"
expresion_postfix = Infix_Postfix(expresion_regular)

# Construir el árbol sintáctico
arbol = construir_arbol(expresion_postfix)

def imprimir_postfija(nodo):
    if nodo:
        imprimir_postfija(nodo.izquierda)
        imprimir_postfija(nodo.derecha)
        print(nodo.valor, end=" ")
imprimir_postfija(arbol)