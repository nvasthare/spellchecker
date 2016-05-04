
from sets import Set
import string
import os
from flask import Flask,request
app = Flask(__name__)

threshRes = 10
threshAdd = 20
scale = 100 * 1000

words = []
dictionary = Set()
prevLang = ''
prevWords = ''

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

def getWords(filename):
    l = []
    mydir = os.path.dirname(__file__)
    filepath = os.path.join(mydir,filename)
    f2 = open(filepath)
    for line in f2:
        line = line.strip()
        line = line.split()
        if len(line) == 0:
        	continue
        word = line[0]
        word = word.lower()
        l.append(word.strip())
        if len(l) > 1000:
            break
    f2.close()
    return l

def test(trigrams,testTri):
    for tri in testTri:
        if tri in trigrams:
            minTri = trigrams[tri]
        else:
            minTri = 0
        break
    for tri in testTri:
        if tri in trigrams:
            minTri = min(minTri,trigrams[tri])
            if minTri == trigrams[tri]:
                mtri = tri
        else:
            minTri = 0
            mtri = tri
    return minTri,mtri

def doTest(word):
    global trigrams
    global dictionary
    word = word.strip(',')
    word = word.strip('?')
    word = word.strip('!')
    word = word.strip(';')
    word = word.strip('.')
    if word in dictionary:
    	return 0
    if word in string.punctuation:
    	return 0
    s = Set()
    i = 0
    tri = getTrigrams(set([word]))
    minTri,mtri = test(trigrams,tri)
    size = getSize(trigrams)
    perc = minTri/size * scale
    if perc > threshAdd:
    	trigrams = getTrigrams(set([word]),trigrams)
    if (perc > threshRes):
        return 0
    else:
        return -1
       
def addToDict(sentence):
	global dictionary
	global trigrams
	sentence = sentence.split()
	for word in sentence:
		word = word.strip('.')
		word = word.lower()
		if word not in dictionary:
			trigrams = getTrigrams(set([word]),trigrams)
			dictionary.add(word)

def doReset():
	global trigrams
	global train
	global dictionary
	global words
	trigrams = getTrigrams(train)
	dictionary = Set()
	for word in words:
		dictionary.add(word.lower())

@app.route("/",methods=["GET","POST"])
def main():
	global train
	global trigrams
	global words
	global dictionary
	global prevLang
	global prevWords
	print "prev",prevLang,prevWords
	word = request.form['params']
	if word == "**reset**":
	    doReset()
	    return str(0)
	lang = request.form['l']
	word = word.strip()
	numWords = request.form['w']
	if numWords == '1000' and (prevLang != lang or prevWords != numWords):
		print "in if"
		dictionary = Set()
		if lang == 'eng':
			words = getWords('engtrain.txt')
			train = Set(words[:1000])
			trigrams = getTrigrams(train)
			for w in words:
				dictionary.add(w.lower())

		elif lang == 'esp':
			words = getWords('esptrain.txt')
			words = [w.decode('utf-8') for w in words]
			train = Set(words[:1000])
			trigrams = getTrigrams(train)
			for w in words:
				dictionary.add(w)

		elif lang == 'viet':
			words = getWords('viettrain.txt')
			words = [w.decode('utf-8') for w in words]
			train = Set(words[:1000])
			trigrams = getTrigrams(train)
			for w in words:
				dictionary.add(w)

		elif lang == 'hin':
			words = getWords('hintrain.txt')
			words = [w.decode('utf-8') for w in words]
			train = Set(words[:1000])
			trigrams = getTrigrams(train)
			for w in words:
				dictionary.add(w)

		elif lang == 'far':
			words = getWords('fartrain.txt')
			words = [w.decode('utf-8') for w in words]
			train = Set(words[:1000])
			trigrams = getTrigrams(train)
			for w in words:
				dictionary.add(w)

	elif numWords == '100'and (prevLang != lang or prevWords != numWords):
		print "in if"
		dictionary = Set()
		if lang == 'eng':
			words = getWords('engtrain.txt')
			train = Set(words[:100])
			trigrams = getTrigrams(train)
			for w in words:
				dictionary.add(w.lower())

		elif lang == 'esp':
			# print 'spanish'
			words = getWords('esptrain.txt')
			# print repr(words[25])
			words = [w.decode('utf-8') for w in words]
			train = Set(words[:100])
			trigrams = getTrigrams(train)
			for w in words:
				dictionary.add(w)

		elif lang == 'viet':
			words = getWords('viettrain.txt')
			words = [w.decode('utf-8') for w in words]
			train = Set(words[:100])
			trigrams = getTrigrams(train)
			for w in words:
				dictionary.add(w)

		elif lang == 'hin':
			words = getWords('hintrain.txt')
			words = [w.decode('utf-8') for w in words]
			train = Set(words[:100])
			trigrams = getTrigrams(train)
			for w in words:
				dictionary.add(w)

		elif lang == 'far':
			words = getWords('fartrain.txt')
			words = [w.decode('utf-8') for w in words]
			train = Set(words[:100])
			trigrams = getTrigrams(train)
			for w in words:
				dictionary.add(w)
	prevLang = lang
	prevWords = numWords
	word = word.strip()
	if len(word.split()) > 1 and word[len(word)-1] == '.':
		addToDict(word)
		return str(0)
	elif len(word.split()) > 1:
		return str(0)
	word = word.lower()
	result = doTest(word)
	return str(result)

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

if __name__ == "__main__":
    app.run()


