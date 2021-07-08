import json
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
import string
#imports all the necessary packages

inv_ind = {}

getdirec = os.getcwd()
newdirec = getdirec+"/ECTText"
#gets the ECTText directory
os.chdir(newdirec)
directory = os.listdir(os.getcwd())
accu = -1

lemmas = WordNetLemmatizer()

for files in directory:
#Loops over all the files in the ECTText directory
  with open(files) as fp:
     accu = accu + 1
     makefile = fp.read()
     collection = word_tokenize(makefile)

     newcol = str.maketrans('','','\t')
     collection = [word.translate(newcol) for word in collection]
     pun = (string.punctuation).replace("'","")
     table = str.maketrans('', '' ,pun)
     #removes the punctuation marks
     stop_words = set(stopwords.words('english'))
     collection = [word for word in collection if word not in stop_words]
     stripped_words = [word.translate(table) for word in collection]
     collection = [word for word in stripped_words if word]
     collection = [word.lower() for word in collection]
     collection = [lemmas.lemmatize(word) for word in collection]


     for position,strings in enumerate(collection):
        if strings in inv_ind:
            inv_ind[strings][0]=inv_ind[strings][0]+1
            if accu in inv_ind[strings][1]:
             inv_ind[strings][1][accu].append(position)
            else:
             inv_ind[strings][1][accu]=[position]
        else:
            inv_ind[strings]=[]
            inv_ind[strings].append(1)
            inv_ind[strings].append({})
            inv_ind[strings][1][accu]=[position]

address=getdirec
#Gets the address folder location
os.chdir(address)
dictionary = open("inverted_list.json","w")
json.dump(inv_ind,dictionary)

dictionary.close()
os.chdir(newdirec)

        
