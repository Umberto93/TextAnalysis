from dandelion import DataTXT
import requests
import json

datatxt = DataTXT(token='1950484b2eef4aef8784f97bff21b28f')

annotations = datatxt.nex(
        'The Mona Lisa is a 16th century oil painting created by Leonardo. It\'s held at the Louvre in Paris.',
        lang='en',
        min_confidence=0.7,
        include='types,lod').annotations

for annotation in annotations:
    print(annotation)

ner = {'title': annotations[0].title, 'wikipediaUri': annotations[0].lod.wikipedia, 'dbpediaUri': annotations[0].lod.dbpedia, 'types': annotations[0].types}

print(ner)

def dandelionRequest(text):
    endpoint = 'https://api.dandelion.eu/datatxt/cl/v1'
    authToken = '1950484b2eef4aef8784f97bff21b28f'
    res = requests.post(endpoint, data={
        'text': text,
        'model': '54cf2e1c-e48a-4c14-bb96-31dc11f84eac',
        'token': authToken
    })
    return json.loads(res.text)

res = dandelionRequest('See how the main parties are doing in the latest opinion polls on voting intention')
print(res['categories'])
