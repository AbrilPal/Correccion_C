import graphviz

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def construir_arbol(postfix):
    stack = []
    escape = False
    for c in postfix:
        if escape:
            node = Node(c)
            stack.append(node)
            escape = False
        elif c == '\\':
            escape = True
        elif c == '|' or c == '.' or c == '*' or c == '+':
            right_child = stack.pop()
            left_child = stack.pop()
            node = Node(c, left_child, right_child)
            stack.append(node)
        else:
            node = Node(c)
            stack.append(node)
    return stack[0]

def imprimir_arbol(nodo, nombre_archivo):
    dot = graphviz.Digraph(comment='Árbol sintáctico')
    _agregar_nodo(dot, nodo)
    dot.render(nombre_archivo, view=True)

def _agregar_nodo(dot, nodo):
    if nodo is None:
        return
    _agregar_nodo(dot, nodo.left)
    _agregar_nodo(dot, nodo.right)
    dot.node(str(nodo), str(nodo.value))
    if nodo.left is not None:
        dot.edge(str(nodo), str(nodo.left))
    if nodo.right is not None:
        dot.edge(str(nodo), str(nodo.right))

# Expresión regular en notación posfija generada
expresion_postfix = r"(0|1|2|3|4|5|6|7|8|9|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)+(\+)+(\*)+(\()+(\))"

# Construir el árbol sintáctico
arbol = construir_arbol(expresion_postfix)

# Imprimir el árbol en formato gráfico
imprimir_arbol(arbol, 'arbol_sintactico')
