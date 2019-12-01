from nltk.corpus import stopwords
from nltk import RegexpTokenizer, WordNetLemmatizer


def get_cleaned_text(text):
    """
    Effettua la pulizia del testo rimuovendo stop words e lemmatizzando.
    :param text: Il testo su cui effettuare l'operazione di pulizia.
    :return: Il testo pulito.
    """

    tokenizer = RegexpTokenizer(r'\w{4,}')
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    clean_text = ''

    # Estrae i token dal testo rimuovendo i caratteri speciali e
    # le parole con meno di 4 caratteri
    tokens = tokenizer.tokenize(text.lower())

    # Costruisce un nuovo testo a partire dall'insieme di token
    # estratti in precedenza, ignorando le stop words.
    for word in tokens:
        if not word in stop_words:
            clean_text += lemmatizer.lemmatize(word) + ' '

    return clean_text
