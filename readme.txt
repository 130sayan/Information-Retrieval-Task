TASK 2(Building Corpus):

On running the code task2.py it traverses the html files from ECT folder one by one and processes them to get text files and stores them in ECTText in the required format. It also creates json files for dictionaries in ECTNestedDict folder. Both of these have all the text information concatenated.

TASK 3(Building Index):

On running task3.py it traverses each text file stored in ECTText folder and builds the positional indices for it. This continues for all the text files unless the final positional list is obtained. The entire dictionary is then stored in a .json format file (dumped into) which is created in the original directory.

TASK 4(Answering Wild Card Queries):

On running task4.py it reads the json dictionary file and the query.txt file present in the directory. For each query word we perform a linear search on the posting lists. Whenever a word obeying the given conditions is obtained we write its positional index array into the final results text file which gets created in the original directory. The format given has been followed.
