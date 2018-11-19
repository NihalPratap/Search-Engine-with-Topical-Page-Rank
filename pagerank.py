import numpy as np

def create_transition_matrix(data):
	urls = get_urls(data)
	N = len(data)
	M = np.matrix([[weight(N, ru, cu, data) for ru in urls] for cu in urls])
	return M.T

def get_urls(data):
	return [url for url, _, _ in data]

def weight(N, ru, cu, data):
	if data[ru][1] is []:
		return 1/N
	elif cu in data[ru][2]:
		return 1/len(data[ru][2])
	else:
		return 0

def page_rank(d, data, delta):
	N = len(data)
	M = create_transition_matrix(data)
	v = [1/N] * N
	M_hat = (d * M) + (((1 - d)/N) * np.ones((N, N), dtype=np.float32))
	last_v = np.ones((N, 1), dtype=np.float32)

	while np.linalg.norm(v - last_v) > delta:
		last_v = v
		v = np.matmul(M_hat, v)
	return v