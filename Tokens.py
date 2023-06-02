import re

tokens = {
    'WHITESPACE': '\s+',
    'ID': '[A-Za-z][A-Za-z0-9]*',
    'PLUS': '\+',
    'TIMES': '\*',
    'LPAREN': '\(',
    'RPAREN': '\)',
}

def get_tokens():
    return tokens

