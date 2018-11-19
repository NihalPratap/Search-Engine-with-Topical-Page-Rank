def calculate_TFIDF(word_count, vocabulory): # Function to calculate the tfidf weights
	tfidf = {}
	for doc in word_count:
		tfidf[doc] = {}
		for term in word_count[doc]:
			tf = word_count[doc][term]/(max(i for i in word_count[doc].values()))
			idf = np.log2(len(word_count)/vocabulory[term])
			tfidf[doc][term] = tf * idf
	return tfidf
