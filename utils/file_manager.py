class FileManager:
    """ Gestisce la lettura/scrittura di files """

    def __init__(self):
        pass

    def read_file(self, path):
        """ Restituisce il contenuto di un file in formato testuale """
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

    def write_file(self, path, text):
        """ Effettua la scrittura su file """
        with open(path, 'w') as f:
            return f.write(text)
