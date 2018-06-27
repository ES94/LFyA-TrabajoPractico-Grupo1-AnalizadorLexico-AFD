firsts = []
follows = []
Regla_Temporal = []
Agregar_Follow = False #Banderas que se activan para saber si estoy trabajando con la lista de follows o de firsts.
Agregar_First = False
U = 2 #Ubicacion en regla original. Se usa para moverme a lo largo de esta regla original.
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



def terminal_es_lambda(regla):
    if regla[2] == 'l' and regla[3] == 'a' and regla[4] == 'm' and regla[5] == 'b' and regla[6] == 'd' and regla[7] == 'a':
        return True
    else:
        return False
        

def buscar_terminal(NT,reglaTemp): #Si voy a buscar terminales a traves de otros NT, significa que puedo encontrarme más de un terminal, hago una Lista Aux de firsts.
    for r in reglas:
        Terminal_lambda = False
        if NT == r.regla[0]: #Encontre el NT como antecedente de una regla
            if str.isupper(r.regla[2]):
                buscar_terminal(r.regla[2],reglaTemp)
            else:
                terminal = r.regla[2]
                Terminal_lambda = terminal_es_lambda(r.regla)
                if Terminal_lambda == True: #Si el terminal es lambda
                    global U #Hago uso de la variable GLOBAL U
                    if len(reglaTemp) - 1 > U:       #Si el NT NO es el ultimo de la cadena
                        U = U + 1                      
                        if str.isupper(reglaTemp[U]):                                
                            buscar_terminal(reglaTemp[U],reglaTemp)   #vuelvo a buscar terminales
                        else:
                            terminal = reglaTemp[U]
                            if Agregar_First == True:
                                if terminal not in firsts:
                                    firsts.append(terminal)
                            else:
                                if Agregar_Follow == True:
                                    if terminal not in follows:
                                        follows.append(terminal)
                    else: #Si no hay mas nada, agrego lambda a los firsts (en FIRST) || busco follows del antecedente(en FOLLOW)
                        terminal = 'lambda'
                        if Agregar_First == True:
                            if terminal not in firsts:
                                firsts.append(terminal)
                        else:
                            if Agregar_Follow == True:
                                buscar_follows_antecedente(reglaTemp)
                else: #Si el terminal no es lambda
                    if Agregar_First == True:
                        if terminal not in firsts:
                            firsts.append(terminal)
                    else:
                        if Agregar_Follow == True:
                            if terminal not in follows:
                                follows.append(terminal)

                
def calcular_firsts(indice_regla): #llamar funcion dentro de un ciclo iterando por cada regla de reglas.
    global Agregar_First
    Agregar_First = True
    terminal = ''
    Regla_Temporal = reglas[indice_regla].regla

    if str.isupper(reglas[indice_regla].regla[2]): # Si el primer consecuente es un NT, busco los firsts de sus reglas.
        no_terminal = reglas[indice_regla].regla[2]
        buscar_terminal(no_terminal,Regla_Temporal)
    else: #Sino, significa que ya tenemos el first de la regla.
        terminal = reglas[indice_regla].regla[2]
        Terminal_lambda = terminal_es_lambda(reglas[indice_regla].regla)
        if Terminal_lambda == True: #Si el terminal es lambda
            terminal = 'lambda'
        if terminal not in firsts:
            firsts.append(terminal)

    Agregar_First = False
    return firsts

def buscar_follows_antecedente(reglaTemp):  #Se debe recorrer las listas de follows de cada NT.
    for r in reglas:
        if r.regla == reglaTemp:
            for f in range(0,len(r.follows)):
                if r.follows[f] not in follows:
                    follows.append(r.follows[f])
            break

        
def es_distinguido(NT):
    for r in reglas:
        if r.regla[0] == NT:
            return True
        else:
            return False
        break 
   
def buscar_follows(NT):
    for r in reglas: #Se usa para recorrer todas las reglas
        for n in range(2,len(r.regla)): #Se usa para recorrer cada caracter de cada una de esas reglas
            if NT == r.regla[n]: #Encontre el NT como consecuente en alguna regla
                reglaTemp = r.regla
                if len(reglaTemp) - 1 > n:       #Si el NT NO es el ultimo de la cadena
                    if str.isupper(reglaTemp[n+1]):
                        global U
                        U = n
                        buscar_terminal(reglaTemp[n+1],reglaTemp)   #vuelvo a buscar terminales
                    else:
                        terminal = reglaTemp[n+1]
                        if terminal not in follows:
                            follows.append(terminal)
                else: #Si no hay mas nada, busco los follows del antecedente de esa regla.
                    buscar_follows_antecedente(reglaTemp)    
       
def calcular_follows(no_terminal):
    global Agregar_Follow
    Agregar_Follow = True
    reglaTemp = []
    if es_distinguido(no_terminal) == True:
        follows.append('$')
    terminal = ''
    buscar_follows(no_terminal)

    Agregar_Follow = False
    return follows

def calcular_selects():
    for r in reglas:
        if 'lambda' in r.firsts:
            aux = r.firsts
            aux.remove('lambda')
            r.selects = aux

            for f in r.follows:
                if f not in r.selects:
                    r.selects.append(f)
        else:
            r.selects = r.firsts
        print(r.selects)            
            

def calcular_LL1():
    antecedente = ''
    es_ll1 = True
    lista_selects = []

    for r in reglas:
        if r.regla[0] != antecedente:
            antecedente = r.regla[0]
            lista_selects.clear()
        
        for s in r.selects:
            if s in lista_selects:
                es_ll1 = False

                break
            else:
                lista_selects.append(s)

        if not es_ll1:
            break
    
    return es_ll1

def setear_gramatica(gramatica):
    '''Recibe una gramática, pasada como parámetro, y devuelve los firsts, 
    follows y selects de la gramática, y si ésta es LL1.

    '''

    # {...}

def evaluar_cadena(cadena):
    '''Evalua una cadena, pasada como parámetro, y determina si pertenece o no 
    a una gramática dada.

    '''

    # {...}

    
r1 = Regla('E:[E]', [], [], [])
r2 = Regla('E:nF', [], [], [])
r3 = Regla('F:,n', [], [], [])
r4 = Regla('F:lambda', [], [], [])

#NO OLVIDARSE DE AGREGAR LAS REGLAS QUE SE AGREGAN ARRIBA, ACA ABAJO!!

reglas = [r1, r2, r3, r4]  #La lista reglas tiene 4 posiciones (regla, firsts, follows y select) por cada posicion
print (' ')
print ('-------------- F I R S T S ---------------')
print (' ')
for r in range(0,len(reglas)):
    print(reglas[r].regla,'     ', calcular_firsts(r))
    reglas[r].firsts = firsts
    firsts = []
print (' ')
print ('-------------- F O L L O W S ---------------')
print (' ')
for r in range(0,len(reglas)):
    print(reglas[r].regla,'    ', calcular_follows(reglas[r].regla[0]))
    reglas[r].follows = follows
    follows = []
print (' ')
print ('-------------- S E L E C T ---------------')
print (' ')
calcular_selects()
print (' ')
if calcular_LL1():
    print ('ES LL 1')
else:
    print ('NO ES LL 1')
