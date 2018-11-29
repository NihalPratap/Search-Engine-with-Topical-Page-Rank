import sys
import pickle
import nltk
from nltk.stem import PorterStemmer
from flask import Flask, render_template, redirect, url_for,request, jsonify
from flask import make_response
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

def stemmer_porter(arr):  # function to apply stemming on the words
    stemmer = PorterStemmer()
    arr = [stemmer.stem(i) for i in arr]
    return arr

def score(pageranks, query):
	prob_query = {}
	ranks = {}
	query = nltk.word_tokenize(query)
	query = stemmer_porter(query)
	for word in query:
		prob_query[word] = 1/len(query)
	for doc in pageranks:
		ranks[doc] = sum(prob_query[word]*pageranks[doc][word] if word in pageranks[doc] else 0 for word in query)
	return ranks

def return_links(ranks):
	top = 10
	results = sorted(ranks.items(), key=lambda x: (-x[1], x[0]))[0:top]
	return results

def load_pickle(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def load(name):
	if os.path.getsize(name+".pkl") > 0:      
	    with open(name+".pkl", "rb") as f:
	        unpickler = pickle.Unpickler(f)
	        # if file is not empty scores will be equal
	        # to the value unpickled
	        return unpickler.load()

def load_json(name):
	with open(name+'.json') as json_data:
		return json.load(json_data)

@app.route('/rank', methods=['GET', 'POST'])
def main():
	if request.method == 'GET':
		query = request.args['param']
		print(query)
		# pageranks = load_pickle("querydependentrank")
		pageranks = load_json("querydependentrank")
		print(len(pageranks))
		ranks = score(pageranks, query)
		results = return_links(ranks)
		count = 0
		for i in results:
			if i[1] == 0:
				count += 1
		if count < 10:
			return jsonify(results)
		else:
			return jsonify("No Match")

if __name__ == "__main__":
	app.run(debug=True)