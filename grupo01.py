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

reglas = []

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

    firsts = []
    follows =[]
    selects = []

    def __init__(self, regla):
        self.regla = regla

def buscar_terminal(no_terminal, regla_a_excluir):
    for r in reglas:
        if r.regla != reglas[regla_a_excluir].regla:
            if no_terminal == r.regla[0]:
                if str.isupper(r.regla[3]):
                    buscar_terminal(r.regla[3], regla_a_excluir)
                else:
                    return r.regla[3]

def calcular_firsts(indice_regla):
    firsts = []
    terminal = ''

    if str.isupper(reglas[indice_regla].regla[3]):
        for r in reglas:
            if r.regla[0] == reglas[indice_regla].regla[3]:
                terminal = buscar_terminal(reglas[indice_regla].regla[3], 
                reglas.index(reglas[indice_regla]))

        if terminal not in firsts:
            firsts.append(terminal)

    else:
        terminal = reglas[indice_regla].regla[3]
            
        if terminal not in firsts:
            firsts.append(terminal)

    return firsts

def calcular_follows():
    follows = []

    for r in reglas:
        antecedente = r.regla[0]
        
        for re in reglas:
            s = re.regla[3:len(re.regla)]

            if antecedente in s:
                pass

            for i in range(3, len(r.regla - 1)):
                pass

    return follows

def setear_gramatica(reglas):
    '''Recibe una gramática, pasada como parámetro, y devuelve los firsts, 
    follows y selects de la gramática, y si ésta es LL1.

    '''
    
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
            l = tabla[(s, look)]    # Se copia el resto de la entrada en lista.
            l = l[::-1]             # Se invierte la lista con la copia.
            pila.extend(l)          # Se añade la lista invertida a la pila.
        elif s == look:             # Si es un terminal y es igual al look:
            look = lexer.token()    # Se hace un lookahead.
        else:                       # Sino:
            print('Error')          # Imprime error.
    
    if look == '$':                 # Si al final el lookahead devuelve un '$':
        print('True')               # Imprime 'True'. La cadena es válida.
    else:                           # Sino:
        print('False')              # Imprime 'False'. La cadena no es válida.

def cargar_reglas():
    '''Carga las reglas que el usuario define.

    '''

    r = Regla(input('\nIngrese una regla: '))
    reglas.append(r)
    opcion = input('¿Desea ingresar otra regla? (s/n): ')

    while opcion == 's':
        r = Regla(input('\nIngrese una regla: '))
        reglas.append(r)
        opcion = input('¿Desea ingresar otra regla? (s/n): ')

def ver_reglas():
    '''Muestra las reglas cargadas hasta el momento.

    '''

    print('\nReglas:\n')
    resultado = ''

    if len(reglas) == 0:
        resultado = 'No hay reglas cargadas.'
    else:
        for r in reglas:
            resultado += r.regla + '\n'
    
    print(resultado + '\n')

def borrar_reglas():
    '''Borra las reglas almacenadas, si las hay.

    '''

    if len(reglas) == 0:
        input('\nNo hay registros cargados. Pulse cualquier tecla.\n\n')
    else:
        opcion = input('\n¿Desea borrar las reglas? (s/n): ')

        if opcion == 's':
            reglas.clear()
            print('Reglas borradas.')
    
    print('\n')

def aplicacion():
    '''Inicia la aplicación.

    '''

    opcion = ''

    while opcion != '5':
        opcion = input('+' + ('-' * 26) + '+\n' +
        '+ {0:25s}+\n'.format('Elija una opción:') +
        '+ {0:25s}+\n'.format('1 - Cargar reglas') +
        '+ {0:25s}+\n'.format('2 - Ver reglas') +
        '+ {0:25s}+\n'.format('3 - Borrar reglas') +
        '+ {0:25s}+\n'.format('4 - Analizar gramática') +
        '+ {0:25s}+\n'.format('5 - Salir') +
        '+' + ('-' * 26) + '+\n\n' +
        '>>>')

        if opcion == '1':
            cargar_reglas()
        elif opcion == '2':
            ver_reglas()
        elif opcion == '3':
            borrar_reglas()
        elif opcion == '4':
            pass # Analizar gramática.
        elif opcion == '5':
            pass
        else:
            print('\nError: elija una opción dentro del rango permitido.\n\n')

aplicacion()