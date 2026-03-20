terminals = {"id","num","string",":","+","-","*","/","=","==","!=","<",">"}

numerRules = int(input("¿Cuántas reglas necesitdas? \n"))

listOflist = {}

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
            print(rr)
            i += 1
            continue
        #Si llegó hasta aquí fue porque tuvo que haber encontrado alguna letra minuscula
        print(rr)
        aux += rr
        oldIndex = i

        #Se elimina la letra en la posición en la que estaba eso significa que si tenemos ["i","d"] se eliminaría ambos
        #Sin embargo al final de todo esto se concatenan las letras y se verifican lo que hace que tengamos ["id"]
        listRr.pop(i)
        print(listRr)
        isterminal = verifyTerminal(aux)

        #Si la palabra formada es terminal se debe poner como reemplazo
        if isterminal:
            print(oldIndex)
            print(aux)
            listRr.insert(oldIndex, aux)
            aux = ""
            i += 1 



def verifyTerminal(rightRules):
    #Aquí buscará letras como + - * / pero solo una letra si es que eso se le llaman letras
    terminalFounded = False
    for terminal in terminals:
        #Si la letra que vino 
        if(rightRules == terminal):
            terminalFounded = True
            break
    return terminalFounded

for i in range(0,numerRules):
    lr = input("Regla izquierda \n")
    rr = input("Regla derecha \n")
    listRule = list(rr)
    refineList(listRule)
    listOflist[lr] = listRule

print(listOflist)
        