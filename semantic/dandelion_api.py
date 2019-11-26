from dandelion import DataTXT
import requests
import json


class DandelionAPI:
    """ La classe permette di interrogare le api di Dandelion per il Ner e la Text Classification. """
    def __init__(self, token):
        self._endpoint = 'https://api.dandelion.eu/datatxt/cl/v1'
        self._model = '54cf2e1c-e48a-4c14-bb96-31dc11f84eac'
        self._token = token
        self._categories = []
        self._entities = []

    def get_categories(self, text):
        """ Dato un testo recupera le categorie. """
        res = requests.post(self._endpoint, data={
            'text': text,
            'model': self._model,
            'token': self._token
        })

        self._categories = json.loads(res.text)['categories']
        return self._categories[0]

    def get_entities(self, text, lang='en', min_confidence=0.7, include='types, lod'):
        """ Dato un testo recupera le entità. """
        datatxt = DataTXT(token=self._token)
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

        return self._entities


if __name__ == '__main__':
    api = DandelionAPI('1950484b2eef4aef8784f97bff21b28f')
    print(api.get_categories('See how the main parties are doing in the latest opinion polls on voting intention'))
    print(api.get_entities('The Mona Lisa is a 16th century oil painting created by Leonardo. It\'s held at the Louvre in Paris.'))
