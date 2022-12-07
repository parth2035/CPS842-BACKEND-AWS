import numpy as np

def get_doc_length(titles):
    sum = 0
    titles_length = len(titles)
    for term in titles:
        sum += titles[term][1]
    return sum / titles_length

def get_term_freq(freq, k, b, doc_length, avg_doc_length):
    num = freq * (k + 1)
    denom = freq + k * (1 - b + b * (doc_length / avg_doc_length))
    return num/denom

def get_inverse_doc_freq(titles_length, doc_freq):
    ratio = (titles_length - doc_freq + 0.5) / (doc_freq + 0.5)
    return np.log((ratio) + 1)

def bm25(doc_length, freq, doc_freq, titles_length, avg_doc_length, k=1.2, b=0.75):
    tf = get_term_freq(freq, k, b, doc_length, avg_doc_length)
    idf = get_inverse_doc_freq(titles_length, doc_freq)
    return round(tf * idf, 4)

def bm25_handler(term, index, titles, doc_id):
    doc_freq = index[term][0]
    freq = index[term][2][str(doc_id)][0]
    avg_doc_length = get_doc_length(titles)
    titles_length = len(titles)
    doc_length = titles[str(doc_id)][1]
    score = bm25(doc_length, freq, doc_freq, titles_length, avg_doc_length)
    return score
