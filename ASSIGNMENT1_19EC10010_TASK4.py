import json
import os
import sys
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
#All necessary packages have been imported
filename = str(sys.argv[1])
#To get the query.txt file
results = open("RESULTS1_19EC10010.txt", "w+")

with open(filename, 'r') as fp:
    queries = fp.readlines()
#Reads the queries one by one
    cnt = 0
    for words in queries:
        cnt = cnt+1
        words = words.strip()
        with open('inverted_list.json', 'r') as fpdash:
            dictionary = json.load(fpdash)
            if(words.startswith("*")):
                words = queries[1:]
                for word in dictionary:
#Iterates over all the words in the dictionary
                    if (word.endswith(words)):
                        results.write(word+":")
                        curr = 0
                        for coor1 in dictionary[word][1]:
                            for coor2 in dictionary[word][1][coor1]:
                                if(curr > 0):
                                    results.write(",")
                                results.write("<"+str(coor1) +
                                              ","+str(coor2)+">")
                                curr = curr+1
                        results.write(";")
#Handles the case when the word begins with a *
            elif (words.endswith("*")):
                words = words[0:len(words)-1]
                for word in dictionary:
                    if (word.startswith(words)):
                        results.write(word+":")
                        curr = 0
                        for coor1 in dictionary[word][1]:
                            for coor2 in dictionary[word][1][coor1]:
                                if(curr > 0):
                                    results.write(",")
                                results.write("<"+str(coor1) +
                                              ","+str(coor2)+">")
                                curr = curr+1
                        results.write(";")
#Handles the case when the word ends with *

            else:
                posn = 0
                begin = ""
                end = ""
                for ch in words:
                    if ch == '*':
                        break
                    posn = posn+1
                begin = words[0:posn]
                end = words[posn+1:len(words)]
                for word in dictionary:
                    if ((word.startswith(begin))and(word.endswith(end))):
                        results.write(word+":")
                        curr = 0
                        for coor1 in dictionary[word][1]:
                            for coor2 in dictionary[word][1][coor1]:
                                if(curr > 0):
                                    results.write(",")
                                results.write("<"+str(coor1) +
                                              ","+str(coor2)+">")
                                curr = curr+1
                        results.write(";")
#Handles all other cases

        results.write("\n")
