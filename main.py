import os

from ontology.ontology_builder import OntologyBuilder
from preprocessing.keywords_extractor import KeywordsExtractor

dataset_path = './dataset'
dirs = os.listdir(dataset_path)

ob = OntologyBuilder('./ontology/', 'ontology_output.owl')

for dirname in dirs:
    ke = KeywordsExtractor(dataset_path + '/' + dirname)
    keys = ke.extract(topn=10)
    # Istanza della categoria
    ob.add_individual(dirname, dirname + '_01')

    # Istanza dei documenti
    for document, keywords in keys.items():
        path = dataset_path + '/' + dirname + '/' + document.replace(dirname + '_doc_', '') + '.txt'
        doc = ob.add_individual('Document', document)
        cat = ob.get_individual(dirname + '_01')
        ob.add_property(doc, 'has_category', cat)

        for key in keywords.keys():
            keyword = ob.add_individual('Word', 'word_' + key)
            ob.add_property(doc, 'has_keyword', keyword)
            ob.add_property(keyword, 'value', key)

        ob.add_property(doc, 'has_score_' + dirname.lower(), 1)
        ob.add_property(doc, 'path', path)

ob.save()
