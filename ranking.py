import sys
import pickle
import nltk
from nltk.stem import PorterStemmer

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

if __name__ == "__main__":
	query = sys.argv[1]
	pageranks = load_pickle("querydependentrank")
	ranks = score(pageranks, query)
	results = return_links(ranks)
	for i in results:
		print(i)
		print()