from flask import Flask,request
app = Flask(__name__)
d = ['some', 'text', 'with', 'wrong', 'words', 'hello', 'this', 'is', 'a', 'post'];

@app.route("/",methods=["GET","POST"])
def main():
	# print "main"
	global d
	print d
	word = request.form['params']
	if word in d:
		return str(0)
	else:
		# d += [word]
		return str(-1)

@app.after_request
def add_headers(response):
	# print "response"
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	return response

if __name__ == "__main__":
	# print "run"
	app.run()
