from utils.token_handler import TokenHandler
import requests
import json

class TextClassifier(TokenHandler):
    """ La classe permette di interrogare le API di Meaning Cloud per la Text Classification. """

    def __init__(self, tokenList, maxRequests):
        super().__init__(tokenList, maxRequests)
        self._endpoint = "https://api.meaningcloud.com/class-1.1"
        self._onto_cat = {
            'Business': 'Business',
            'Sports': 'Sport',
            'Arts&Entertainment': 'Entertainment',
            'Technology&Computing': 'Technology',
            'Health&Fitness': 'Health',
            'LawGovt&Politics': 'Politics'
        }
        self._model = "IAB_en"
        self._model_cat = "|".join(self._onto_cat.keys())

    def get_categories(self, text, min_score = 0.75):
        """
        Dato un testo permette di individuarne la categoria di appartenenza.

        :param text: testo da classificare.
        :param min_score: indica il valore minimo di attendibilità per cui la classificazione del testo è ritenuta
        esatta. Rappresenta un valore compresto tra 0 e 1.
        :return: un dizionario contenente i seguenti campi:
            - name: nome della categoria in cui è stato classificato il testo;
            - score: valore, compreso tra 0 a 1, che indica l'attendibilità della classificazione.
        """

        self.validate_token()
        token = self._tokenList[self._indexToken]
        payload = "key=" + str(token) + "&txt=" + text + "&model=" + self._model +"&categories=" + self._model_cat
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", self._endpoint, data=payload, headers=headers)
        res = json.loads(response.text)['category_list']

        cat = {
            'name': 'Other',
            'score': 1
        }

        if res:
            # Prelevo la prima categoria restituita, ovvero quella con maggiore attendibilità.
            res = res[0]

            cat_name = res['code']
            cat_score = int(res['relevance']) / 100

            # Se la categoria ottenuta rientra in quelle di interesse e lo score è superiore alla soglia stabilita,
            # restituisco le informazioni ottenute. Viceversa, il documento verrà classificato come 'Other' e
            # lo score sarà 1.
            for k in self._onto_cat.keys():
                if k in cat_name and cat_score >= min_score:
                    cat['name'] = self._onto_cat[k]
                    cat['score'] = cat_score

        return cat
