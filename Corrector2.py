import pickle, sys
from decimal import Decimal
import itertools
import math

kg_index = {}
words_dictionary = {}

wordDicFile = open('./words.dict' , 'r')
kgIndexFile = open('./kgIndex.dict' , 'r')
bigramWordDicFile = open('./bigramWords.dict' , 'r')

print >> sys.stderr, '\nLoading words dictionary!\n'
words_dictionary = pickle.load(wordDicFile)
print >> sys.stderr, '\nLoading K-gram index dictionary!\n'
kg_index = pickle.load(kgIndexFile)
print >> sys.stderr, '\nLoading bigram words index !\n'
bigramWords_dictionary = pickle.load(bigramWordDicFile)
termCount = open('./terms.count' , 'r')
NumberOfTerms = int(pickle.load(termCount))

def editDistance(s1, s2):
    s1= str(s1)
    s2 = str(s2)
    
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in xrange(-1,lenstr1+1):
        d[(i,-1)] = i+1
    for j in xrange(-1,lenstr2+1):
        d[(-1,j)] = j+1
 
    for i in xrange(lenstr1):
        for j in xrange(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i,j)] = min(
                           d[(i-1,j)] + 1, # deletion
                           d[(i,j-1)] + 1, # insertion
                           d[(i-1,j-1)] + cost, # substitution
                          )
            if i and j and s1[i]==s2[j-1] and s1[i-1] == s2[j]:
                d[(i,j)] = min (d[(i,j)], d[i-2,j-2] + cost) # transposition
 
    return d[lenstr1-1,lenstr2-1]


def kgrams(word):
  word  = str(word)
  k = 2
  grams = []
  
  word = ("$" * (k-1)) + word + ("$" * (k-1)) 
  for i in range(len(word)):
    g = word[i:i+k]
    if len(g) < k:
      break
    grams.append(str(g))
  return grams

def GetKGramCandidates(testWord):
  temp = []
  resultList = []
  tempWordDic = {}
  kgs =  kgrams(str(testWord))
  
  for kg in kgs:
    temp.append((str(kg),kg_index[str(kg)]))
  
  for kg in temp:
    for word in kg[1]:
      if word in tempWordDic:
        tempWordDic[word].append(kg[0])
      else:
        tempWordDic[word] = [kg[0]]
  
  #calculate thresholds for words
  for w in tempWordDic.keys():
    unionSet = set(kgrams(w)).union(kgs)
    interesctionSet = tempWordDic[w]
    threshold = Decimal(len(interesctionSet)) / Decimal(len(unionSet))
    resultList.append((w, threshold))
    
  resultList = sorted(resultList,key= lambda x: x[1],reverse=True)
  
  finalResulList = []
  
  """ get items untill threshold is 0.4"""
  for i in resultList:
    if i[1] < 0.4:
      break
    #finalResulList.append(i)
    finalResulList.append(i[0])
  
  return finalResulList

"""Filters k-gram candidates which are worse then 2 edit distance"""
def FindTermCandidates(word):
  candidates = []
  
  kGramCandidates =  GetKGramCandidates(word)
  
  #it means word is correct, no need to calculate edit distances
  if len(kGramCandidates):
    if(kGramCandidates[0] == word):
      return [(word,0)]
    
    for can in kGramCandidates:
      if editDistance(word, can) <= 2:
        candidates.append((can,editDistance(word, can)))
    return candidates
  else:
    return [(word,0)]

def FindCandidatesBeforeCrossProduct(phrase):
  results = []
  terms  = phrase.split()
  for term in terms:
    results.append((term,FindTermCandidates(term)))
  return results

def FindCandidates(phrase):
  listOfCandidates = FindCandidatesBeforeCrossProduct(phrase)
  b = map(lambda x:x[1],listOfCandidates)

  candidates = []
  for i in itertools.product(*b):
    temp= 0 
    tempZero = 0
    tempText = ' '.join(map(str, map(lambda x:str(x[0]),i)))
    
    for term in i:
      if term[1] == 0:
        tempZero = tempZero + 1
      else:
        temp = temp + term[1]
     
    candidates.append((tempText , (temp,tempZero)))
  
  return candidates
  
print FindCandidates("2009 electochemical deposition")