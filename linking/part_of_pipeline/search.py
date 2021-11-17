### AUTHORS ###
## Clifton Roozendal
## Eduard Bosch
## Floris ten Lohuis
## Jens van Holland

## Version: 1.0.0
## Date: 16-11-2021
## Course: Web Data Processing Systems

### DESCRIPTION ###
#Search class, uses Elastic Search to get entities. 
#TODO: add some other disambiguation functions e.g. with Trident
import json
from elasticsearch import Elasticsearch

class Search:
    # class information
    input_ = "list:amb_entities"
    output_ = "list:disamb_entities"

    def __init__(self) -> None:
        """
        Initialisation function\n
        Input: \n
        \tNone\n
        Output: \n
        \tNone
        """
        self.e = Elasticsearch()
        pass

    def search(self, amb_entities):
        """
        Searches a list of given entities \n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tresults of the queries (dict with {wikidatalink:entity} pairs)
        """
        results = []
        for ent in amb_entities:
            #TODO: we need to find a way to make the quering more efficient (i.e. batches possible?)
            p = { "query" : { "query_string" : { "query" : ent }}}
            try:
                response = self.e.search(index="wikidata_en", body=json.dumps(p))
                id_labels = {}
                if response:
                    for hit in response['hits']['hits']:
                        label = hit['_source']['schema_name']
                        id = hit['_id']
                        id_labels.setdefault(id, set()).add(label)
                results.append(id_labels)
            except:
                continue
            #TODO: a lot of duplicates (might also impact computation time)
        return results
    
    def _forward(self, amb_entities):
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
        return self.search(amb_entities)
