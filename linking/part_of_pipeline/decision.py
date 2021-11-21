### AUTHORS ###
# Clifton Roozendal
# Floris ten Lohuis
# Jens van Holland

# Version: 1.0.0
## Date: 21-11-2021
# Course: Web Data Processing Systems

### DESCRIPTION ###
# Search class, uses Elastic Search to get entities.
# TODO: add some other disambiguation functions e.g. with Trident
import json
import trident
# import asyncio
# from elasticsearch import Elasticsearch, AsyncElasticsearch
import time

KBPATH = 'assets/wikidata-20200203-truthy-uri-tridentdb'
QUERY_FORMAT = ""


class Decision:
    # class information
    input_ = "dict:amb_entities"
    output_ = "dict:disamb_entities"

    def __init__(self) -> None:
        """
        Initialisation function\n
        Input: \n
        \tNone\n
        Output: \n
        \tNone
        """
        self.trident_db = trident.Db(KBPATH)
        pass

    def decide(self, amb_entities):
        """
        Searches a list of given entities \n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tresults of the queries (dict with {wikidatalink:entity} pairs)
        """

        pass
        # return results

    def _forward(self, amb_entities, disambiguation=True):
        """
        Dummy function for streamlining the pipeline\n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tresults of the queries (dict with {wikidatalink:entity} pairs)
        """
        # this is used by the pipeline
        # make sure this returns the acceptable output
        # it seems redudant but _forward is universal parse functions in the pipeline
        if disambiguation:
            return self.decide(amb_entities)
        else:
            return amb_entities
