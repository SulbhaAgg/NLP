#Math imported for log calculations in sentencePerplexity and filePerplexity
import math

#This function is used to add <s></s> paddings and lowercase all words in the text file
def addPadding(fileName, newFile):
    with open(fileName, 'r') as f:
        with open(newFile, 'w') as w:
            for line in f.readlines():
                lineEdited = "<s> " + line.replace('\n', ' </s>\n')
                w.write(lineEdited.lower())

#This function counts the total # of tokens that aren't in the training file then gets the percentage over all tokens             
def unigramNotInTraining(fileName, unigram):
    tokens = 0
    tokensNotInTraining = 0
    for line in fileName:
        for word in line.split():
            tokens += 1
            if word not in unigram:
                tokensNotInTraining += 1
    print(fileName.name)
    print("Total # of words =", tokens)
    print("Words not in training data =", tokensNotInTraining)
    print("Percentage =", (tokensNotInTraining / tokens))
    print()

#This function is used to find the number of words that aren't in bigram file given the previous word in the file including the <s> </s> paddings then finds the percentages
def bigramNotInTraining(fileName, unigram, bigram):
    bigrams = 0
    bigramsNotInTraining = 0
    for line in fileName:
        previous = ""
        for word in line.split():
            if word not in unigram:
                word = "<unk>"
            if word == '<s>':
                previous = word
            elif previous + " " + word not in bigram:
                bigramsNotInTraining += 1
                bigrams += 1
                previous = word
            else:
                bigrams += 1
                previous = word
    print(fileName.name)
    print("Total # of words =", bigrams)
    print("Bigrams not in training data =", bigramsNotInTraining)
    print("Percentage =", (bigramsNotInTraining / bigrams))
    print()

#This function is used to figure out the smoothing and perplexity of a given sentence
def sentencePerplexityAndSmoothing(sentence, unigram, bigram, tokens):
    print(sentence)
    print()
    numWords = len(sentence.split())
    logProb = 0
    for word in sentence.lower().split():
        if word not in unigram:
            word = "<unk>"
        if word == '<s>':
            pass
        else:
            logProb += math.log2(unigram[word] / tokens)
            print("p(" + word + ") =", str(unigram[word]) + "/" + str(tokens))
    print()
    print("Unigram log probability =", logProb) #This calculates the sum of all tokens then does the log of that
    l = (1 / numWords) * logProb
    print("Unigram perplexity =", pow(2, -l)) #This is the formula used to find the perplexity (1/M (sigma log(x))
    print()
    sentenceProb = 1
    previous = ""
    for word in sentence.lower().split():
        if word not in unigram:
            word = "<unk>"
        if word == '<s>':
            previous = word
        elif previous + " " + word not in bigram:
            sentenceProb *= (0 / unigram[previous])
            #Shows the probability of each word
            print("p(" + word + "|" + previous + ") =", str(0) + "/" + str(unigram[previous]))
            previous = word
        else:
            sentenceProb *= (bigram[previous + " " + word] / unigram[previous])
            print("p(" + word + "|" + previous + ") =",
                  str(bigram[previous + " " + word]) + "/" + str(unigram[previous]))
            previous = word
    print()
    #This shows the bigram log probability and perplexity which is where you find the probability of a word given the previous word which is [(p(A) * p(B))/p(B)]
    if sentenceProb == 0:
        print("Bigram log probability =", str(0))
        print("Bigram perplexity =", "Undefined")
    else:
        print("Bigram log probability =", math.log2(sentenceProb))
        l = (1 / numWords) * math.log2(sentenceProb)
        print("Bigram perplexity =", pow(2, -l))
    print()
    logProb = 0
    for word in sentence.lower().split():
        if word not in unigram:
            word = "<unk>"
        if word == '<s>':
            previous = word
        elif previous + " " + word not in bigram:
            logProb += math.log2(1 / (unigram[previous] + len(unigram.items())))
            print("p(" + word + "|" + previous + ") =", str(1) + "/" + str(unigram[word] + len(unigram.items())))
            previous = word
        else:
            logProb += math.log2((bigram[previous + " " + word] + 1) / (unigram[previous] + len(unigram.items())))
            print("p(" + word + "|" + previous + ") =", str(bigram[previous + " " + word] + 1) + "/" + str(
                unigram[previous] + len(unigram.items())))
            previous = word
    print()
    print("Bigram smoothing log probability =", logProb)
    l = (1 / numWords) * logProb
    print("Bigram smoothing perplexity =", pow(2, -l)) #This is for the bigram perplexity but add one smoothing which is to take away from the probability mass from observed events and reassigning it to *unseen* events
    print()
    
#Notes for this function is almost the same as the sentencePerplexityAndSmoothing function
def filePerplexityAndSmoothing(fileName, unigram, bigram, tokens):
    numWords = 0
    numWordsBigram = 0
    numLines = 0
    numLinesDiscarded = 0
    for line in fileName:
        numLines += 1
        for word in line.split():
            numWords += 1
            numWordsBigram += 1
    fileName = open(fileName.name, 'r')
    totalUnigramLogProb = 0
    totalBigramLogProb = 0
    totalSmoothedBigramLogProb = 0
    for line in fileName:
        logProb = 0
        for word in line.split():
            if word not in unigram:
                word = "<unk>"
            if word == '<s>':
                pass
            else:
                logProb += math.log2(unigram[word] / tokens)
        totalUnigramLogProb += logProb
        sentenceProb = 1
        previous = ""
        for word in line.split():
            if word not in unigram:
                word = "<unk>"
            if word == '<s>':
                previous = word
            elif previous + " " + word not in bigram:
                sentenceProb *= (0 / unigram[previous])
                previous = word
            else:
                sentenceProb *= (bigram[previous + " " + word] / unigram[previous])
                previous = word
        if sentenceProb == 0:
            numWordsBigram -= len(line.split())
            numLinesDiscarded += 1
        else:
            totalBigramLogProb += math.log2(sentenceProb)
        logProb = 0
        for word in line.split():
            if word not in unigram:
                word = "<unk>"
            if word == '<s>':
                previous = word
            elif previous + " " + word not in bigram:
                logProb += math.log2(1 / (unigram[previous] + len(unigram.items())))
                previous = word
            else:
                logProb += math.log2((bigram[previous + " " + word] + 1) / (unigram[previous] + len(unigram.items())))
                previous = word
        totalSmoothedBigramLogProb += logProb
    print(fileName.name)
    print()
    l = (1 / numWords) * totalUnigramLogProb
    print("Unigram perplexity =", pow(2, -l))
    print()
    l = (1 / numWordsBigram) * totalBigramLogProb
    print("Bigram perplexity =", pow(2, -l))
    print(numLinesDiscarded, "of", numLines, "sentences had zero probability and were discarded")
    print()
    l = (1 / numWords) * totalSmoothedBigramLogProb
    print("Bigram smoothing perplexity =", pow(2, -l))
    print()

#This creates the padded files
addPadding('brown-train.txt', 'modified-brown-train.txt')
addPadding('brown-test.txt', 'modified-brown-test.txt')
addPadding('learner-test.txt', 'modified-learner-test.txt')

#Counts the keys to values of the dictionary 
brown_train_file = open('modified-brown-train.txt', 'r')
count = {}
for line in brown_train_file:
    for word in line.split():
        if word in count:
            count[word] += 1
        else:
            count[word] = 1
brown_train_file.close()

#This writes padding and unknown from modified-brown-training to a new file called unknown-brown-train.txt
currentFile = open('modified-brown-train.txt', 'r')
newFile = open('unknown-brown-train.txt', 'w')
for line in currentFile:
    for word in line.split():
        if count[word] == 1:
            newFile.write("<unk>" + " ")
        elif word == '</s>':
            newFile.write(word)
        else:
            newFile.write(word + " ")
    newFile.write("\n")
currentFile.close()
newFile.close()

#Opens the new file and counts the total # of unigrams and bigrams
textFile = open('unknown-brown-train.txt', 'r')
unigram = {}
bigram = {}
previous = ""
for line in textFile:
    for word in line.split():
        if word in unigram:
            unigram[word] += 1
        else:
            unigram[word] = 1
        if word == '<s>':
            previous = word
        elif previous + " " + word not in bigram:
            bigram[previous + " " + word] = 1
            previous = word
        else:
            bigram[previous + " " + word] += 1
            previous = word
unigramVocSize = len(unigram.keys())
textFile.close()

#Solutions start here
print("SOLUTION TO #1")
print("Unique words in training corpus =", unigramVocSize)
print()

#Get the number of tokens in the corpus
values = unigram.values()
tokens = 0
for val in values:
    tokens += val

print("SOLUTION TO #2")
print("Word tokens in training corpus =", tokens)
print()

print("SOLUTION TO #5/#6")
sentence1 = "<s> He was laughed off the screen . </s>"
sentence2 = "<s> There was no compulsion behind them . </s>"
sentence3 = "<s> I look forward to hearing your reply . </s>"
sentencePerplexityAndSmoothing(sentence1, unigram, bigram, tokens)
sentencePerplexityAndSmoothing(sentence2, unigram, bigram, tokens)
sentencePerplexityAndSmoothing(sentence3, unigram, bigram, tokens)

print("SOLUTION TO #7")
textFile1 = open('modified-brown-test.txt', 'r')
textFile2 = open('modified-learner-test.txt', 'r')
filePerplexityAndSmoothing(textFile1, unigram, bigram, tokens)
filePerplexityAndSmoothing(textFile2, unigram, bigram, tokens)
textFile1.close()
textFile2.close()

print("The modified-learner-test.txt file had higher values than the modified-brown-test.txt file, but the bigram perplexity with and without smoothing but had more than the unigram perplexity.")

#Opens modified-brown-train.txt file and counts the number of unigrams there are
unigram_file = open('modified-brown-train.txt', 'r')
unigram = {}
for line in unigram_file:
    for word in line.split():
        if word in unigram:
            unigram[word] += 1
        else:
            unigram[word] = 1
unigram_file.close()

print("SOLUTION TO #3")
print()
fileName1 = open('modified-brown-test.txt', 'r')
fileName2 = open('modified-learner-test.txt', 'r')
unigramNotInTraining(fileName1, unigram)
unigramNotInTraining(fileName2, unigram)
fileName1.close()
fileName2.close()

print("SOLUTION TO #4")
print()
File1 = open('modified-brown-test.txt', 'r')
File2 = open('modified-learner-test.txt', 'r')
bigramNotInTraining(File1, unigram, bigram)
bigramNotInTraining(File2, unigram, bigram)
File1.close()
File2.close()