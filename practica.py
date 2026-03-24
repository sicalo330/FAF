def makeGramatic():
    ruleQuantity = int(input("cantidad de reglas"))
    splitRule = ""

    listOfRules = {}

    for i in range(0,ruleQuantity):
        listRule = []

        lr = input("lado izquierdo")
        rr = input("lado derecho")

        splitRule = rr.split("|")

        for rule in splitRule:
            tokens = rule.strip().split()
            listRule.append(tokens)

        listOfRules[lr] = listRule
    
    return listOfRules

def first(key, rProduction,firstResults):
    if key in firstResults:
        return firstResults[key]
    
    firsts = set()

    if key not in rProduction:
        return {key}
    
    for produccion in rProduction:
        if produccion == 'ε':
            firsts.add("ε")
        else:
            for char in produccion:
                resultsChar = first(key, rProduction, firstResults)

                if 'ε' in resultsChar:
                    firsts.update(resultsChar - {'ε'})
                    if char == produccion[-1]:
                        firsts.add("ε")
                else:
                    firsts.update(resultsChar)
                    break
    
    firstResults[key] = firsts
    return firsts

def getNullable(firstResults):
    nullable = set()

    for nt,firstSet in firstResults:
        if 'ε' in firstSet:
            nullable.add(nt)
    return nullable

