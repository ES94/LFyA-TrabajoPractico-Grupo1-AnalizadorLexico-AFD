# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# Se utiliza la siguiente notación:
# - UpperCamelCase para nombres de Clases.
# - snake_case en minúsculas para nombres de funciones y variables.
# - SNAKE_CASE en mayúsculas para nombres de constantes.
# - Nombrar a las clases con nombres propios, y a las funciones con verbos de 
# las acciones que realizan.
# - Cada línea de código no debe superar las 80 columnas de ancho. Debe
# realizarse un salto de línea.
#------------------------------------------------------------------------------

from ply import cpp, ctokens, lex, yacc, ygen

class ResultadoGramatica:
    '''Representa el resultado del análisis de una gramática, junto con las 
    reglas que la definen y los firsts, follows, y selects de cada una de 
    ellas.

    '''

    def __init__(self, reglas, es_ll1):
        self.reglas = reglas
        self.es_ll1 = es_ll1
    
    def __repr__(self):
        salida = (
        ('+' + ('-' * 15)) * 4 + '+\n' +
        '+{0:15s}+{1:15s}+{2:15s}+{3:15s}+\n'.format('Regla', 'Firsts', 
        'Follows', 'Selects') +
        ('+' + ('-' * 15)) * 4 + '+\n')
        
        for r in self.reglas:
            hay_caracteres = True
            salida += '+{0:15s}'.format(r.regla)

            while hay_caracteres:
                hay_caracteres = False
                s = ''

                while r.firsts:
                    if len(s) < 15:
                        s += r.firsts.pop()
                    else:
                        hay_caracteres = True

                salida += '+{0:15s}'.format(s)
                s = ''

                while r.follows:
                    if len(s) < 15:
                        s += r.follows.pop()
                    else:
                        hay_caracteres = True

                salida += '+{0:15s}'.format(s)
                s = ''

                while r.selects:
                    if len(s) < 15:
                        s += r.selects.pop()
                    else:
                        hay_caracteres = True

                salida += '+{0:15s}+\n'.format(s)
                s = ''

                if hay_caracteres:
                    salida += '+{0:15s}'.format(' ')
                else:
                    salida += ('+' + ('-' * 15)) * 4 + '+\n'

        salida += '\nEsta gramática {0}es LL1.'.format(('no ','')[self.es_ll1])

        return salida

class Regla:
    '''Representa una regla, junto con sus firsts, follows y selects.\n
    Atributos:
        regla (string): cadena con la representación de la regla.
        firsts (List<string>): lista de los firsts de la regla.
        follows (List<string>): lista de los follows de la regla.
        selects (List<string>): lista de los selects de la regla.

    '''

    def __init__(self, regla, firsts, follows, selects):
        self.regla = regla
        self.firsts = firsts
        self.follows = follows
        self.selects = selects

def setear_gramatica(cadena):
    '''Recibe una gramática, pasada como parámetro, y devuelve los firsts, 
    follows y selects de la gramática, y si ésta es LL1.

    '''
    
    r1 = Regla('', ['', ''], ['', ''], ['', ''])
    r2 = Regla('', ['', ''], ['', ''], ['', ''])
    r3 = Regla('', ['', ''], ['', ''], ['', ''])
    reglas = [r1, r2, r3]
    resultado = ResultadoGramatica(reglas, True)
    
    # {...}

    return resultado

def evaluar_cadena(cadena):
    '''Evalua una cadena, pasada como parámetro, y determina si pertenece o no 
    a una gramática dada.

    '''

    pila = ['', '']
    lexer = lex.lex()
    lexer.input(cadena)
    look = lexer.token()
    NT = []
    tabla = [[0, 0], 
             [0, 0]]

    #--------------------------------------------------------------------------
    # Cómo hacer lookahead:
    # lexer = lex.lex()             # Se crea el lexer (analizador léxico).
    # lexer.input(cadena)           # Se ingresa la cadena y se la tokeniza.
    # lexer.token()                 # Se realiza un lookahead.
    #--------------------------------------------------------------------------

    while pila:                     # Mientras la pila no esté vacía:
        s = pila.pop()              # Extrae el primer elemento de la pila.
        
        if s in NT:                 # Si el elemento es un no terminal:
            l = tabla[(s, look)]    # Se copia el resto de la cadena en lista.
            l = l[::-1]             # Se invierte la lista con la copia.
            pila.extend(l)          # Se añade la lista invertida a la pila.
        elif s == look:             # Si es un no terminal y es igual al look:
            look = lexer.token()    # Se hace un lookahead.
        else:                       # Sino:
            print('Error')          # Imprime error.
    
    if look == '$':                 # Si al final el lookahead devuelve un '$':
        print('True')               # Imprime 'True'. La cadena es válida.
    else:                           # Sino:
        print('False')              # Imprime 'False'. La cadena no es válida.