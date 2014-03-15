import pickle, sys
from decimal import Decimal
import math

kg_index = {}
words_dictionary = {}

wordDicFile = open('./words.dict' , 'r')
kgIndexFile = open('./kgIndex.dict' , 'r')
bigramWordDicFile = open('./bigramWords.dict' , 'r')
termCount = open('./terms.count' , 'r')

NumberOfTerms = int(pickle.load(termCount))

print >> sys.stderr, '\nLoading words dictionary!\n'
words_dictionary = pickle.load(wordDicFile)
print >> sys.stderr, '\nLoading K-gram index dictionary!\n'
kg_index = pickle.load(kgIndexFile)
print >> sys.stderr, '\nLoading bigram words index !\n'
bigramWords_dictionary = pickle.load(bigramWordDicFile)

def CalcProb(term):
  result = 0
  if term in words_dictionary:
    countTerm = words_dictionary[term]
    result = math.log10(Decimal(countTerm) / Decimal(NumberOfTerms))
    print "=> "+ term +" " + str(countTerm)  + " / " + str(NumberOfTerms) +  " = " + str(result) 
  else:
    result = math.log10(Decimal(1) / Decimal(NumberOfTerms + 26))
    print "=>  1  / number of terms = "  + str(result)  
  return result

def CalcCondProb(terms):
  result = 0
  term = terms[0]+"|"+terms[1]
  if term in bigramWords_dictionary:
    secondTerm = words_dictionary[terms[1]]
    countTerm = bigramWords_dictionary[term]
    print "=> " + term + " / " + terms[1]
    result = math.log10(Decimal(countTerm) / Decimal(secondTerm)) 
  else:
    keyWord = terms[1]
    if keyWord in words_dictionary:
      countTerm = words_dictionary[keyWord]
      result = math.log10(Decimal(countTerm) / Decimal(NumberOfTerms))
      print "=> " + keyWord + " / " + "count terms " + str(result) 
    else:
      result = math.log10(Decimal(1) / Decimal(NumberOfTerms + 26))
      print "=> 1 / " + "count terms + 26" + " result = " + str(result)

  print "res " +  str(result)  
  return result

def CalcLanModel(phrase):
  terms = phrase.split()
  termPairs = zip(terms[:-1],terms[1:])

  result = 0
  if len(terms) == 1:
    result = CalcProb(terms[0])
  elif len(terms) > 1:
      result = CalcProb(terms[0])
      for i in termPairs:
        result = result + CalcCondProb(i)
 
  return result

print CalcLanModel("your majesty had")

