import string

wList = "humpty dumpty billy sat in the hall".split(" ")

s = "$h,hu,mp,pt,ty,y$,$d,du,um,mp,pt,ty,y$,$b,bi,il,ll,ly,y$,$s,sa,at,t$,$i,in,n$,$t,th,he,e$,$h,ha,al,ll,l$"
bList = s.split(",")

bDic = {}

def InsertDic(blist):
  for b in blist:
    if b not in bDic:
      bDic[b] = []
    
def InsertWordsToDic(words):
  for word in words:
    for b in bDic.keys():
      if str(b) in word:
        bDic[b].append(word)
      elif "$" == b[0]:
        startString = b.replace("$","")
        if word.startswith(startString):
          bDic[b].append(word)
      elif "$" == b[-1]:
        endString = b.replace("$","")
        if word.endswith(endString):
          bDic[b].append(word)
        
InsertDic(bList)
InsertWordsToDic(wList)


#print bDic.keys()
#print len(bDic.keys())
#print "\n"
#print bDic.values()

count = 0

for i in bDic.keys():
  print i + " = " + str(bDic[i])


for i in bDic.keys():
  count += len(bDic[i])  

print count