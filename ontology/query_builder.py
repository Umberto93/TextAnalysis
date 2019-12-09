from owlready2 import *


class QueryBuilder:
    """ La classe consente di effettuare query SPARQL. """

    def __init__(self):
        self._world = default_world
        sync_reasoner(self._world)
        self._graph = self._world.as_rdflib_graph()

    def get_graph(self):
        return self._graph

    def run_query(self, query):
        """
        Esegue la query passata come parametro.
        :param query: La query da eseguire.
        :return: I risultati della query.
        """
        return list(self._graph.query(query))
