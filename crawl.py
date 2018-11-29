import re
import string
import nltk
import os
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO, BytesIO
import pagerank
import pickle

def readStopwords():  # function to read the stopwords from stopwords.txt file
    stopwords = []
    with open("stopwords.txt", 'r') as f:
        for line in f.readlines():
            word = line.strip()
            stopwords.append(word)
    return stopwords

def stemmer_porter(arr):  # function to apply stemming on the words
    stemmer = PorterStemmer()
    arr = [stemmer.stem(i) for i in arr]
    return arr

def crawl(urls, crawled, word_count, vocabulory, base=None):
	not_allowed = ['.avi', '.zip', '.mov']
	if not base:
		base = [urlparse(u).netloc for u in urls]
	while urls:
		if len(crawled) % 50 == 0 and len(crawled) != 0:
			delete_pickle()
			save_pickle(crawled, urls, word_count, vocabulory)
		print(len(urls))
		print(len(crawled))
		url = urls.pop(0)
		url = url.rstrip("/")
		if url == "https://www.cs.uic.edu/bin/view/Tanya/KenyaCourse#foo_1":
			continue
		if "http://www.cs.uic.edu/bin/view/CHE" in url:
			continue
		if url in crawled or url.rstrip("/") in crawled:
			continue
		print("crawling ", url)
		try:
			response = download(url)
		except Exception as e:
			print(e, url)
			continue
		data = parse(url, response, base, word_count, vocabulory)
		if data is not -1:
			crawled[url] = data
			a = [i for i in crawled[url][2] if (i not in crawled and i.rstrip("/") not in crawled and i not in urls and not any([i.endswith(format) for format in not_allowed]))]
			urls += a
			print("Crawled %s with %d links but unvisited are %d"%(url, len(crawled[url][2]), len(a)))
	return crawled

def parse(url, response, base, word_count, vocabulory):
	soup = BeautifulSoup(response, 'lxml')
	content = None
	if url.endswith('.pdf'):
		scrape = urlopen(url)
		try:
			content = readPDF(BytesIO(scrape.read()))
			content = tokenize_text(content, word_count, vocabulory, url)
		except Exception as e:
			print(e, url)
			return -1
	else:
		if soup.body:
			content = cleanMe(soup, response)
			content = tokenize_text(content, word_count, vocabulory, url)
	links = [urljoin(url, l.get('href')) for l in soup.findAll('a')]
	links = [l.rstrip("/") for l in links if urlparse(l).netloc in base]
	# print(content)
	return url, content, list(set(links))

def download(url):
	return urlopen(url)

def tokenize_text(content, word_count, vocabulory, url):
	arr = []
	vocab = True
	translator=str.maketrans('','',string.punctuation)
	stopwords = readStopwords()
	cleanr = re.compile('<.*?>')
	content = re.sub(cleanr, '', content)
	content = ''.join([i for i in content if not i.isdigit()])
	content = content.strip().lower()
	content = content.translate(translator)
	words = nltk.word_tokenize(content)  # tokenize the words using nltk's tokenizer
	words = [i for i in words if not i in stopwords] # remove stop words
	words = stemmer_porter(words) # stemming
	words = [i for i in words if not i in stopwords] # remove stop words after stemming
	word_count[url] = {}
	for token in words:
		if len(token) > 2: # use the word only if the lenght is greater than 2
			if token not in word_count[url].keys():
				word_count[url][token] = 1
			else:
				word_count[url][token] += 1
			# update the vocabulory count/document frequency
			if token not in vocabulory:
				vocabulory[token] = 1
			elif vocab:
				vocabulory[token] += 1
				vocab = False
			arr.append(token)
	return arr

def cleanMe(soup, html):
    for script in soup(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def load_pages(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def load_urls(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def load_word_count(name):
    with open('word_count.pkl', 'rb') as f:
        return pickle.load(f)

def load_vocabulory(name):
    with open('vocabulory.pkl', 'rb') as f:
        return pickle.load(f)

def save_pickle(obj, urls, word_count, vocabulory):
    with open('crawl_pages.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    with open('urls.pkl', 'wb') as f:
        pickle.dump(urls, f, pickle.HIGHEST_PROTOCOL)
    with open('word_count.pkl', 'wb') as f:
        pickle.dump(word_count, f, pickle.HIGHEST_PROTOCOL)
    with open('vocabulory.pkl', 'wb') as f:
        pickle.dump(vocabulory, f, pickle.HIGHEST_PROTOCOL)

def delete_pickle():
	os.remove("crawl_pages.pkl")
	os.remove("urls.pkl")
	os.remove("word_count.pkl")
	os.remove("vocabulory.pkl")

def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(pdfFile, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    device.close()
    textstr = retstr.getvalue()
    retstr.close()
    return textstr

if __name__ == "__main__":
	crawled = load_pages("crawl_pages")
	urls = load_urls("urls")
	word_count = load_word_count("word_count.pkl")
	vocabulory = load_vocabulory("vocabulory.pkl")
	# word_count = {}
	# vocabulory = {}
	# crawled = {}
	# urls = ["https://www.cs.uic.edu/"]
	pages = crawl(urls, crawled, word_count, vocabulory)
	delete_pickle()
	save_pickle(pages, "crawl_pages")
	# ranks = pagerank.page_rank(pages)