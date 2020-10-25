from paice import Paice

def montaGrupos(lemmasFile):
    grupos = dict()
    indice = 0
    lemmas = open(lemmasFile,"r").read().replace("**","").split("*")
    
    for lemma in lemmas:
        if indice not in grupos:
           grupos[indice] = []
        lemmaSplit = list(filter(lambda s: s != "",lemma.split("\n")))
        grupos[indice] = grupos[indice] + lemmaSplit 
        indice +=1

    return grupos

def main():
    
    resultados = open("resultados","w")
    #snowball
    lemmas = montaGrupos("words_sample.txt")
    stemSnow = montaGrupos("stems_snowball.txt")
    stemRslp = montaGrupos("stems_rslp.txt")        
    pS = Paice(lemmas, stemSnow)
    pR = Paice(lemmas, stemRslp)

    resultados.write("-----------------APLICACAO DO METODO DE PAICE PARA MEDIR DESEMPENHO DE STEMMERS-----------------\n")    
    resultados.write("--------------------------------------RESULTS SNOWBALL------------------------------------------\n")
    resultados.write(pS.__str__())
    resultados.write("\n--------------------------------------RESULTS RSLP----------------------------------------------\n")
    resultados.write(pR.__str__())
    resultados.write("\n------------------------------------------------------------------------------------------------\n")
    resultados.close()

if __name__ == "__main__":
    main()