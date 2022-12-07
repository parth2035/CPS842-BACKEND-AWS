STOPWORDS_BOOL = True
STEMMING_BOOL = True
DATA_CUTOFF = 20000
KMEANS_VEC_PATH = "backend/search_engine/kmeans_vec.pkl"
KMEANS_MODEL_PATH = "backend/search_engine/kmeans_model.pkl"
SAVE_DOC_TITLES_PATH = "backend/data/processed/doc_titles.json"
SAVE_DOC_TEXT_PATH = "backend/data/processed/doc_text.json"
RAW_DATA_PATH = "backend/data/raw/trec_corpus_20220301_plain.json"
TEST_BUILD_1 = "backend/data/processed/index.json"
STOPWORDS_FILE = "backend/search_engine/stopwords.txt"
SAVE_INDEX_PATH = "backend/data/processed/index.json"
PUNCTUATION = r'[,.;@#?!&$()]+'
LOGO = r""" ____     ____    ____       __    __ __       ___     
/\  _`\  /\  _`\ /\  _`\   /'_ `\ /\ \\ \    /'___`\   
\ \ \/\_\\ \ \L\ \ \,\L\_\/\ \L\ \\ \ \\ \  /\_\ /\ \  
 \ \ \/_/_\ \ ,__/\/_\__ \\/_> _ <_\ \ \\ \_\/_/// /__ 
  \ \ \L\ \\ \ \/   /\ \L\ \/\ \L\ \\ \__ ,__\ // /_\ \
   \ \____/ \ \_\   \ `\____\ \____/ \/_/\_\_//\______/
    \/___/   \/_/    \/_____/\/___/     \/_/  \/_____/ """