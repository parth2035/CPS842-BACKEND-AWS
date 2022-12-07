import json
import logging
import backend.search_engine.config as config
from nltk.stem import PorterStemmer
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer

from backend.search_engine.bm25 import bm25_handler

with open(config.KMEANS_MODEL_PATH, "rb") as f:
    kmeans_model = pickle.load(f)

with open(config.KMEANS_VEC_PATH, "rb") as f:
    vectorizer = pickle.load(f)

with open(config.SAVE_DOC_TEXT_PATH, "rb") as f:
    doc_to_text = json.load(f)


class UserInterface:
    def __init__(self):
        self.index = None
        self.titles = None
        self.ps = PorterStemmer()

        self.logo = config.LOGO

        self.template_query_results = {
            "doc_id": None,
            "doc_title": None,
            "": None
        }

    def index_loader(self):
        f = open(config.TEST_BUILD_1)
        self.index = json.load(f)
        f.close()

    def title_loader(self):
        f = open(config.SAVE_DOC_TITLES_PATH)
        self.titles = json.load(f)
        f.close()

    def query_handler(self, cmd, bm25=False, recommendations=False):
        query_results = []

        if cmd == "ZZEND":
            return query_results

        cmd = self.ps.stem(cmd.lower().strip())

        if cmd in self.index:
            counter = 0

            for doc_id in self.index[cmd][1]:
                counter += 1

                record = {
                    "term": cmd,
                    "doc_id": doc_id,
                    "recommended_term": False,
                    "doc_name": self.titles[str(doc_id)][0],
                    "num_doc_occurrence": self.index[cmd][2][str(doc_id)][0],
                    "locations_term": self.index[cmd][2][str(doc_id)][1]
                }

                query_results.append(record)

                if counter % 20 == 0:
                    break

            if bm25:
                new_results = []
                for record in query_results:
                    record["bm25_score"] = bm25_handler(cmd, self.index, self.titles, record["doc_id"])
                    new_results.append(record)
                query_results = sorted(new_results, key=lambda d: d["bm25_score"], reverse=True)

            if recommendations:
                top_stuff = kmeans_model.cluster_centers_.argsort()[:, ::-1]
                terms = vectorizer.get_feature_names()
                Y = vectorizer.transform([" ".join(doc_to_text[str(query_results[0]["doc_id"])])])  # HERE

                prediction = kmeans_model.predict(Y)[0]
                top_5_terms_recommended = []
                for i in range(2):
                    top_5_terms_recommended.append(terms[top_stuff[prediction][i]])

                recommendations_results = []
                for term in top_5_terms_recommended:
                    recom_results = self.query_handler(term, bm25, recommendations=False)
                    for result in recom_results:
                        result["recommended_term"] = True
                        recommendations_results.append(result)
                query_results = query_results + recommendations_results

            temp_results = []
            for result in query_results:
                term_index = result["locations_term"][0]

                if term_index > 30:
                    words = doc_to_text[str(result["doc_id"])][term_index - 30:term_index + 30]
                else:
                    words = doc_to_text[str(result["doc_id"])][0:60]

                result["sample_text"] = ' '.join(words)
                if len(result["sample_text"]) == 0:
                    words = doc_to_text[str(result["doc_id"])][0:60]
                    result["sample_text"] = ' '.join(words)

                temp_results.append(result)

            query_results = temp_results

            return query_results
        else:
            print('Query not found')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Started the app!")
    userInterface = UserInterface()
    userInterface.index_loader()
    userInterface.title_loader()
    logging.info("Application terminated!")
