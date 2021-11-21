### AUTHORS ###
# Clifton Roozendal
# Floris ten Lohuis
# Jens van Holland

# Version: 1.0.0
## Date: 21-11-2021
# Course: Web Data Processing Systems


### DESCRIPTION ###
# Decision class, uses Trident to decide if correct wikilinks are found for the entities are found
# TODO: add some other disambiguation functions e.g. with Trident

#LITERATURE
# http://ceur-ws.org/Vol-2773/paper-02.pd (paper for entity linking using wikidata)
import json
import trident
import collections
# import asyncio
import time

KBPATH = 'assets/wikidata-20200203-truthy-uri-tridentdb'
QUERY_FORMAT = 'PREFIX wd: {}'\
               'PREFIX schema: <http://schema.org/>'\
               'SELECT ?o'\
               'WHERE'\
               '{'\
               'wd:Q3 schema:description ?o.'\
               'FILTER ( lang(?o) = "en" )'\
               '}'


class Decision:
    # class information
    input_ = "dict:amb_entities"
    output_ = "dict:disamb_entities"

    def __init__(self, threshold = None, take_first = True, n_hits = 5) -> None:
        """
        Initialisation function\n
        Input: \n
        \tNone\n
        Output: \n
        \tNone
        """
        self.trident_db = trident.Db(KBPATH)
        self.n_hits_entity = n_hits
        self.threshold = threshold
        self.take_first = take_first
        pass

    def _query(self, wiki):
        
        return self.trident_db.sparql( #query to database
            QUERY_FORMAT.format(wiki) #format string with inputs
        )

    def _convertToVector(self, query_information = None, text_information = None):
        """
        Converts query and/or text information to a vector (which can be compared) \n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tresults of the queries (dict with {wikidatalink:entity} pairs)
        """
        if query_information != None:
            #some code to represent the information 
            if method == "1":
                return None
            elif method == '2':
                return None

        elif text_information != None:
            #some code to represent the information 
            if method == "1":
                return None
            elif method == '2':
                return None

        else:  print("Please give query or text information to vectorize (None given).")

    def _compare(self, entity_representation = None, text_representation = None, method = "1"  ):
        """
        Searches a list of given entities \n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tresults of the queries (dict with {wikidatalink:entity} pairs)
        """
        if method == "1": #comparting method 1 (cosine similarity?)
            return None
        elif method == "2": #comparing method 2 (.... similarity0)
            return None
        else: #no method is accepting al (i.e. omitting disambiguation)
            return 1.0

    def decide(self, amb_entities, texts):
        """
        Searches a list of given entities \n
        Input: \n
        \t amb_entities: (list) a list with tuples (text_id, entity, wikilink)\n
        \t texts: (list) a list with tuples (text_id, text)\n
        Output: \n
        \tresults of the queries (dict with {wikidatalink:entity} pairs)
        """

        representation_ents = [] #4-tuple (text_id, ent, wiki, vector)
        representation_texts = [] #2 tuple (text_id, vector)

        entity_frequency= dict(collections.Counter(list(amb_entities.values())))
        #first represent the entity-wiki
        for id_, ent, wiki in amb_entities:
            if (take_first)&(entity_frequency[ent] < 2): #if only 1 match always return this match
                representation_ents.append((id_, ent, wiki, [None])) 
            else:#otherwise make representation for the ent-wiki
                information = self._query(inputs = wiki)
                representation_ents.append(
                    (id_, ent, wiki, self._convertToVector(query_information=information))
                )

        #second represent the sentences (could also use other entities for this)
        for id_, text in texts:
            information = text #make information variable
            representation_texts.append(
                (id_, ent, wiki, self._convertToVector(query_information=information))
            )

        #make scores for each entity-wiki
        #TODO make exception for 1 match entities
        scores = [] #4-tuple (text_id, ent, wiki, score)
        temp_id = ""
        temp_representation = ""
        for id_, ent, wiki, ent_vector in representation_ents:
            if temp_id != id_:
                text_vector =  representation_texts[representation_texts[:][0] == id_] #compute vector representation
                temp_vector = text_vector #remember vector for next iteration (if same id is used)
                temp_id = id_ #remember id for next iteration (if same id is used0)
            else: 
                text_vector = temp_vector #if vector already computed than take temp_vector value

            score = self._compare(
                entity_representation = ent_vector,
                text_representation = text_vector
            )
            scores.append(
                (id_, ent, wiki, score)
            )
        
        #select results
        results = [] 
        for id_, text in texts:
            temp = scores[scores[:][0] == id_] #does not work but place holder
            temp =  sorted(temp, key =lambda element: (element[1], element[3]))#sort on scores
            for ent in list(set(temp[:][1])):
                results.append(
                    temp[temp[:][1] == ent][:self.n_hits_entity]#select n hightest scores per entity match (does not work)
                ) 
        #returns list of tuple    
        return results

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
