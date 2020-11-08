from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer


#libs a parte pip install krovetzstemmer
from krovetzstemmer import Stemmer as KrovetzStemmer

# st = LancasterStemmer()
# print(st.stem('itemization'))

# pt = PorterStemmer()
# print(pt.stem('itemization'))


# sn = SnowballStemmer(language='english')
# print(sn.stem('itemization'))


# ks = KrovetzStemmer()
# print(ks.stem('itemization'))



# para portugues

from nltk.stem import RSLPStemmer

pt0 = RSLPStemmer()
print(pt0.stem('banimento'))
# pt1 = LancasterStemmer(language='portuguese')

# print(pt1.stem('banimento'))

pt2 = SnowballStemmer(language='portuguese')

print(pt2.stem('banimento'))

# pt3 = PorterStemmer(language='portuguese')
# print(pt3.stem('banimento'))

# pt4 = LancasterStemmer(language='portuguese')
# print(pt4.stem('banimento'))
