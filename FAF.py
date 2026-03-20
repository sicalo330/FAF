#Ahora el problema es que tengo que hacer que idetnifique un operador or | por ejemplo A -> a|b

terminals = {"id","num","string",":","+","-","*","/","=","==","!=","<",">","(",")"}

def makegramatic():
    rulesQuantity = int(input("¿Cuántas reglas de producción necesita? \n"))
    #Esta es la lista de una sola regla, si esta es S' -> S la lista debería ser ["S'", "->", "S"]
    splitRule = ""

    listOfRules = {}
    rulesOfRules = []
    #Tengo que utilizar la función match para hacer un switch case
    #Para ello supongo que lo mejor sería ponerlo dentro del for ya que este representa la cantidad de relgas que hay
    #¿O quizás lo mejor sería hacer otro for anidado?
    for i in range(0,rulesQuantity):
        listRule = []
        #Inicializar y reinicializar con cada iteración
        print("------------------------------Nueva regla---------------------------------")
        lr = input("¿Cuál es el lado izquierdo de la regla de producción? (Ejemplo: S') \n")
        #Es obligatorio que la regla de producción tenga un produce (->)
        #El lado derecho es lo que puede ser más de uno, ¿pongo otro for?
        rr = input("¿Cuál es o cuáles son sus reglas de la derecha? (Ejemplo S, id:S, EE) \n")
        splitRule = rr.split("|")

        #Tengo que verificar que splitRule sea una lista tal que así ["i","d",":","S","|","b"]

        for rule in splitRule:
            result = refineList(list(rule))
            listRule.append(result)

        # beyondOr.append(splitRule[1])

        # rule = list(splitRule[0])   
        # print(rule)
        # refineList(rule)

        # listRule.append(rule)
        # listRule.append(beyondOr)
        #singleRule.append(rr) Tal vez poner la lista en como estaba antes me sirve de algo en el futuro
        listOfRules[lr] = listRule
    #Por el momento solo es capaz de imprimir una regla con solo un estado por ejemplo S' -> S
    #Mi plan es hacer una matriz, es decir una lista que tenga posiciones tales como  ["S'","->","s"] dentro de otra lista
    #Dentro de otral lista más grande para poder ciclar en todas las reglas
    return listOfRules

def printAllRules(listOfRules):
    #Es lo más parecido a un foreach que encontré
    #Por ahora las relgas de las derechas no detectan uno "S" o muchos "id:S" espero que no sea un problema mayor
    for index,rule in enumerate(listOfRules):
        print(f'Regla {index}')
        print(rule)

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
    print(result)
    # printAllRules(result)

#Ok, al parecer la lista de reglas no debería ser así:["S", "->", "id:S"] sino así
"""
Así{
  "S": [["A", "B"]],
  "A": [["a", "A"], ["ε"]],
  "B": [["b", "B"], ["c"]]
}
"""