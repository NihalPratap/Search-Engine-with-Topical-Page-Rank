import pickle
import numpy as np

def calculate_TFIDF(word_count, vocabulory): # Function to calculate the tfidf weights
	tfidf = {}
	for doc in word_count:
		tfidf[doc] = {}
		for term in word_count[doc]:
			tf = word_count[doc][term]/(max(i for i in word_count[doc].values()))
			idf = np.log2(len(word_count)/vocabulory[term])
			tfidf[doc][term] = tf * idf
	return tfidf

def load_word_count():
    with open('word_count.pkl', 'rb') as f:
        return pickle.load(f)

def load_vocabulory():
    with open('vocabulory.pkl', 'rb') as f:
        return pickle.load(f)

def save_pickle(obj):
    with open('tfidf.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
	word_count = load_word_count()
	vocabulory = load_vocabulory()
	print(len(word_count))
	tfidf = calculate_TFIDF(word_count, vocabulory)
	save_pickle(tfidf)