import eel
from ontology.ontology_builder import OntologyBuilder
from utils.kency_api import KencyAPI

eel.init('web')

ontology_builder = OntologyBuilder()
onto = ontology_builder.load_onto('../kency/of4-ontology.owl')

api = KencyAPI(onto)

@eel.expose
def py_request(pathname, params=None):
    if pathname == '/articles':
        return api.get_documents(params)
    if pathname == '/keywords':
        pass
        #return api.get_words_starting_with()
    if pathname == '#classification':
        return 'classification'
    if pathname == '/categories':
        return api.get_categories()


eel.start('index.html', mode='chrome-app')
