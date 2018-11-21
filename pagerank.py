import numpy as np
import pickle

### Standard PageRank

# def create_transition_matrix(data):
# 	urls = get_urls(data)
# 	N = len(data)
# 	M = np.matrix([[weight(N, ru, cu, data) for ru in urls] for cu in urls])
# 	return M.T

# def get_urls(data):
# 	return [url for url, _, _ in data]

# def weight(N, ru, cu, data):
# 	if data[ru][1] is []:
# 		return 1/N
# 	elif cu in data[ru][2]:
# 		return 1/len(data[ru][2])
# 	else:
# 		return 0

# def page_rank(d, data, delta):
# 	N = len(data)
# 	M = create_transition_matrix(data)
# 	v = [1/N] * N
# 	M_hat = (d * M) + (((1 - d)/N) * np.ones((N, N), dtype=np.float32))
# 	last_v = np.ones((N, 1), dtype=np.float32)

# 	while np.linalg.norm(v - last_v) > delta:
# 		last_v = v
# 		v = np.matmul(M_hat, v)
# 	return v

### Topical PageRank

def QueryDependentPageRank(tfidf, crawled_pages, beta=0.85):
	querydependentrank = {}
	for doc in tfidf:
		querydependentrank[doc] = {}
		for term in tfidf[doc]:
			querydependentrank[doc][term] = 1/len(tfidf[doc])
	for iters in range(50):
		for doc in tfidf:
			querydependentrank[doc] = {}
			for term in tfidf[doc]:
				s = 0
				print(term)
				for i in crawled_pages:
					if doc in crawled_pages[i][2]:
						s += (querydependentrank[i][term] if term in querydependentrank[i] else 0) * pi2j_query(term, i, doc, tfidf)
				pdash_query = tfidf[doc][term]/sum(tfidf[i][term] if term in tfidf[i] else 0 for i in tfidf)
				querydependentrank[doc][term] = (1 - beta) * pdash_query + (beta * s)
	save_pickle(querydependentrank,"querydependentrank")

def pi2j_query(term, i, j, tfidf):
	s = 0
	for doc in crawled_pages[i][2]:
		if doc in tfidf and term in tfidf[doc]:
			s += tfidf[doc][term]

	return (tfidf[j][term] if term in tfidf[j] else 0)/s
	# sum(tfidf[doc][term] if term in tfidf[doc] else 0 for doc in crawled_pages[i][2])

def save_pickle(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_pickle(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
	crawled_pages = load_pickle("crawl_pages")
	tfidf = load_pickle("tfidf")
	print(len(crawled_pages))
	print(len(tfidf))
	# print(crawled_pages['https://www.cs.uic.edu/<br /> <b>Notice</b>:  Undefined variable: cat_link in <b>/var/www/cs1.engr-dev.uic.edu/wp-content/themes/lincoln/content-single.php</b> on line <b>47</b><br /> '])
	QueryDependentPageRank(tfidf, crawled_pages, 0.85)
