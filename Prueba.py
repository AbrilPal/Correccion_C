from Arbol import *
from graphviz import Digraph

def shunting_yard(user_input):
    precedence_table= {'|':1,'•':2,'*':3,'+':3,'?':3,'(':-1,')':-1}
    operators = ['|','*','+','?','•']
    output = []
    operator_stack = []
    for token in user_input:
        if token in operators:
            while (len(operator_stack)>0 and precedence_table[token] <= precedence_table[operator_stack[-1]]):
                output.append(operator_stack.pop())
            operator_stack.append(token)
        else:
            if token != '(' and token != ')':
                output.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while (len(operator_stack)>0 and operator_stack[-1] != '('):
                    output.append(operator_stack.pop())
                operator_stack.pop()
    while (len(operator_stack)>0):
        output.append(operator_stack.pop())
    return output

def format_input(user_input):
    symbols = ['|','*','+','?']
    result = []
    for i in range(len(user_input)):
        if (i != 0):
            #fist case we check if the previous character is a token and current character is a opening parenthesis
            if (user_input[i-1] not in symbols and user_input[i-1] != '('  and user_input[i] == '('):
                result.append('•')
                result.append(user_input[i])
            #second case we check if the previous character is a * or + or ? and current character is a token
            elif (user_input[i-1] in symbols[1:] and user_input[i] not in symbols and user_input[i] != ')'):
                result.append('•')
                result.append(user_input[i])
            #third case we check if the previous character is a closing parenthesis and current character is a token
            elif (user_input[i-1] == ')' and user_input[i] not in symbols and user_input[i] != '(' and user_input[i] != ')'):
                result.append('•')
                result.append(user_input[i])
            #last check if previous character is not a symbol and not a parenthesis and current character is not a symbol and not a parenthesi
            elif (user_input[i-1] not in symbols and user_input[i-1] != '(' and user_input[i-1] != ')' and user_input[i] not in symbols and user_input[i] != '(' and user_input[i] != ')'):
                result.append('•')
                result.append(user_input[i])
            else:
                result.append(user_input[i])
        else:
            result.append(user_input[i])
    return result

expresion_postfix = r"(0|1|2|3|4|5|6|7|8|9|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(\+)|(\*)|(\()|(\))"
user_input = format_input(expresion_postfix)
output = shunting_yard(user_input)
print('Postfix: ',output)

tree = build_tree(output)
digraph = Digraph(graph_attr={'dpi': str(200)})
postorder_traversal_draw(tree, digraph)
digraph.render('expression_tree', format='png')