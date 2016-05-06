import random 
from numpy import arange
import os,bz2
from sets import Set
import operator

threshRes = 0
threshResEsp = 0
threshResEng = 0
threshResViet = 0
threshResHin = 0
threshResFar = 0
threshAdd = -1
scale = 100 * 1000

def getSize(trigrams):
    size = 0
    for tri in trigrams:
        size += trigrams[tri]
    return 1.0 * size

def getTrigrams(words,trigrams = 0):
    if (trigrams == 0):
        trigrams = dict()
    for word in words:
        word = ("**" + word + "**").lower()
        for i in xrange(len(word) - 2):
            tri = word[i:i+3]
            if tri in trigrams:
                trigrams[tri] += 1
            else:
                trigrams[tri] = 1
    return trigrams

def getCounts(filename,counts=0):
    if counts == 0:
        counts = dict()
    L = []
    for i in xrange(100):
        if (i % 100 < 10):
            add = '0' + str(i % 100)
        else:
            add = str(i % 100)
        f = open(filename + add)
        for line in f:
            if line[0] == '<':
                continue
            line = line.split()
            for word in line:
                word = word.strip('"')
                word = word.strip('.')
                word = word.strip(',')
                word = word.lower()
                if word in counts:
                    counts[word] +=1
                else:
                    counts[word] = 1
    
    # words = sorted(counts.items(), key=operator.itemgetter(1),reverse=True)
    # print words[:1000]
    return counts

def getWords(filename):
    l = []
    for fi in filename:
        words = getCounts(fi)
        words = sorted(words.items(), key=operator.itemgetter(1),reverse=True)
        for word,_ in words:
            l.append(word.decode('utf-8'))
    return l

def flipWord(word):
    if (len(word) <= 1):
        return word
    p1 = random.randrange(0,len(word) - 1)
    word = list(word)
    p2 = p1 + 1
    l = word[:p1]
    if (p2 < len(word)):
        r = word[p1+2:]
    else:
        r = ""
    flipped = ''.join(l) + word[p2] + word[p1] + ''.join(r)
    return flipped

def getMisspell(rights):
    s = Set()
    for word in rights:
        flipped = flipWord(word)
        s.add(flipped)
    return list(s)

def getCorrect(filenames,train):
    l = []
    words = dict()
    for filename in filenames:
        words0 = getCounts(filename,words)
    words = sorted(words0.items(), key=operator.itemgetter(1),reverse=True)

    for (word,_) in words:
        if word not in train:
            l.append(word.decode('utf-8'))
    return l

def test(trigrams,testTri):
    # print testTri
    for tri in testTri:
        if tri in trigrams:
            minTri = trigrams[tri]
        else:
            minTri = 0
        break
    for tri in testTri:
        if tri in trigrams:
            minTri = min(minTri,trigrams[tri])

        else:
            minTri = 0
    return minTri

def updateTrigrams(rnd,trigrams,rights,wrongs):
    numRights = (rnd) * 90
    numWrongs = (rnd) * 10
    global threshAdd
    for i in xrange(rnd):

        rightIndex = i*90
        wrongIndex = i*10
        right90 = rights[rightIndex:rightIndex+90]
        wrong10 = wrongs[wrongIndex:wrongIndex+10]

        for word in set(right90 + wrong10):
            tri = getTrigrams(set([word]))
            minTri = test(trigrams,tri)
            size = getSize(trigrams)
            perc = minTri/size * scale
            if (perc > threshAdd):
                trigrams = getTrigrams(set([word]), trigrams)

    return trigrams,wrongs[numWrongs:],rights[numRights:]


def doTest(trigrams,tests,threshRes):
    s = Set()
    for word in tests:
        tri = getTrigrams(set([word]))
        minTri = test(trigrams,tri)
        size = getSize(trigrams)
        perc = minTri/size * scale

        if (perc > threshRes):
            s.add((word,True))
        elif (perc <= threshRes):
            s.add((word,False))
    return s


def main(rnd,filenames,thresh):
    allWords = getWords(filenames)
    train = allWords[:1000]


    rights = allWords[1000:]
    wrongs = getMisspell(rights)
    trigrams = getTrigrams(train)
    if rnd > 0:
        trigrams,wrongs,rights = updateTrigrams(rnd,trigrams,rights,wrongs)
    size = getSize(trigrams)

    if (size == 0):
        return "no words"
    #True means correctly spelled, False means misspelling
    results = doTest(trigrams,rights[:90] + wrongs[:10],thresh)
    return results,rights[:90],wrongs[:10]


# print "eng"
for rnd in xrange(0,200,5):
    print 'rnd',rnd
# rnd = 450

# for threshRes in xrange(10,11):
#     print "thresh",threshRes
    results,rights,wrongs = main(rnd,['wiki/texts/eng/AA/wiki_',
        'wiki/texts/eng/AB/wiki_'
        ,'wiki/texts/eng/AC/wiki_',
            'wiki/texts/eng/AD/wiki_','wiki/texts/eng/AE/wiki_','wiki/texts/eng/AF/wiki_',
            'wiki/texts/eng/AG/wiki_','wiki/texts/eng/AH/wiki_','wiki/texts/eng/AI/wiki_',
            'wiki/texts/eng/AJ/wiki_','wiki/texts/eng/AK/wiki_','wiki/texts/eng/AL/wiki_'
            ,'wiki/texts/eng/AM/wiki_','wiki/texts/eng/AN/wiki_','wiki/texts/eng/AO/wiki_'
            ,'wiki/texts/eng/AP/wiki_','wiki/texts/eng/AQ/wiki_','wiki/texts/eng/AR/wiki_'
            ,'wiki/texts/eng/AS/wiki_','wiki/texts/eng/AT/wiki_','wiki/texts/eng/AU/wiki_'
            ,'wiki/texts/eng/AV/wiki_','wiki/texts/eng/AW/wiki_','wiki/texts/eng/AX/wiki_'
            ,'wiki/texts/eng/AY/wiki_','wiki/texts/eng/AZ/wiki_','wiki/texts/eng/BA/wiki_',
            'wiki/texts/eng/BB/wiki_']


    ,threshResEng)
    # results,rights,wrongs = 
# main(rnd,['wiki/texts/esp/AA/wiki_',
#     'wiki/texts/esp/AB/wiki_'
#     ,'wiki/texts/esp/AC/wiki_',
#         'wiki/texts/esp/AD/wiki_','wiki/texts/esp/AE/wiki_','wiki/texts/esp/AF/wiki_',
#         'wiki/texts/esp/AG/wiki_','wiki/texts/esp/AH/wiki_','wiki/texts/esp/AI/wiki_',
#         'wiki/texts/esp/AJ/wiki_','wiki/texts/esp/AK/wiki_','wiki/texts/esp/AL/wiki_'
#         ,'wiki/texts/esp/AM/wiki_','wiki/texts/esp/AN/wiki_','wiki/texts/esp/AO/wiki_'
#         ,'wiki/texts/esp/AP/wiki_','wiki/texts/esp/AQ/wiki_','wiki/texts/esp/AR/wiki_'
#         ,'wiki/texts/esp/AS/wiki_','wiki/texts/esp/AT/wiki_','wiki/texts/esp/AU/wiki_'
#         ,'wiki/texts/esp/AV/wiki_','wiki/texts/esp/AW/wiki_','wiki/texts/esp/AX/wiki_'
#         ,'wiki/texts/esp/AY/wiki_','wiki/texts/esp/AZ/wiki_','wiki/texts/esp/BA/wiki_',
#         'wiki/texts/esp/BB/wiki_']

#     ,threshResEsp)
# results,rights,wrongs = main(rnd,['wiki/texts/viet/AA/wiki_',
#         'wiki/texts/viet/AB/wiki_'
#         ,'wiki/texts/viet/AC/wiki_',
#             'wiki/texts/viet/AD/wiki_','wiki/texts/viet/AE/wiki_','wiki/texts/viet/AF/wiki_',
#             'wiki/texts/viet/AG/wiki_','wiki/texts/viet/AH/wiki_','wiki/texts/viet/AI/wiki_',
#             'wiki/texts/viet/AJ/wiki_','wiki/texts/viet/AK/wiki_','wiki/texts/viet/AL/wiki_'
#             ,'wiki/texts/viet/AM/wiki_','wiki/texts/viet/AN/wiki_','wiki/texts/viet/AO/wiki_'
#             ,'wiki/texts/viet/AP/wiki_','wiki/texts/viet/AQ/wiki_','wiki/texts/viet/AR/wiki_'
#             ,'wiki/texts/viet/AS/wiki_','wiki/texts/viet/AT/wiki_','wiki/texts/viet/AU/wiki_'
#             ,'wiki/texts/viet/AV/wiki_','wiki/texts/viet/AW/wiki_','wiki/texts/viet/AX/wiki_'
#             ,'wiki/texts/viet/AY/wiki_','wiki/texts/viet/AZ/wiki_','wiki/texts/viet/BA/wiki_',
#             'wiki/texts/viet/BB/wiki_']
#             ,threshResViet)
# results,rights,wrongs = main(rnd,
#             ['wiki/texts/hindi/AA/wiki_',
#         'wiki/texts/hindi/AB/wiki_'
#         ,'wiki/texts/hindi/AC/wiki_',
#             'wiki/texts/hindi/AD/wiki_','wiki/texts/hindi/AE/wiki_','wiki/texts/hindi/AF/wiki_',
#             'wiki/texts/hindi/AG/wiki_','wiki/texts/hindi/AH/wiki_','wiki/texts/hindi/AI/wiki_',
#             'wiki/texts/hindi/AJ/wiki_','wiki/texts/hindi/AK/wiki_','wiki/texts/hindi/AL/wiki_'
#             ,'wiki/texts/hindi/AM/wiki_']
#             ,threshResHin)
# results,rights,wrongs = main(rnd,
#         ['wiki/texts/farsi/AA/wiki_',
#         'wiki/texts/farsi/AB/wiki_'
#         ,'wiki/texts/farsi/AC/wiki_',
#             'wiki/texts/farsi/AD/wiki_','wiki/texts/farsi/AE/wiki_','wiki/texts/farsi/AF/wiki_',
#             'wiki/texts/farsi/AG/wiki_','wiki/texts/farsi/AH/wiki_','wiki/texts/farsi/AI/wiki_',
#             'wiki/texts/farsi/AJ/wiki_','wiki/texts/farsi/AK/wiki_','wiki/texts/farsi/AL/wiki_'
#             ,'wiki/texts/farsi/AM/wiki_','wiki/texts/farsi/AN/wiki_','wiki/texts/farsi/AO/wiki_'
#             ,'wiki/texts/farsi/AP/wiki_','wiki/texts/farsi/AQ/wiki_','wiki/texts/farsi/AR/wiki_'
#             ,'wiki/texts/farsi/AS/wiki_','wiki/texts/farsi/AT/wiki_','wiki/texts/farsi/AU/wiki_'
#             ,'wiki/texts/farsi/AV/wiki_','wiki/texts/farsi/AW/wiki_','wiki/texts/farsi/AX/wiki_'
#             ]
#         ,threshResFar)
    accur = 0
    accuw = 0
    for (word,b) in results:
        if b == True:
            if word in rights:
                # print word
                accur+=1
            # else:
            #     print "wrong", word.encode('utf-8')
        if b == False:
            if word in wrongs:
                accuw+=1
            # else:
            #     print "right", word.encode('utf-8')
    print accur
    print accuw





