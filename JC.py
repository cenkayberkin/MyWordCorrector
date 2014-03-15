from decimal import getcontext, Decimal

getcontext().prec = 4

""" |X intersect Y| / |X U Y| """

s1= "the way to the school is long and hard when walking in the rain"
s2 = "the rain has not stopped in days and the school has closed"
stopWords = "the to is and in has not"
query = "school closed rain"

setStopWords = set(stopWords.split(" "))

set1 = set(s1.split(" "))
set1 = set1.difference(setStopWords)

set2 = set(s2.split(" "))
set2 = set2.difference(setStopWords)

setquery = set(query.split(" "))

union = len(setquery.union(set2))
intersection = len(setquery.intersection(set2))

result =  Decimal(intersection) /  Decimal(union)
print result
#s1 icin 0.1538
#s2 icin 0.3

#stop word leri cikarinca
#s1 0.25
#s2 0.6


