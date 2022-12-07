from typing import Union
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.search_engine.ui import UserInterface
import uvicorn


app = FastAPI()


ui = UserInterface()
ui.index_loader()
ui.title_loader()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/fetch/{term}")
def read_item(term: str, bm25: Union[bool, None] = None, recommendations: Union[bool, None] = None):
    start = time.time()
    term_2 = term.replace("/", " ")
    terms = term_2.split()
    queries = []
    for term in terms:
        queries += ui.query_handler(term, bm25, recommendations)
    runtime = time.time()-start
    resp = {
                "term": term,
                "runtime": runtime,
                "bm25": bm25,
                "recs": recommendations,
                "queries": queries
    }
    return resp

if __name__ == '__main__':
    uvicorn.run("backend.main:app", port=8000, reload=True)

