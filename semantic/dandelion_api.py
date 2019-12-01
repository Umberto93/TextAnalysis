import json
import requests
from dandelion import DataTXT


class DandelionAPI:
    """ La classe permette di interrogare le api di Dandelion per il Ner e la Text Classification. """
    def __init__(self, tokenList, maxRequests):
        self._endpoint = 'https://api.dandelion.eu/datatxt/cl/v1'
        self._model = '54cf2e1c-e48a-4c14-bb96-31dc11f84eac'
        self._tokenList = tokenList
        self._maxRequests = maxRequests
        self._indexToken = 0
        self._requests = 0
        self._categories = []
        self._entities = []

    def get_categories(self, text):
        self.validate_token()
        """ Dato un testo recupera le categorie. """
        res = requests.post(self._endpoint, data={
            'text': text,
            'model': self._model,
            'token': self._tokenList[self._indexToken]
        })

        self._requests = self._requests + 1
        self._categories = json.loads(res.text)['categories']
        return self._categories[0]

    def get_entities(self, text, lang='en', min_confidence=0.7, include='types, lod'):
        self._entities = []
        self.validate_token()
        """ Dato un testo recupera le entità. """
        datatxt = DataTXT(token=self._tokenList[self._indexToken])
        annotations = datatxt.nex(
            text,
            lang=lang,
            min_confidence=min_confidence,
            include=include
        ).annotations

        for annotation in annotations:
            self._entities.append({
                'title': annotation.title,
                'wikipediaURI': annotation.lod.wikipedia,
                'dbpediaURI': annotation.lod.dbpedia,
                'types': annotation.types
            })

        self._requests = self._requests + 1

        return self._entities

    def validate_token(self):
        if(self._requests == self._maxRequests):
            self._requests = 0
            self._indexToken = (self._indexToken + 1) % len(self._tokenList)


if __name__ == '__main__':
    api = DandelionAPI(['1950484b2eef4aef8784f97bff21b28f','90057b00684745d5b4fe2ae0a82432a9', 'bda714d81dc54fc8a0bd43398125a4e6'], 950)
    entities = api.get_entities('The Mona Lisa is a 16th century oil painting created by Leonardo. It is held at the Louvre in Paris. The Mona Lisa is a oil painting.')
    print(entities)
