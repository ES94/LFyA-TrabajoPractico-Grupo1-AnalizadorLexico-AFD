# -*- coding: utf-8 -*-

from ply import lex, yacc

""" Se utiliza la siguiente notación:
- UpperCamelCase para nombres de Clases.
- snake_case en minúsculas para nombres de funciones y variables.
- SNAKE_CASE en mayúsculas para nombres de constantes.
- Nombrar a las clases con nombres propios, y a las funciones con verbos de las
acciones que realizan.
- Cada línea de código no debe superar las 80 columnas de ancho. Debe
realizarse un salto de línea. """

def setear_gramatica(cadena):
    pass

def evaluar_cadena(cadena):
    stack = []
    look = yylex()

    while stack:
        s = stack.pop()
        
        if s in NT:
            l = table[(s, look)]
            l = l[::-1]
            stack.extend(l)
        elif s == look:
            look = yylex()
        else:
            print('Error')
    
    if look == '$':
        print(OK)
    else:
        print('Error')