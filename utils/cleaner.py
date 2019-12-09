import os

from nltk.corpus import stopwords
from nltk import RegexpTokenizer, WordNetLemmatizer

from utils.file_manager import FileManager


def clean_text(text):
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

def read_cleaned_docs(documents_path, category):
    """
    Legge i documenti relativi alla categoria in esame ed effettua la pulizia del testo.

    :param documents_path: lista contenente i percorsi alle cartelle in cui risiedono i documenti del dataset e i
    documenti caricati dall'utente.
    :param category: nome della categoria di interesse. Il nome della cartella contenente i file relativi alla categoria
    deve coincidere con quello della relativa classe presente nell'ontologia.
    :return: dizionario contenente i documenti letti. In particolare:
        - La chiave corrisponde al seguente nome '(category)_doc_(nome_del_documento)';
        - Il valore corrisponde al testo pulito.
    """

    file_manager = FileManager()

    # Collezione dei documenti contenuti nella directory esaminata
    docs = {}

    for path in documents_path:
        # Path della cartella contenente i documenti relativi alla categoria esaminata
        cat_dir_path = path + '/' + category

        if os.path.exists(cat_dir_path):
            # Elenco dei file contenuti nella directory esaminata
            files = os.listdir(cat_dir_path)

            # Lettura file e pulizia del testo contenuto
            for file_name in files:
                text = file_manager.read_file(cat_dir_path + '/' + file_name)
                docs[category + '_doc_' + file_name.split('.')[0]] = clean_text(text)
        else:
            os.makedirs(cat_dir_path)

    return docs
