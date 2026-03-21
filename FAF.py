#Ahora el problema es que tengo que hacer que idetnifique un operador or | por ejemplo A -> a|b

terminals = {"id","num","string",":","+","-","*","/","=","==","!=","<",">","(",")"}

def makegramatic():
    rulesQuantity = int(input("¿Cuántas reglas de producción necesita? \n"))
    #Esta es la lista de una sola regla, si esta es S' -> S la lista debería ser ["S'", "->", "S"]
    splitRule = ""

    listOfRules = {}
    #Tengo que utilizar la función match para hacer un switch case
    #Para ello supongo que lo mejor sería ponerlo dentro del for ya que este representa la cantidad de relgas que hay
    #¿O quizás lo mejor sería hacer otro for anidado?
    for i in range(0,rulesQuantity):
        listRule = []
        #Inicializar y reinicializar con cada iteración
        print(f'------------------------------Regla {i}---------------------------------')
        lr = input("¿Cuál es el lado izquierdo de la regla de producción? (Ejemplo: S') \n")
        #Es obligatorio que la regla de producción tenga un produce (->)
        #El lado derecho es lo que puede ser más de uno, ¿pongo otro for?
        rr = input("¿Cuál es o cuáles son sus reglas de la derecha? (Ejemplo S, id:S, EE) \n")
        splitRule = rr.split("|")
        #Tengo que verificar que splitRule sea una lista tal que así ["i","d",":","S","|","b"]

        for rule in splitRule:
            # result = refineList(list(rule))
            tokens = rule.strip().split()
            listRule.append(tokens)
        #singleRule.append(rr) Tal vez poner la lista en como estaba antes me sirve de algo en el futuro
        listOfRules[lr] = listRule
    #Por el momento solo es capaz de imprimir una regla con solo un estado por ejemplo S' -> S
    #Mi plan es hacer una matriz, es decir una lista que tenga posiciones tales como  ["S'","->","s"] dentro de otra lista
    #Dentro de otral lista más grande para poder ciclar en todas las reglas
    return listOfRules

def refineList(listRr):
    aux = ""
    oldIndex = 0
    i = 0
    #Quería usar for con lal ista pero el pop hace que las interaciones tengan problemas
    while i < len(listRr):
        rr = listRr[i]
        #Si la letra que viene NO es mayuscula se continua iterando
        if rr.isupper():
            i += 1
            continue

        isterminal = verifyTerminal(rr)

        #Si verifyTerminal encontró una terminal entonces se puede seguir a la siguiente palabra
        if isterminal:
            i += 1
            continue
        #Si llegó hasta aquí fue porque tuvo que haber encontrado alguna letra minuscula
        aux += rr
        oldIndex = i

        #Se elimina la letra en la posición en la que estaba eso significa que si tenemos ["i","d"] se eliminaría ambos
        #Sin embargo al final de todo esto se concatenan las letras y se verifican lo que hace que tengamos ["id"]
        listRr.pop(i)
        isterminal = verifyTerminal(aux)

        #Si la palabra formada es terminal se debe poner como reemplazo
        if isterminal:
            listRr.insert(oldIndex, aux)
            aux = ""
            i += 1 
    return listRr

def first(key, rProductions, firstResults):
    #Me gustaría un if que devuelva si ya se calculo, para optimizar jeje
    if key in firstResults:
        return firstResults[key]
    #No sé muy bien qué estoy haciendo
    firsts = set()
    #Si es un terminal
    if key not in rProductions:
        print("Entró " + key)
        return {key}
    
    #Si es un no terminal
    for produccion in rProductions[key]:
        if produccion[0] == 'ε':
            firsts.add('ε')
        else:
            for char in produccion:
                #Esta función recursiva es el similar a haber dicho S -> A A -> a, es decir que va a buscar alguna terminal
                #De forma recursiva
                resultsChar = first(char, rProductions, firstResults)
                if 'ε' in resultsChar:
                    #Si tiene epsilon, agregamos todo lo demás y seguimos al siguiente token
                    firsts.update(resultsChar - {'ε'})
                    #Si es el último token y todos tuvieron epsilon, agregamos epsilon al padre
                    if char == produccion[-1]:
                        firsts.add('ε')
                else:
                    #Si no tiene epsilon, agregamos y rompemos el flujo de esta producción
                    firsts.update(resultsChar)
                    break
    
    firstResults[key] = firsts
    return firsts

def follow(rProductions, firstResults):
    # 1. Inicializamos el diccionario de FOLLOW con sets vacíos para cada No Terminal
    followResults = {nt: set() for nt in rProductions}
    
    # 2. Regla de Oro: El símbolo inicial siempre lleva el símbolo de fin de cadena '$'
    # Tomamos la primera llave del diccionario como símbolo inicial
    simboloInicial = list(rProductions.keys())[0]
    followResults[simboloInicial].add('$')
    
    # 3. Bucle Iterativo: Repetimos hasta que los conjuntos de FOLLOW dejen de crecer
    huboCambios = True
    while huboCambios:
        huboCambios = False
        # Guardamos cuántos elementos había antes de empezar esta vuelta
        totalElementosAntes = sum(len(s) for s in followResults.values())
        
        # Recorremos cada No Terminal (A) y sus producciones
        for nt_padre, producciones in rProductions.items():
            for produccion in producciones:
                # Analizamos cada símbolo (B) dentro de la producción: A -> alpha B beta
                for i in range(len(produccion)):
                    B = produccion[i]
                    
                    # Solo nos interesa el FOLLOW de los No Terminales
                    if B in rProductions:
                        # --- CASO 1: ¿Hay algo después de B? (beta) ---
                        if i + 1 < len(produccion):
                            beta = produccion[i+1:]
                            
                            # Calculamos el FIRST de todo lo que sigue (beta)
                            # Para simplificar: tomamos el FIRST del símbolo inmediato siguiente
                            primer_sig = produccion[i+1]
                            
                            if primer_sig in rProductions:
                                # Si lo que sigue es No Terminal, le pedimos su FIRST
                                f_sig = firstResults[primer_sig]
                                followResults[B].update(f_sig - {'ε'})
                                
                                # Si ese FIRST tiene épsilon, B también hereda el FOLLOW del padre (A)
                                if 'ε' in f_sig:
                                    followResults[B].update(followResults[nt_padre])
                            else:
                                # Si lo que sigue es un Terminal, se agrega directo al FOLLOW de B
                                followResults[B].add(primer_sig)
                        
                        # --- CASO 2: B está al final de la producción (A -> alpha B) ---
                        else:
                            # B hereda todo el FOLLOW de su padre (A)
                            followResults[B].update(followResults[nt_padre])
                            
        # Si al final de la vuelta hay más elementos que antes, seguimos iterando
        totalElementosDespues = sum(len(s) for s in followResults.values())
        if totalElementosDespues > totalElementosAntes:
            huboCambios = True
            
    return followResults

def verifyTerminal(rightRules):
    #Aquí buscará letras como + - * / pero solo una letra si es que eso se le llaman letras
    terminalFounded = False
    for terminal in terminals:
        #Si la letra que vino 
        if(rightRules == terminal):
            terminalFounded = True
            break
    return terminalFounded

if __name__ == "__main__":
    result = makegramatic()
    firstResults = {}
    for key in result:
        first(key, result, firstResults)

    print("FIRST: \n")
    for key, valores in firstResults.items():
        print(f"{key}: {valores}")
    
    # Calcular FOLLOW
    resultsFollow = follow(result, firstResults)

    print("FOLLOW: \n")
    for key, valores in resultsFollow.items():
        print(f"{key}: {valores}")

#Ok, al parecer la lista de reglas no debería ser así:["S", "->", "id:S"] sino así
"""
Así{
  "S": [["A", "B"]],
  "A": [["a", "A"], ["ε"]],
  "B": [["b", "B"], ["c"]]
}
"""