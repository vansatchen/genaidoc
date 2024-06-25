#!/opt/local-gen-search/venv/bin/python

from fastapi import FastAPI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from pydantic import BaseModel
import requests
import uvicorn


class Item(BaseModel):
    query: str
    def __init__(self, query: str) -> None:
        super().__init__(query=query)


model_name = "sentence-transformers/msmarco-bert-base-dot-v5"
model_kwargs = {'device': 'cpu'} # {'device': 'cuda'} for use with cuda
encode_kwargs = {'normalize_embeddings': True}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)


client = QdrantClient(path="qdrant/")
collection_name = "MyCollection"
qdrant = Qdrant(client, collection_name, hf)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Ok"}


@app.post("/search")
def search(Item:Item):
    query = Item.query
    search_result = qdrant.similarity_search(
        query=query, k=10
    )
    i = 0
    list_res = []
    for res in search_result:
        list_res.append({"id":i,"path":res.metadata.get("path"),"content":res.page_content})
    return list_res


@app.post("/ask_localai")
async def ask_localai(Item:Item):
    query = Item.query
    search_result = qdrant.similarity_search(
        query=query, k=10
    )
    i = 0
    list_res = []
    context = ""
    mappings = {}
    i = 0
    for res in search_result:
        context = context + str(i)+"\n"+res.page_content+"\n\n"
        mappings[i] = res.metadata.get("path")
        list_res.append({"id":i,"path":res.metadata.get("path"),"content":res.page_content})
        i = i +1

    url = 'http://localhost:8000/v1/chat/completions'
    headers = {'content-type': 'application/json','accept': 'application/json'}
    data = {
            "temperature": 0.1,
            "messages": [
              {"role": "system",
               "content": "Answer user's question using documents given in the context. In the context are documents that should contain an answer. Please always reference document id (in squere brackets, for example [0],[1]) of the document that was used to make a claim. Use as many citations and documents as it is necessary to answer question."
              },
              {"role": "user",
               "content": "Documents:\n"+context+"\n\nQuestion: "+query
              }
            ]
    }

    r = requests.post(url, headers=headers, json=data)
    response = r.json()['choices'][0]['message']['content']
    return {"context":list_res,"answer":response}


if __name__ == "__main__":
    uvicorn.run("api:app",host='0.0.0.0', port=8010)
