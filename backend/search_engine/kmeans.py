from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import json
import backend.search_engine.config as config
import pickle


def loadData():
    documents = []
    count = 0
    with open(config.RAW_DATA_PATH, 'r') as file:
        for line in file:
            count += 1
            documents.append(json.loads(line))
            if count > 20000:
                break
    data = []
    counter = 0
    for doc in documents:
        counter += 1
        data.append(doc["plain"])
        if counter % config.DATA_CUTOFF == 0:
            break
    return data


def vectorizeData():
    vectorizer = TfidfVectorizer(stop_words='english')
    return vectorizer


def modelFit(X, vectorizer):
    true_k = 45
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)

    with open(config.KMEANS_MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    with open(config.KMEANS_VEC_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

def main():
    data = loadData()
    vectorizer = vectorizeData()
    X = vectorizer.fit_transform(data)
    modelFit(X, vectorizer)

main()