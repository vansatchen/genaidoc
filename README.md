# genaidoc
This is adapted version of [Local-GenAI Search](https://github.com/nikolamilosevic86/local-genAI-search) for use with [LLaMA.cpp HTTP Server](https://github.com/ggerganov/llama.cpp/blob/master/examples/server/README.md) or [OpenAI Compatible Web Server](https://github.com/abetlen/llama-cpp-python?tab=readme-ov-file#openai-compatible-web-server)

## How to run
Download the repository:
```
git clone https://github.com/vansatchen/genaidoc.git
```
Move to directory:
```
cd genaidoc
```
(Optional) make virtual environment:
```
python -m venv venv
source venv/bin/activate
```
Install all the requirements:
```
pip install -r requirements.txt
```
The next step is to index a folder and its subfolders containing documents that you would like to search. You can do it using the index.py file. Run:
```
python index.py path/to/folder
```
This will create a qdrant client index locally and index all the files in this folder and its subfolders with extensions .pdf,.txt,.docx,.pptx

The next step would be to run the generative search service. For this you can run:
```
python uvicorn_start.py
```
This will start a local server, that you can query using postman, or send POST requests. Loading of models (including downloading from Huggingface, may take few minutes, especially for the first time). There are two interfaces:
```
http://127.0.0.1:8000/search
```
```
http://127.0.0.1:8000/ask_localai
```
Both interfaces need body in a format:
```
{"query":"What are knowledge graphs?"}
```
and headers for Accept and Content-Type set to `application/json`.

Here is a code example:
```
import requests
import json

url = "http://127.0.0.1:8000/ask_localai"

payload = json.dumps({
  "query": "What are knowledge graphs?"
})
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```
