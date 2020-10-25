'''
Created on 25 de out de 2020

@author: joaop
'''
from nltk.stem.rslp import RSLPStemmer 
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("portuguese")
lemmas = open("words_sample.txt","r").read().replace("**","").split("\n")

#cria stems para o stemmer snowball em portugues --------------------
snowBallFile = open("stems_snowball.txt","w") 
for lemma in lemmas:
    if len(lemma) > 1:
        snowBallFile.write(stemmer.stem(lemma)+"\n")
    else:
        snowBallFile.write(lemma +"\n")    
 
snowBallFile.close()
#cria stems para o stemmer rslp -------------------------------------
stemmer = RSLPStemmer()
rslpFile = open("stems_rslp.txt","w")
for lemma in lemmas:
    if len(lemma) > 1:
        rslpFile.write(stemmer.stem(lemma)+"\n")
    else:
        rslpFile.write(lemma +"\n")    

rslpFile.close()
#--------------------------------------------------------------------
