class TokenHandler:
    """ Gestisce i token utilizzati per effettuare le richieste alle API di Dandelion e Meaning Cloud. """

    def __init__(self, tokenList, maxRequests):
        self._tokenList = tokenList
        self._maxRequests = maxRequests
        self._indexToken = 0
        self._requests = 0

    def validate_token(self):
        if(self._requests == self._maxRequests):
            self._requests = 0
            self._indexToken = (self._indexToken + 1) % len(self._tokenList)