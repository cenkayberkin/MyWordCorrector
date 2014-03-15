import pickle
from decimal import Decimal

bigramWordDicFile = open('./bigramWords.dict' , 'r')
bigramWords_dictionary = pickle.load(bigramWordDicFile)

wordDicFile = open('./words.dict' , 'r')
words_dictionary = pickle.load(wordDicFile)

def CalculateConditionalProbw2w1(w1,w2):
  result  = Decimal(0)
  key = w1+"|"+w2
  if key in bigramWords_dictionary:
    #print Decimal(bigramWords_dictionary[w1+"|"+w2])
    #print Decimal(words_dictionary[w1])
    result = Decimal(bigramWords_dictionary[w1+"|"+w2]) / Decimal(words_dictionary[w1])  
  else:
    #print "hmm"
    result = 1 / Decimal(words_dictionary[w1])
  return result


print CalculateConditionalProbw2w1("memory","of")

