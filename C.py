import re
import string
import graphviz
tokens_d = {
    'WHITESPACE': r'\s+',
    'ID': r'[A-Za-z][A-Za-z0-9]*',
    'NUMBER': r'\d+(\.\d+)?([Ee][+-]?\d+)?',
    'PLUS': r'\+',
    'MINUS': r'-',
    'TIMES': r'\*',
    'DIV': r'/',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'ASSIGNOP': r':=',
    'EQUALS': r'=',
    'SEMICOLON': r';',
    'LT': r'<',
    'GT': r'>',
}

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def build_syntax_tree(postfix_expression):
    stack = []

    for char in postfix_expression:
        if char == '|':
            right_node = stack.pop()
            left_node = stack.pop()

            or_node = Node(char)
            or_node.left = left_node
            or_node.right = right_node

            stack.append(or_node)
        else:
            node = Node(char)
            stack.append(node)

    return stack[0]

def generate_graphviz_dot(node, dot):
    if node is None:
        return

    if node.left is None and node.right is None:
        dot.node(str(id(node)), label=node.value)
    else:
        dot.node(str(id(node)), label=node.value)
        generate_graphviz_dot(node.left, dot)
        generate_graphviz_dot(node.right, dot)
        dot.edge(str(id(node)), str(id(node.left)))
        dot.edge(str(id(node)), str(id(node.right)))

def print_syntax_tree(node):
    dot = graphviz.Digraph()
    generate_graphviz_dot(node, dot)
    dot.format = 'png'
    dot.render('arbol', view=True)

def merge_tokens(tokens, additional_tokens):
    """
    Función que combina dos diccionarios de tokens y elimina los tokens repetidos según su token_rule y token_name.

    Args:
        tokens (dict): Diccionario original de tokens.
        additional_tokens (dict): Diccionario de tokens adicionales a agregar.

    Returns:
        dict: Diccionario combinado de tokens sin tokens repetidos según su token_rule y token_name.
    """
    merged_tokens = tokens.copy()
    for token_name, token_rule in additional_tokens.items():
        if token_name not in merged_tokens.keys() and token_rule not in merged_tokens.values():
            merged_tokens[token_name] = token_rule
    return merged_tokens

def filter_tokens(tokens, tokens_d):
    """
    Función que filtra los tokens de un diccionario de tokens generados por la función
    extract_tokens_from_yalex_file, 
    Args:
        tokens (dict): Diccionario con los tokens y sus reglas.
        tokens_d (dict): Diccionario con los nombres de los tokens permitidos y sus reglas.
    Returns:
        dict: Diccionario con los tokens procesados.
    """
    filtered_tokens = {}
    for token_name, token_rule in tokens.items():
        if token_name == "id" and "ID" in tokens_d:
            filtered_tokens["ID"] = tokens_d["ID"]
        elif token_name == "number" and "NUMBER" in tokens_d:
            filtered_tokens["NUMBER"] = tokens_d["NUMBER"]
        elif token_name == "ws":
            filtered_tokens["WHITESPACE"] = tokens_d["WHITESPACE"]
        elif token_name in tokens_d and token_rule == tokens_d[token_name]:
            filtered_tokens[token_name] = token_rule
    return filtered_tokens


def extract_tokens_from_yalex_file(file_path, tokens_d):
    """
    Función que extrae los tokens de una gramática en formato yalex desde un archivo
    Args:
        file_path (str): Ruta del archivo yalex.
        tokens_d (dict): Diccionario con los tokens y sus reglas a reemplazar.
    Returns:
        dict: Diccionario con los tokens y sus reglas.
    """
    tokens = {}

    with open(file_path, 'r') as file:
        contenido = file.read()

    contenido_sin_comentarios = re.sub(r'\(\*.*?\*\)', '', contenido, flags=re.DOTALL)

    with open(file_path, 'w') as file:
        file.write(contenido_sin_comentarios)

    with open(file_path, 'r') as file:
        yalex_text = file.read()

    tokens_def = re.findall(r"let\s+(\w+)\s+=\s+(.+)", yalex_text)

    for token_name, token_rule in tokens_def:
        if "return" in token_rule:
            token_rule = token_rule.replace("'", "").replace("return", "").strip()
            if token_rule in tokens_d:
                tokens[token_name] = tokens_d[token_rule]
                tokens[token_rule] = tokens_d[token_rule] 
            else:
                if token_name in tokens_d:
                    tokens[token_name] = tokens_d[token_name]
                else:
                    tokens[token_name] = token_rule
        else:
            token_rule = token_rule.replace("'", "")
            if token_rule in tokens_d:
                tokens[token_name] = tokens_d[token_rule]
                tokens[token_rule] = tokens_d[token_rule]
            else:
                if token_name in tokens_d:
                    tokens[token_name] = tokens_d[token_name]
                else:
                    tokens[token_name] = token_rule

    rules = re.findall(r"rule\s+tokens\s+=\s+([\s\S]+?)(?=\nrule|\Z)", yalex_text)

    for rule in rules:
        rule_lines = rule.split("\n")
        for line in rule_lines:
            line = line.strip()
            if line:
                tokens_and_rules = line.split("{")
                token_names = tokens_and_rules[0].split("|")
                for token_name in token_names:
                    token_name = token_name.strip()
                    if token_name and token_name not in tokens.keys():
                        if len(tokens_and_rules) > 1:
                            token_rule = tokens_and_rules[1].split("}")[0].strip()
                            if "return" in token_rule:
                                token_rule = token_rule.replace("'", "").replace("return", "").strip()
                                if token_rule in tokens_d:
                                    tokens[token_name] = tokens_d[token_rule]
                                    tokens[token_rule] = tokens_d[token_rule] 
                                else:
                                    if token_name in tokens_d:
                                        tokens[token_name] = tokens_d[token_name]
                                    else:
                                        tokens[token_name] = token_rule
                            else:
                                if token_rule in tokens_d:
                                    tokens[token_name] = tokens_d[token_rule]
                                    tokens[token_rule] = tokens_d[token_rule] 

    return tokens

def get_accepted_characters(pattern):
    accepted_chars = set()
    for char_code in range(128):  # Se asume ASCII de 128 caracteres
        char = chr(char_code)
        if re.fullmatch(pattern, char):
            accepted_chars.add(char)
    return sorted(list(accepted_chars))

file_path = input('Ingrese la ruta del archivo de entrada: ')
print()
tokens = extract_tokens_from_yalex_file(file_path, tokens_d)
tokens = filter_tokens(tokens, tokens_d)

# Imprimir los tokens y sus reglas
print("Se identificaron estos tokens en el YALEX:")
for token_name, token_rule in tokens.items():
    print("Token: %s " % (token_name))

print("\nTokens con sus valores aceptados:")
accepted_characters_list = []
accepted_characters_dict = {}
for token_name, pattern in tokens.items():
    if token_name == 'ID':
        accepted_characters = get_accepted_characters(''.join([c + '|' for c in string.ascii_letters + string.digits])[:-1])
    else:
        accepted_characters = get_accepted_characters(pattern)
    accepted_characters_list.append(accepted_characters)
    accepted_characters_dict[token_name] = accepted_characters
    print(f'{token_name}: {accepted_characters}')

regex_parts = []
for token_name, pattern in tokens.items():
    regex_parts.append(pattern)

print("\nEsta es la expresion regular sin sustituir valores:")
regex = '|'.join(regex_parts)
print(regex)

print("\nTokens con sus expresiones regulares:")
for token, characters in accepted_characters_dict.items():
    regex = '|'.join(characters)
    print(f"{token}: [{regex}]")

print("\nExpresion regular final:")
# Generar la expresión regular
regex = "+".join("({})".format("|".join(map(re.escape, value))) for key, value in accepted_characters_dict.items() if key != 'WHITESPACE')

# Imprimir la expresión regular generada
print(regex)

