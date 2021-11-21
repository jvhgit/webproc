### AUTHORS ###
## Clifton Roozendal
## Eduard Bosch
## Floris ten Lohuis
## Jens van Holland

## Version: 1.0.1
## Date: 21-11-2021
## Course: Web Data Processing Systems

### DESCRIPTION ###
#Search class, uses Elastic Search to get entities. 
#TODO: add some other disambiguation functions e.g. with Trident
import json
import asyncio
from elasticsearch import Elasticsearch, AsyncElasticsearch
import time
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
        self.async_e = AsyncElasticsearch()
        pass

    def _remove(self, amb_entities):
        """
        Removes obviously wrong entities (doubles, single characters, weird characters?) \n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tam_entities
        """

        #
        temp_result = list(set(amb_entities)) #property of set is no doubles allowed->than cast to list again

        return temp_result

    async def _search(self, query):
        """
        Removes obviously wrong entities (doubles, single characters, weird characters?) \n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tam_entities
        See: https://elasticsearch-py.readthedocs.io/en/7.x/async.html
        """
        # print(help(self.async_e.search))
        try:
            response = await self.async_e.search(
                index="wikidata_en",
                body=query,
                # size = 20
            )
            # async with response:
            id_labels = {}
            if response:
                for hit in response['hits']['hits']:
                    label = hit['_source']['schema_name']
                    id = hit['_id']
                    id_labels.setdefault(id, set()).add(label)
            return id_labels
        except:
            return {}

    def fastsearch(self, amb_entities):
        """
        Removes obviously wrong entities (doubles, single characters, weird characters?) \n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tam_entities
        See: https://elasticsearch-py.readthedocs.io/en/7.x/async.html
        """
         #remove doubles and obvious wrongly entities
        start = time.time()
        amb_entities = self._remove(amb_entities)
        results = []
        #set queries
        json_queries = [json.dumps({ "query" : { "query_string" : { "query" : ent }}}) for ent in amb_entities ]
        query_group = asyncio.gather(*[self._search(q) for q in json_queries])
        #initialize loop
        loop = asyncio.get_event_loop()
        #get queries
        results = loop.run_until_complete(query_group)
        # print(results)
        stop = time.time()
        print(f"The time for search is: {stop - start}")
        return results

    def search(self, amb_entities):
        """
        Searches a list of given entities \n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tresults of the queries (dict with {wikidatalink:entity} pairs)
        """
        results = []
        start = time.time()

        #remove doubles and obvious wrongly entities
        amb_entities = self._remove(amb_entities)
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
        stop = time.time()
        print(f"The time for search is: {stop - start}")

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
        # return self.search(amb_entities)
        return self.fastsearch(amb_entities)

