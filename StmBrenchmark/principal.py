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
    
    lemmas = montaGrupos("words_sample.txt")
    stems = montaGrupos("stems.txt")        
    p = Paice(lemmas, stems)
    print(p)

if __name__ == "__main__":
    main()