#Todas las ayudas de la IA que se ven en los comentarios fueron solo recomendaciones o instrucciones lógicas que me daban nunca fue código en bruto
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
    #Primera ayuda de la IA: Chatgpt no me dio el código, solo me recomendó usar un while en vez de un for
    #Si anteriormente se usaba un for aquí, no estoy muy seguro si algun commit lo tiene registrado
    #Lo que sucedió fue que yo estaba iterando en la misma lista que estaba alterando para poder refinar las terminales y no terminales de la lista
    #Y eso resultaba en errores de lógica, por lo tanot chatgpt NO me dio código, solo me dijo que usara un while en vez de un for
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

#Segunda ayuda de la IA: gemini me recomendó usar set en vez de una lista corriente ya que los first o los follows pueden tener duplicados redundantes
#Además con los sets se puede usar update que es el equivalente de una unión de conjuntos tal y como lo dice el librro
def first(key, rProductions, firstResults):
    #Me gustaría un if que devuelva si ya se calculo, para optimizar jeje
    if key in firstResults:
        return firstResults[key]
    #No sé muy bien qué estoy haciendo
    firsts = set()
    #Si es un terminal
    if key not in rProductions:
        # print("Entró " + key)
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
                    firsts.update(resultsChar - {'ε'})
                    if char == produccion[-1]:
                        firsts.add('ε')
                else:
                    firsts.update(resultsChar)
                    break
    
    firstResults[key] = firsts
    return firsts

def follow(results, firstResults):
    print("Gramática: " + str(results))
    #Esto inicicializa el diccionario de follow con sets vacíos para las no terminales
    # Forma con bucle tradicional (más código, misma función)
    followResults = {}

    for result in results:
        #Se crea un set o conjunto vacío para cada no terminal, por ejemplo si la gramática es {'S': [['A']], 'A': [['a']]} entonces
        #followResults sería {'S': set(), 'A': set()}
        followResults[result] = set()
    
    #El símbolo inicial siempre lleva el símbolo de fin de cadena $, es decir la primera llave debe tener un $
    simboloInicial = list(results.keys())[0]
    followResults[simboloInicial].add('$')
    #Se repetimos hasta que los conjuntos de FOLLOW dejen de crecer
    changes = True
    while changes:
        changes = False
        totalElementsBefore = 0
        for setFollowResults in followResults.values():#Este .values() de aquí es importante porque lo que debo sacar son los valores de cada regla no la llave de este
            #Lo que hace esto es tomar la cantidad de elmentos que tiene una llave y lo pone en setQuantity para poder sumarlo a
            #totalElemtBefore
            setQuantity = len(setFollowResults)
            totalElementsBefore = totalElementsBefore + setQuantity 
        
        #Esto itera en reglas de producción, es decir la parte de la derecha
        for key, rules in results.items():
            #Esto itera en las regas sacando cada regla

            #Ya puse los dos fors, es que no entiendo por qué no funciona, no quiero usar otro for más eso ya sería feísimio
            #Por la forma en la que se construye la gramática necesito 3 fors, que feo ojalá pudiera cambiarlo un poco
            #Pense que con dos fors ya era suficiente jeje
            for rule in rules:
                for i in range(len(rule)):
                    # print("---------------------for 3---------------------")
                    B = rule[i]
                    # print("regla: " + str(B))
                    # print("rule: " + str(rule))
                    # print("results: " + str(results))
                    #Lo que hace es buscar si B es alguna llave en las demás reglas, por ejemplo si tenemos S -> A A-> a, B=A entra porque A es una llave de una regla
                    if B in results:
                        # print("Entró")
                        #Revisa si la relga tiene algo más a la derecha, si NO se sale del rango es porque sí tiene algo a la derecha
                        if i + 1 < len(rule):
                            # print("---------------------dentro del if i + 1 < len(rule):---------------------")
                            # print("este rule pasó: " + str(rule))
                            # print("con este results: " + str(results))
                            #Creo que deberísa usar beta para algo
                            #beta = rule[i+1:]

                            #Esto toma el símbolo siguiente
                            firstS = rule[i+1]
                            #Pasa lo mismo que más arriba, toma el símbolo de la derecha y si es una no terminal buscará su first
                            #Si la gramática es S -> A B A->a B -> b lo que sucederá es que tomará A e irá con el de la derecha B, y buscará si B tiene su propia regla
                            #Como en esta gramática hipotética Sí tiene una regla, lo que se hará es tomar su first, en este caso el b
                            if firstS in results:
                                # Si lo que sigue es No Terminal, le pedimos su FIRST
                                # print("firstResults: " + str(firstResults))
                                # print("firstS: " + str(firstS))
                                # print("followResults: " + str(followResults))
                                # print("B: " + str(B))
                                firstValue = firstResults[firstS]
                                # print("firstValue: " + str(firstValue))
                                #Recordar que B sería el key con el que entró, es decir que si A -> B y B -> b, la variable B = A
                                #Por lo tanto lo que sucede aquí es que en el json followResults se va a usar la posición A para guardar el first de B que en este caso sería b
                                #Por lo tanto si se tiene esta gramática {'S': [['A', 'B']], 'A': [['a', 'C']], 'B': [['b']], 'C': [['ε'], ['d']]}
                                #El conjunto inicial se vería así {'S': {'$'}, 'A': set(''), 'B': set(...), 'C': set(...)}
                                #El followResults de A sería b, por lo tanto se vería algo así {'S': {'$'}, 'A': set('b'), 'B': set(...), 'C': set(...)}
                                #El - {'ε'} significa que haga update exceptuando el - ε
                                #Por lo tanto si el conjunto A es {} y el conjunto firstValue es {'b' - 'ε'}
                                #Si en el futuro el conjunto A encuentra otro follow quedaría así
                                #Conjunto A {'b'} y el conjunto firstValue {'$' - 'ε'}
                                #Conjuinto A sería {'$','b'} nunca con epsilon
                                followResults[B].update(firstValue - {'ε'})
                                
                                #Si el first tiene epsilon, entonces hereda el follow del padre
                                if 'ε' in firstValue:
                                    # print("se encontró un epsilon")
                                    followResults[B].update(followResults[key])
                            else:
                                #Si no entró al if significa que ya no hay más por buscar y se agregará al json followResults
                                followResults[B].add(firstS)
                        
                        #Si se sale del rango es porque está al final, entonces lo que debería hacer es heredar el follow de su padre
                        else:
                            #Si B lleó hasta aquí significará que heredará el follow de su padre PENDIENTE DE ESTE
                            followResults[B].update(followResults[key])
        # Si al final de la vuelta hay más elementos que antes, seguimos iterando
        totalElementosDespues = sum(len(s) for s in followResults.values())
        if totalElementosDespues > totalElementsBefore:
            changes = True
            
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

    #Aquí se calcula el follow
    print("FIRST: \n")
    for key, valores in firstResults.items():
        print(f"{key}: {valores}")
    
    #Aquí se calcula el follow
    resultsFollow = follow(result, firstResults)

    print("FOLLOW: \n")
    for key, valores in resultsFollow.items():
        print(f"{key}: {valores}")

#Ok, al parecer la lista de reglas no debería ser así:["S", "->", "id:S"] sino así

#Tercera ayuda de la IA: Noah del pasado escribió esto, y sí al parecer poner la gramática como está abajo ayuda mucho más porque es más fácil acceder, menos mal no seguí
#con lo de ariba
"""
Así{
  "S": [["A", "B"]],
  "A": [["a", "A"], ["ε"]],
  "B": [["b", "B"], ["c"]]
}
"""