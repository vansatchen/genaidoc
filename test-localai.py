import requests

r = requests.post("http://localhost:8010/ask_localai", json={"query":"Who is eating cocoa?"})

#for item in r.json()['context']:
#    print(item['path'])
#    print(item['content'])
#    print('-----------------------\n')

print(r.json()['answer'])
