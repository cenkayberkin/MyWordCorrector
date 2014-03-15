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
  k = 2
  grams = []
  word = ("$" * (k-1)) + word + ("$" * (k-1)) 
  for i in range(len(word)):
    g = word[i:i+k]
    if len(g) < k:
      break
    grams.append(g)
  return grams

def GetKGramCandidates(testWord):
  temp = []
  resultList = []
  tempWordDic = {}
  kgs =  kgrams(testWord)
  
  for kg in kgs:
    temp.append((kg,kg_index[kg]))
  
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
    if i[1] < 0.5:
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
    
    if temp < 2:  
      candidates.append((tempText , (temp,tempZero)))
  
  candidates = sorted(candidates ,key= lambda x: x[1][0])
    
  return candidates
  
  
def CalcProb(term):
  result = 0
  if term in words_dictionary:
    countTerm = words_dictionary[term]
    result = math.log10(Decimal(countTerm) / Decimal(NumberOfTerms))
    #print "=> "+ term +" " + str(countTerm)  + " / " + str(NumberOfTerms) +  " = " + str(result) 
  else:
    result = math.log10(Decimal(1) / Decimal(NumberOfTerms + 26))
    #print "=>  1  / number of terms = "  + str(result)  
  return result

def CalcCondProb(terms):
  result = 0
  term = terms[0]+"|"+terms[1]
  if term in bigramWords_dictionary:
    secondTerm = words_dictionary[terms[1]]
    countTerm = bigramWords_dictionary[term]
    #print "=> " + term + " / " + terms[1]
    result = math.log10(Decimal(countTerm) / Decimal(secondTerm)) 
  else:
    keyWord = terms[1]
    if keyWord in words_dictionary:
      countTerm = words_dictionary[keyWord]
      result = math.log10(Decimal(countTerm) / Decimal(NumberOfTerms))
      #print "=> " + keyWord + " / " + "count terms " + str(result) 
    else:
      result = math.log10(Decimal(1) / Decimal(NumberOfTerms + 26))
      #print "=> 1 / " + "count terms + 26" + " result = " + str(result)

  #print "res " +  str(result)  
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

def CalculateBestCandidate(phrase):
  result = []
  candidates =  FindCandidates(phrase)
  for candidate in candidates:
    ProblanModel = CalcLanModel(candidate[0])
    ProbNoisyChannel = Decimal(0.1) ** int(candidate[1][0])  
    probability = Decimal(ProblanModel) * ProbNoisyChannel
    result.append((candidate[0],probability))

  result = sorted(result,key= lambda x: x[1], reverse=True)
  return result[0]
  

if __name__ == '__main__':
  if len(sys.argv) != 4:
    print "Usage: ./runcorrector.sh <dev|test> <uniform|empirical> <queries file>"
    sys.exit()
  mode = sys.argv[1]
  prob_mode = sys.argv[2]
  queries_file = sys.argv[3]
  queryFile = open(queries_file,'r')
  for line in queryFile:
    line = line.rstrip().rstrip('\n')
    print >> sys.stderr, line
    print CalculateBestCandidate(line)

