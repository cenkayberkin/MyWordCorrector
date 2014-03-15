import re, pickle
import os,sys

kg_index = {}
words_dictionary = {}
bigramWords_dictionary = {}

def trainUnigrams(features):
  for f in features:
    if f in words_dictionary:
      words_dictionary[f] += 1
    else:
      words_dictionary[f] = 1

def trainBiGrams(features):
  index1 = 0
  index2 = 1
  while index2 < len(features):
    key = features[index1] + "|" + features[index2]
    if key in bigramWords_dictionary:
      bigramWords_dictionary[key]  = bigramWords_dictionary[key] + 1 
    else:
      bigramWords_dictionary[key] = 1
    index1 = index1 + 1
    index2 = index2 + 1
      
def kgrams(word):
  k = 2
  grams = []
  word = ("|" * (k-1)) + word + ("|" * (k-1)) 
  for i in range(len(word)):
    g = word[i:i+k]
    if len(g) < k:
      break
    grams.append(g)
  return grams

def generateKgIndex():
  for word in sorted(words_dictionary.keys()):
    kgs = kgrams(word)
    for kg in kgs:
      if kg in kg_index:
        kg_index[kg].append(word)
      else:
        kg_index[kg] = [word]
  
  
def words(text): return re.findall('[a-z0-9.$]+', text.lower())

termCountFile = open('./terms.count' , 'w')
wordDicFile = open('./words.dict' , 'w')
kgIndexFile = open('./kgIndex.dict' , 'w')
bigramWordDicFile = open('./bigramWords.dict' , 'w')

def TrainCorpus(url):
  
  files = os.listdir(url)
  termCount = 0
  for f in files:
    text = words(open(os.path.join(url, f)).read())
    trainUnigrams(text)
    trainBiGrams(text)
    generateKgIndex()
    termCount = termCount + len(text)
    
  pickle.dump(len(text),termCountFile)


if __name__ == '__main__':
  if len(sys.argv) != 3:
    print "Usage: python models.py <training corpus dir> <training edit1s file>"
    sys.exit()
  training_corpus_loc = sys.argv[1]
  edit1s_loc = sys.argv[2]
  #TrainCorpus("./data/corpus")
  TrainCorpus(training_corpus_loc)
  print >> sys.stderr, "Training Corpus"

pickle.dump(words_dictionary, wordDicFile) 
pickle.dump(kg_index, kgIndexFile) 
pickle.dump(bigramWords_dictionary,bigramWordDicFile)
print >> sys.stderr, "Training Finished"


