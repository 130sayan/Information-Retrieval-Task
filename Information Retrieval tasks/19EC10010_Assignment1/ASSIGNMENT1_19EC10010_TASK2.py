from bs4 import BeautifulSoup
from dateutil.parser import parse
import datetime
import os
import json
import nltk
getobj = os.getcwd()
getobjnew = getobj+"/ECT"
os.chdir(getobjnew)
internal = os.listdir(os.getcwd())
accu = 0

for direc in internal:

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
        file1.write("PRESENTATION ------------------------------------: \n")
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
