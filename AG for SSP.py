from random import *
from operator import *
from time import *

def initPopulacao(numPop, n):
    populacao = []
    
    for i in range(numPop):
        cromossomo = []
        while(len(cromossomo) != n):
            i = randint(0,n-1)
            if(cromossomo.count(i) == 0):
                cromossomo.append(i)        
        populacao.append(cromossomo)
    return populacao

def lenOverlapString(a,b):
    flag = 0
    if(a.count(b[0]) == 0):
        return 0
    else:
        #i = a.index(b[0])
        #for j in xrange(1,len(a)-i):
        #   if(a[i+j] != b[j]):
        #       return 0
        if(len(a) >= len(b)):
            x = len(b)-1
        else:
            x = len(a)-1
        while(x > 0):
            for i in xrange(0,x):
                if(b[i] != a[-x+i]):
                    flag = 1
            if(flag == 0):
                return x
            else:
                flag = 0
                x = x-1
    return x

def mergeStrings(a,b):
    mergedString = ""
    l = lenOverlapString(a,b)
    mergedString = a + b[l:]
    return mergedString

def superstring(cromossomo, instancia):
    s = ""
    b = instancia[cromossomo[-1]]
    a = instancia[cromossomo[-2]]
    s = mergeStrings(a,b)
    for i in xrange(0,len(cromossomo)-2):
        a = instancia[cromossomo[-i-3]]
        s = mergeStrings(a,s)
    return s

def funcaoAptidao(cromossomo, instancia):
    valor = 0
    for i in xrange(1,len(cromossomo)):
        indexB = cromossomo[-i]
        indexA = cromossomo[-i-1]
        b = instancia[indexB]
        a = instancia[indexA]
        valor += lenOverlapString(a, b)
    return valor

# Toma uma populacao como entrada, calcula e grava o valor de aptidao de cada individuo
def avaliarAptidaoPopulacao(populacao, instancia):
    classificacao = []
    
    for s in populacao:
        valor = funcaoAptidao(s, instancia)
        classificacao.append((s,valor))
    return classificacao

# Funcao de selecao: Ranking
# Ordena os individuos pela aptidao e seleciona os n primeiros        
def selecaoRanking(populacao, n):
    populacao.sort(key=itemgetter(1))
    selecao = populacao[len(populacao)-n:]
    return selecao
'''
# Funcao de cruzamento: Ponto unico
# A funcao usa (x,y), portanto nao existe mistura de geracoes
def crossoverPontoUnico(selecionados, n):
    novaGeracao = []
    for i in range(n):
        seed(time())
        pai_1 = selecionados[randint(0,len(selecionados)-1)][0]
        pai_2 = selecionados[randint(0,len(selecionados)-1)][0]
        filho1 = pai_1[0:len(pai_1)/2] + pai_2[len(pai_2)/2:len(pai_2)]
        filho2 = pai_2[0:len(pai_1)/2] + pai_1[len(pai_2)/2:len(pai_2)]
        #print("Pais: "+ pai_1 +"-"+pai_2)
        #print("Filhos: "+ filho1 +"-"+filho2)
        novaGeracao.append(filho1)
        novaGeracao.append(filho2)
    return novaGeracao
'''

def orderCrossover(selecionados, n):
    novaGeracao = []
    for i in range(n):
        seed(time())
        pai1 = selecionados[randint(0,len(selecionados)-1)][0]
        pai2 = selecionados[randint(0,len(selecionados)-1)][0]
        filho1 = []
        filho1 += pai1[0:len(pai1)/2]

        for j in range(len(pai2)):
            if(filho1.count(pai2[j]) == 0):
                filho1.append(pai2[j])
            if(len(filho1) == len(pai1)):
                break
        novaGeracao.append(filho1)

        filho2 = []
        filho2 += pai2[0:len(pai2)/2]

        for j in range(len(pai1)):
            if(filho2.count(pai1[j]) == 0):
                filho2.append(pai1[j])
            if(len(filho2) == len(pai2)):
                break
        novaGeracao.append(filho2)

    return novaGeracao

def crossoverPontoAleatorio(selecionados, n):
    novaGeracao = []
    for i in range(n):
        seed(time())
        pai_1 = selecionados[randint(0,len(selecionados)-1)][0]
        pai_2 = selecionados[randint(0,len(selecionados)-1)][0]
        print('pai 1'+str(pai_1))
        print('pai 2'+str(pai_2))
        filho1 = []
        flag = 1
        while(flag == 1):
            flag = 0
            cut1 = randint(0,len(pai_1)-2)
            genes1 = pai_1[cut1:cut1+2]
            for g in genes1:
                if(filho1.count(g)!= 0):
                    flag = 1
                    continue
            
        filho1 += genes1
        flag = 1
        
        while(flag == 1):
            flag = 0
            cut1 = randint(0,len(pai_2)-2)
            genes2 = pai_2[cut1:cut1+2]
            for g in genes2:
                if(filho1.count(g)!= 0):
                    flag = 1
                    continue

        filho1 += genes2

        while(len(filho1)!=len(pai_1)):
            j = randint(0,len(pai_1)-1)
            if(filho1.count(j)==0):
                filho1.append(j)
                
        novaGeracao.append(filho1)
    return novaGeracao
        
# Funcao de mutacao: Aleatoria
# No maximo 10% da populacao vai sofrer mutacao.
# Mutacao: um caractere da string eh modificado aleatoriamente por outro no intervalo a-z
def mutacaoAleatoria(populacao):
    n = len(populacao)
    for i in range((n/10)):
        seed(time())
        gene1 = randint(0,len(populacao[0])-1)
        gene2 = randint(0,len(populacao[0])-1)
        indiceCromossomo = randint(0,n-1)
        #print(gene1,gene2,indiceCromossomo)
        valor1 = populacao[indiceCromossomo][gene1]
        valor2 = populacao[indiceCromossomo][gene2]
        populacao[indiceCromossomo][gene1] = valor2
        populacao[indiceCromossomo][gene2] = valor1
        
# Retorna o somatorio da aptidao da populacao dividido pelo numero de individuos
def calcularAptidaoMedia(populacao):
    soma = 0
    for i in populacao:
        soma += i[1]
    return soma/float(len(populacao))

# AG
def genetico(instancia, n, geracoes):
    populacao = initPopulacao(n,len(instancia))
    
    for i in range(geracoes):
        populacaoPonderada = avaliarAptidaoPopulacao(populacao, instancia)
        populacaoSelecionada = selecaoRanking(populacaoPonderada,n/2)
        #populacao = crossoverPontoAleatorio(populacaoSelecionada, n)
        populacao = orderCrossover(populacaoSelecionada, n/2)
        mutacaoAleatoria(populacao)
        
        media = calcularAptidaoMedia(populacaoPonderada)
        print("[+] Geracao: "+str((i+1))+"\t\tAptidao Media: "+str(media))
        if(media < 0.5):
            break

    return populacao

def catConjunto(instancia):
    cat = ''
    for i in instancia:
        cat += i

    return cat

def retornarMelhorIndividuo(populacao, instancia):
    pp = avaliarAptidaoPopulacao(populacao, instancia)
    fitnessBest = pp[0][1]
    indexBest = 0

    for p in pp:
        if(p[i][1] > fitnessBest):
            fitnessBest = p[i][1]
            indexBest = i

    return pp[indexBest][0]
    

from random import *

def generateSSP_Instance(lenString = 1000, numStringCp = 10, minLen = 50, maxLen = 60):
    instance = []
    sigma = ['a','c','g','t']

    string = ""    
    for i in range(lenString):
        letter = randint(0,3)
        string += sigma[letter]

    stringCp = ""
    for i in range(numStringCp):
        stringCp += string
    numFrag = len(stringCp)/((minLen + maxLen)/2)

    cutInit = 0
    for i in range(numFrag):
        cutFinal = randint(minLen + cutInit, maxLen + cutInit)
        s = stringCp[cutInit:cutFinal]
        cutInit = cutFinal
        instance.append(s)

    while(len(instance[-1]) < minLen):
        instance.pop(-1)
        
    #return instance,stringCp
    return instance
        
#usar "".find(sub)

'''
if __name__ == "__main__":
    print('oi')
  
    frase = "algoritmos"
    n = 10
    geracoes = 3000
    
    populacao = genetico(frase, n, geracoes)
''' 

'''
lenString representa o tamanho da string a ser gerada
'''


