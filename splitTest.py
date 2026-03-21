import sys

terminals = {"id","num","string",":","+","-","*","/","=","==","!=","<",">","(",")"}

def makegramatic():
    rulesQuantity = int(input("¿Cuántas reglas de producción necesita? \n"))
    listOfRules = {}

    for i in range(0, rulesQuantity):
        listRule = []
        print("-" * 30 + "Nueva regla" + "-" * 30)
        lr = input("Lado izquierdo (Ej: E): \n").strip()
        rr = input("Lado derecho (Ej: T E' | id): \n")
        
        # 1. Separamos por el operador OR (|)
        splitRule = rr.split("|")

        for rule in splitRule:
            # 2. TOKENIZADO INTELIGENTE:
            # Si el usuario NO puso espacios (ej: "TE'"), intentamos separar 
            # basándonos en mayúsculas o símbolos conocidos.
            # Pero lo más seguro es pedir espacios o usar esta lógica:
            raw_tokens = rule.strip().split()
            
            # Si el split no separó nada (ej: "TE'"), podrías necesitar 
            # un separador más avanzado, pero por ahora, exijamos espacios:
            listRule.append(raw_tokens)
            
        listOfRules[lr] = listRule
    return listOfRules

def calcular_first(simbolo, gramatica, memo_first):
    if simbolo in memo_first:
        return memo_first[simbolo]
    
    firsts = set()
    
    # CASO 1: Es un Terminal (No es una llave en el diccionario)
    # También manejamos el caso de caracteres especiales como ( o +
    if simbolo not in gramatica:
        return {simbolo}
    
    # CASO 2: Es un No Terminal
    for produccion in gramatica[simbolo]:
        # Si la producción es vacía o directamente epsilon
        if not produccion or produccion[0] == 'ε':
            firsts.add('ε')
        else:
            for i, char in enumerate(produccion):
                res_char = calcular_first(char, gramatica, memo_first)
                
                # Si el First del símbolo actual tiene épsilon
                if 'ε' in res_char:
                    firsts.update(res_char - {'ε'})
                    # Si es el último símbolo de la producción, agregamos ε al First del padre
                    if i == len(produccion) - 1:
                        firsts.add('ε')
                else:
                    # Si no hay épsilon, agregamos y dejamos de procesar esta producción
                    firsts.update(res_char)
                    break
    
    memo_first[simbolo] = firsts
    return firsts

if __name__ == "__main__":
    result = makegramatic()
    print("\nEstructura de la Gramática:", result)
    
    first_resultados = {}
    # Calculamos FIRST para todos los No Terminales del diccionario
    for nt in result:
        calcular_first(nt, result, first_resultados)

    print("\nFIRST:")
    for nt, valores in sorted(first_resultados.items()):
        # Formateo para que se vea limpio
        print(f"{nt}: {{ {', '.join(valores)} }}")