#Todas las ayudas de la IA que se ven en los comentarios fueron solo recomendaciones o instrucciones lógicas que me daban nunca fue código en bruto
#Ahora el problema es que tengo que hacer que idetnifique un operador or | por ejemplo A -> a|b

#terminals = {"id","num","string",":","+","-","*","/","=","==","!=","<",">","(",")"}

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
        print(f'------------------------------Regla {i + 1}---------------------------------')
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

#Segunda ayuda de la IA: gemini me recomendó usar set en vez de una lista corriente ya que los first o los follows pueden tener duplicados redundantes
#Además con los sets se puede usar update que es el equivalente de una unión de conjuntos tal y como lo dice el librro
def first(key, rProductions, firstResults):
    #Este if es para cuando llegue al follow
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

def getNullable(firstResults):
    nullable = set()
    
    for nt, firstSet in firstResults.items():
        if 'ε' in firstSet:
            nullable.add(nt)
    
    return nullable

def follow(rProductions, firstResults):
    #Inicializamos el diccionario de follow con sets vacíos para cada no terminal
    #SI ALGO FALLA POSIBLEMENTE ESTÉ AQUÍ   
    followResults = {}

    for nt in rProductions:
        followResults[nt] = set()
    
    # El símbolo inicial siempre lleva el símbolo de fin de cadena "$""
    #Tomamos la primera llave del diccionario como símbolo inicial
    simboloInicial = list(rProductions.keys())[0]
    followResults[simboloInicial].add('$')
    
    #Esto repiute hasta que los conjuntos de Fllow dejen de crecer
    changes = True
    while changes:
        changes = False
        #Guardamos cuántos elementos había antes de empezar esta vuelta
        totalElementosAntes = sum(len(s) for s in followResults.values())
        
        #Recorremos cada No Terminal(A) y sus producciones
        for key, producciones in rProductions.items():
            for produccion in producciones:
                #Analizamos cada símbolo(B) dentro de la producción: A -> alpha B beta
                for i in range(len(produccion)):
                    B = produccion[i]
                    
                    # Solo nos interesa el FOLLOW de los No Terminales
                    if B in rProductions:
                        #Esto pregunta si hay algo después del símbolo que se le quiere buscar el FOLLOW-
                        if i + 1 < len(produccion):
                            #El : del final significa que toma toda la lista i+1 y todo lo que queda en la derechs
                            #Esto hace β = Yi+1 … Yk del libro, recorre toda la cadena de busqueda
                            beta = produccion[i+1:]
                            #Recorremos toda la cadena
                            for simbolo in beta:
                                #Busca si el símbolo es una key en alguna regla de producción
                                if simbolo in rProductions:
                                    f_sig = firstResults[simbolo]
                                    followResults[B].update(f_sig - {'ε'})
                                    
                                    #SI NO hay epsilon, el código se detiene
                                    #Caso 1:  SI el símbolo que estaba a la derecha tuvo un epsilon hay que ir hasta el otro símbolo a la derecha
                                    #Caso 2: Si el símbolo No estaba ahí, entonces se rompe el ciclo porque ya no es necesario revisar más
                                    if 'ε' not in f_sig:
                                        break
                                else:
                                    #Si llegó a este else es porque es un terminal y se agrega normal
                                    followResults[B].add(simbolo)
                                    break
                            else:
                                # Si TODOS en beta eran nullable → hereda FOLLOW del padre
                                followResults[B].update(followResults[key])
                        
                        #B está al final de la producción (A -> alpha B) ---
                        else:
                            #Si B lleó hasta aquí significará que heredará el follow de su padre PENDIENTE DE ESTE
                            followResults[B].update(followResults[key])
        # Si al final de la vuelta hay más elementos que antes, seguimos iterando
        totalElementosDespues = sum(len(s) for s in followResults.values())
        if totalElementosDespues > totalElementosAntes:
            changes = True
            
    return followResults

if __name__ == "__main__":
    result = makegramatic()

    #Calcular first
    firstResults = {}
    for key in result:
        first(key, result, firstResults)

    print("\nFirst:")
    for key, valores in firstResults.items():
        print(f"{key}: {valores}")
    
    nullableSet = getNullable(firstResults)

    print("\nNullable")
    for nt in nullableSet:
        print(nt)
    
    #Calcular follow
    resultsFollow = follow(result, firstResults)

    print("\nFollow:")
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