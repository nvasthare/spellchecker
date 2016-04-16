from sets import Set
from flask import Flask,request
app = Flask(__name__)

threshRes = 0
threshAdd = 0
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
        print word
        word = ("**" + word + "**").lower()
        for i in xrange(len(word) - 2):
            tri = word[i:i+3]
            print tri
            if tri in trigrams:
                trigrams[tri] += 1
            else:
                trigrams[tri] = 1
    return trigrams

def getWords():
    s = Set()
    f2 = open('engtrain.txt')
    for line in f2:
        line = line.strip()
        line = line.split()
        word = line[0]
        word = word.lower()
        print word.strip()
        s.add(word.strip())
        if len(s) > 1000:
            break
    f2.close()
    return s

train = getWords()
trigrams = getTrigrams(train)
# orig = getTrigrams(train)

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
    # print "do test"
    s = Set()
    i = 0
    tri = getTrigrams(set([word]))
    minTri,mtri = test(trigrams,tri)
    size = getSize(trigrams)
    perc = minTri/size * scale
    print perc
    # if perc > threshAdd:
    if (perc > threshRes):
        return 0
    else:
        # trigrams = getTrigrams(set([word]),trigrams)
        return -1
       


@app.route("/",methods=["GET","POST"])
def main():
    # print trigrams
    global train
    global trigrams
    word = request.form['params']
    if word == "**reset**":
        print "reset"
        trigrams = getTrigrams(train)
        return str(0)
    print word
    result = doTest(word)
    print result
    return str(result)

@app.after_request
def add_headers(response):
    print "headers"
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

if __name__ == "__main__":
    print "run"
    app.run()






