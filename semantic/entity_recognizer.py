from dandelion import DataTXT
from utils.token_handler import TokenHandler


class EntityRecognizer(TokenHandler):
    """ La classe permette di interrogare le API di Dandelion per la Named-Entity Recognition. """

    def get_entities(self, text, lang='en', min_confidence=0.7, include='types, lod'):
        """
        Dato un testo recupera le entità.

        :param text: rappresenta il testo da cui vogliamo estrarre le entità
        :param lang: indica la lingua in cui è scritto il testo
        :param min_confidence: indica il valore minimo affinchè l'entità estratta venga restituita
        :param include: consente di specificare dei parametri per ottenere più informazioni dalle API di Dandelion.
        In particolare:
            - type: consente di aggiungere informazioni sul tipo (tassonomia) dell'entità estratta attravero una lista
            di link a DBpedia. Se lang='en' vengono restituiti link relativi a DBpedia English.
            - lod: aggiunge link relativi alle equivalenti entità presenti in DBpedia.
        :return: la lista di entità estratte dal documento
        """

        entities = []
        self.validate_token()

        datatxt = DataTXT(token=self._tokenList[self._indexToken])
        annotations = datatxt.nex(
            text,
            lang=lang,
            min_confidence=min_confidence,
            include=include
        ).annotations

        for annotation in annotations:
            entities.append({
                'title': annotation.title,
                'wikipediaURI': annotation.lod.wikipedia,
                'dbpediaURI': annotation.lod.dbpedia,
                'types': annotation.types
            })

        self._requests = self._requests + 1

        return entities
