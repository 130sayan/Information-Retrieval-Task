import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
from dateutil.parser import parse
import json
import datetime
import string
import numpy as np
import sys
from collections import Counter
from math import log10
import pickle5 as pickle
from numpy import linalg as LA
import itertools
# Getting the current working directory
getobj = os.getcwd()
getobjnew = getobj+"/Dataset"
os.chdir(getobjnew)
internal = os.listdir(os.getcwd())
accu = 0
# Running a loop over all html files and converting them to their corresponding text files
for direc in internal:
    try:
        with open(direc) as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            obj1 = soup.find(id="a-body")
            cnt = soup.find_all(class_="p_count")
            nump = len(cnt)+2
            strar = []
            index = []
            ctr = 0
            indd = -1
            for i in range(1, nump):
                objs = obj1.find_all(class_="p p%d" % i)
                for eachobj in objs:
                    temp = str(eachobj)
                    strar.append(temp)
                    if "strong" in temp:
                        index.append(ctr)
                        if "Question-and-Answer" in temp:
                            indd = ctr
                    ctr = ctr+1
            objs = obj1.find_all(class_="p p1")
            company_participants = []
            conference_call_participants = []
            l1 = index[0]
            l2 = index[1]
            l3 = index[2]
            findate = ""
            months = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
            datefind = obj1.find_all(class_="p p1")
            for objj in datefind:
                tempstr = str(objj)
                flag = 0
                for allm in months:
                    if allm in tempstr:
                        flag = 1
                        inddd = -1
                        ccc = 0
                        for i in range(0, len(tempstr)-4):
                            tempword = tempstr[i:i+4]
                            if tempword == "2020":
                                inddd = ccc
                                break
                            ccc = ccc+1
                        findate = allm
                        for i in range(inddd-1, inddd-5, -1):
                            findate = tempstr[i] + findate
                if flag == 1:
                    break

            for i in range(l1+1, l2):

                num = 0
                for ch in strar[i]:
                    if ch == '>':
                        ind1 = num
                    if ch == '-':
                        ind2 = num
                        break
                    num = num+1
                ss = str(strar[i])
                temp = ss[ind1+1:ind2-1]
                company_participants.append(temp)
            company_participants.append("Operator")
            for i in range(l2+1, l3):

                num = 0
                for ch in strar[i]:
                    if ch == '>':
                        ind1 = num
                    if ch == '-':
                        ind2 = num
                        break
                    num = num+1
                ss = str(strar[i])
                temp = ss[ind1+1:ind2-1]
                conference_call_participants.append(temp)

            allobj = soup.find(id="a-body")

            di = {}
            cnt1 = 0
            cnt2 = 0
            spkr = []
            remarks = []
            presspeaker = []
            pressremarks = []
            lastname = ""
            for i in range(l3, indd):
                if "strong" in strar[i]:
                    for allstr in company_participants:
                        if allstr in strar[i]:
                            lastname = allstr
                            break
                    for allstr in conference_call_participants:
                        if allstr in strar[i]:
                            lastname = allstr
                            break
                else:
                    rem = ""
                    fgl = 0
                    for ch in strar[i]:
                        if fgl == 1:
                            if ch == '<':
                                break
                            rem = rem+ch
                        if ch == '>':
                            fgl = 1
                    presspeaker.append(lastname)
                    pressremarks.append(rem)

            for num in range(1, nump):
                tt = soup.find_all(class_="p p%d" % num)
                if num == 1:
                    flag = 0
                else:
                    flag = 1

                for eachobj in tt:

                    string = str(eachobj)
                    if flag == 1:
                        flg = 0
                        ctr = 0
                        if "strong" in string:
                            for allstr in company_participants:
                                if allstr in string:
                                    flg = 1
                                    break
                                ctr = ctr + 1
                            if flg == 1:
                                lastname = company_participants[ctr]
                                continue
                            ctr = 0
                            for allstr in conference_call_participants:
                                if allstr in string:
                                    flg = 1
                                    break
                                ctr = ctr + 1
                            if flg == 1:
                                lastname = conference_call_participants[ctr]
                                continue
                        else:
                            ind1 = -1
                            ind2 = -1
                            ind = 0
                            for ch in string:
                                if ch == '>':
                                    ind1 = ind
                                if ch == '/':
                                    ind2 = ind
                                    break
                                ind = ind + 1
                            tempstring = string[ind1+1:ind2-1]
                            spkr.append(lastname)
                            remarks.append(tempstring)

                    if "question-answer-session" in string:
                        flag = 1

            findate = findate + " 2020 "
            di['Date'] = findate
            di['Company_participants'] = company_participants
            di['Conference_call_participants'] = conference_call_participants
            di['PresentationSpeaker'] = presspeaker
            di['PresentationRemarks'] = pressremarks
            di['QnASpeaker'] = spkr
            di['QnARemarks'] = remarks
            address = getobj+"/ECTNestedDict"
            os.chdir(address)
            diction = open("Doc%d.json" % accu, "w")
            json.dump(di, diction)
            diction.close()
            address = getobj+"/ECTText"
            os.chdir(address)
            file1 = open("%s.txt" % direc, "w+")
            file1.write("DATE : \n")
            file1.write(findate)
            file1.write("\n")
            file1.write(
                "COMPANY PARTICIPANTS ------------------------------------------: \n")
            for sss in company_participants:
                if sss != "Operator":
                    file1.write(sss+"\n")
            file1.write(
                "CONFERENCE CALL PARTICIPANTS --------------------------------------: \n")
            for sss in conference_call_participants:
                file1.write(sss+"\n")
            file1.write(
                "PRESENTATION ------------------------------------: \n")
            x = len(presspeaker)
            for i in range(0, x):
                file1.write("Speaker : "+presspeaker[i])
                file1.write("\n")
                file1.write("Remark : "+pressremarks[i])
                file1.write("\n")
            file1.write(
                "QUESTION AND ANSWER SESSION ----------------------------------: \n")
            file1.write("\n")
            x = len(spkr)
            for i in range(0, x):
                file1.write("Speaker : "+spkr[i])
                file1.write("\n")
                file1.write("Remark : "+remarks[i])
                file1.write("\n")
            file1.close()
            os.chdir(getobjnew)
        accu = accu+1
    except:
        continue

num = 0
lemma = WordNetLemmatizer()
docdict = {}
termfreq = {}
os.chdir(getobj)
folder = os.getcwd()
address = folder + "/ECTText"
# Now we switch to the text files folder
filewrite = open('RESULTS2_19EC10010.txt', 'w+', encoding="utf-8")
os.chdir(address)
docs = os.listdir(os.getcwd())
stoppers = set(stopwords.words('english'))
# We run a loop over all documents
for document in docs:
    num += 1
    print(str(document))
    with open(document, encoding="utf-8") as newfile:

        content = newfile.read()
        listwords = word_tokenize(content)
        listwords = [word.lower() for word in listwords]
        punc_table = str.maketrans('', '', '\t')
        listwords = [word.translate(punc_table) for word in listwords]
        listwords = [word for word in listwords if word not in stoppers]
        listwords = [lemma.lemmatize(word) for word in listwords]

        for term in listwords:

            if term in docdict:
                if str(document) not in docdict[term]:
                    docdict[term].append(str(document))
            else:
                docdict[term] = []
                docdict[term].append(str(document))

            if term in termfreq:
                if document in termfreq[term]:
                    termfreq[term][document] += 1
                else:
                    termfreq[term][document] = 1

            else:
                termfreq[term] = {}
                termfreq[term][document] = 1

ChampionListLocal = {}
ChampionListGlobal = {}
tf = {}
idf = {}

tf = termfreq
for word in termfreq:
    print(str(word))
    for document in termfreq[word]:
        tf[word][document] = log10(1+termfreq[word][document])

for word in docdict:
    print(str(word))
    idf[word] = log10(num/len(docdict[word]))

InvertedPositionalIndex = {}
# Building the Inverted Positional Index
for word in docdict:
    InvertedPositionalIndex[(word, idf[word])] = termfreq[word]

l = len(InvertedPositionalIndex)
os.chdir(folder)
file1 = open('StaticQualityScore.pkl', 'rb')
static_score = pickle.load(file1)
file2 = open('Leaders.pkl', 'rb')
file3 = open(sys.argv[1], 'r', encoding="utf-8")
leaders = pickle.load(file2)
queries = file3.readlines()
v = {}
ctr = 0
for word, idff in InvertedPositionalIndex:
    print(str(word))
    ChampionListLocal[word] = {lis: ele for lis, ele in sorted(InvertedPositionalIndex[(word, idff)].items(), key=lambda item: item[1], reverse=True)}
    ChampionListLocal[word] = dict(itertools.islice(ChampionListLocal[word].items(), 50))
    tf_idf = {}
    for term in InvertedPositionalIndex[(word, idff)]:
        tf_idf[term] = InvertedPositionalIndex[(word, idff)][term]*idff + static_score[int(term[:-9])]
        if term in v:
            v[term][ctr] = InvertedPositionalIndex[(word, idff)][term]*idff
        else:
            v[term] = [0]*l
            v[term][ctr] = InvertedPositionalIndex[(word, idff)][term]*idff

    ChampionListGlobal[word] = {lis: ele for lis, ele in sorted(tf_idf.items(), key=lambda item: item[1], reverse=True)}
    ChampionListLocal[word] = dict(itertools.islice(ChampionListGlobal[word].items(), 50))
    ctr += 1
for query in queries:

    ques = query.strip()
    ques = np.char.lower(ques)
    words = word_tokenize(str(ques))
    print(words)
    print("\n")
    temp = ""
    for word in words:
        if word not in stoppers and len(word) > 1:
            temp = temp + " " + word

    finalq = temp
    finalq = np.char.replace(finalq, ',', '')
    finalq = np.char.replace(finalq, ",", "")
    qline = word_tokenize(str(finalq))
    qline = [lemma.lemmatize(word) for word in qline]

    qv = [0]*l
    ctr = 0
    for word, idff in InvertedPositionalIndex:
        if word in words:
            qv[ctr] = idff
        ctr += 1

    qv_norm = LA.norm(qv)
    sc1 = {}
    sc2 = {}
    sc3 = {}
    sc4 = {}
# Building the Champion Local List and the Champion global List
    for document in v:
        print(str(document))
        print("\n")
        v_norm = LA.norm(v[document])
        sc1[document] = np.dot(v[document], qv)/(v_norm*qv_norm)

    for term in words:
        print(term)
        print("A\n")
        if term in ChampionListLocal:
            for document in ChampionListLocal[term]:
                v_norm = LA.norm(v[document])
                sc2[document] = np.dot(v[document], qv)/(v_norm*qv_norm)
        if term in ChampionListGlobal:
            for document in ChampionListGlobal[term]:
                v_norm = LA.norm(v[document])
                sc3[document] = np.dot(v[document], qv)/(v_norm*qv_norm)
    curr_lead = ""
    curr_max = - 1
    for document in leaders:
        print(str(document))
        print("B\n")
        curr_doc = (str)(document)+".html.txt"
        v_norm = LA.norm(v[curr_doc])
        temp = np.dot(v[curr_doc], qv)/(v_norm*qv_norm)
        if temp >= curr_max:
            curr_max = temp
            curr_lead = curr_doc

    normleader = LA.norm(v[curr_lead])
    fol = []
    fol.append(curr_lead)
# Creating the follower list
    for document in v:
        print(str(document))
        print("C\n")
        if document == curr_lead:
            continue
        document_norm = LA.norm(v[document])
        var1 = np.dot(v[document], v[curr_lead])/(document_norm*normleader)
        flag = 0
        for newdoc in leaders:
            docname = str(newdoc)+".html.txt"
            if docname == curr_lead:
                continue
            newdoc_norm = LA.norm(v[docname])
            var2 = np.dot(v[document], v[docname])/(newdoc_norm*document_norm)
            if var2>var1:
                flag = 1
                break
        if flag == 0:
            fol.append(document)

    sc4 = {}
    for document in fol:
        print(str(document))
        print("\n")
        doc_norm = LA.norm(v[document])
        sc4[document] = np.dot(v[document], qv)/(doc_norm*qv_norm)
# Forming the sc1, sc2, sc3 , sc4
    sc1 = {k: v for k, v in sorted(sc1.items(), key=lambda item: item[1], reverse=True)}
    sc1 = dict(itertools.islice(sc1.items(), 10))
    sc2 = {k: v for k, v in sorted(sc2.items(), key=lambda item: item[1], reverse=True)}
    sc2 = dict(itertools.islice(sc2.items(), 10))
    sc3 = {k: v for k, v in sorted(sc3.items(), key=lambda item: item[1], reverse=True)}
    sc3 = dict(itertools.islice(sc3.items(), 10))
    sc4 = {k: v for k, v in sorted(sc4.items(), key=lambda item: item[1], reverse=True)}
    sc4 = dict(itertools.islice(sc4.items(), 10))

    filewrite.write(query.strip())
    filewrite.write("\n")
    c = 0
    for i in sc1:
        if c == 1:
            filewrite.write(",<"+str(i)+","+str(sc1[i])+">")
        else:
            filewrite.write("<"+str(i)+","+str(sc1[i])+">")
            c = 1
    filewrite.write("\n")

    c = 0
    for i in sc2:
        if c == 1:
            filewrite.write(",<"+str(i)+","+str(sc2[i])+">")
        else:
            filewrite.write("<"+str(i)+","+str(sc2[i])+">")
            c = 1
    filewrite.write("\n")

    c = 0
    for i in sc3:
        if c == 1:
            filewrite.write(",<"+str(i)+","+str(sc3[i])+">")
        else:
            filewrite.write("<"+str(i)+","+str(sc3[i])+">")
            c = 1
    filewrite.write("\n")

    c = 0
    for i in sc4:
        if c == 1:
            filewrite.write(",<"+str(i)+","+str(sc4[i])+">")
        else:
            filewrite.write("<"+str(i)+","+str(sc4[i])+">")
            c = 1
    filewrite.write("\n")
