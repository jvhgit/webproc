### AUTHORS ###
# Clifton Roozendal
# Floris ten Lohuis
# Jens van Holland

## Course: Web Data Processing Systems

### DESCRIPTION ###
#Decision class, uses trident to disambiguate search results

## Version: 2.0.0
## Date: 24-12-2021

import trident
import json
import pandas as pd
import re

class Decision:
    # class information
    input_ = "dict:amb_entities"
    output_ = "list:disamb_entities"

#Note: the following entities are available (where some have of course already been removed during extract)
# PERSON:      People, including fictional.
# NORP:        Nationalities or religious or political groups.
# FAC:         Buildings, airports, highways, bridges, etc.
# ORG:         Companies, agencies, institutions, etc.
# GPE:         Countries, cities, states.
# LOC:         Non-GPE locations, mountain ranges, bodies of water.
# PRODUCT:     Objects, vehicles, foods, etc. (Not services.)
# EVENT:       Named hurricanes, battles, wars, sports events, etc.
# WORK_OF_ART: Titles of books, songs, etc.
# LAW:         Named documents made into laws.
# LANGUAGE:    Any named language.
# DATE:        Absolute or relative dates or periods. -REMOVED
# TIME:        Times smaller than a day. -REMOVED
# PERCENT:     Percentage, including ”%“. -REMOVED
# MONEY:       Monetary values, including unit. -REMOVED
# QUANTITY:    Measurements, as of weight or distance. -REMOVED
# ORDINAL:     “first”, “second”, etc. -REMOVED
# CARDINAL:    Numerals that do not fall under another type. -REMOVED

    def __init__(self, 
                    ent_label_mapping = {
                        "EVENT":["Q1656682","Q22964785"],
                        "FAC":["Q41176","Q1248784", "Q269949","Q12280","Q25297630","Q34442"],
                        "GPE":["Q5107","Q6256","Q7275","Q515","Q35657","Q3957"],
                        "LANGUAGE":["Q34770","Q315"],
                        "LAW":["Q7748"],
                        "LOC":["Q8502","Q9430","Q23397","Q4022"],
                        "NORP":["Q231002","Q7278","Q2742167"],
                        "ORG":["Q43229","Q783794","Q178706"],
                        "PERSON":["Q5","Q95074","Q97498056"],
                        "PRODUCT":["Q42889","Q15401930","Q2095","Q25403900"],
                        "WORK_OF_ART":["Q838948"]
                    }
                    ) -> None:
        """
        Initialisation function\n
        Input: \n
        \tNone\n
        Output: \n
        \tNone
        """
        KBPATH='assets/wikidata-20200203-truthy-uri-tridentdb'
        self.trident_db = trident.Db(KBPATH)
        self.ent_label_mapping = ent_label_mapping

        pass

    def _create_query(self, ent, label_wde):
        return "PREFIX wde: <http://www.wikidata.org/entity/> "\
        "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "\
        "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "\
        "select ?s where {" + ent + " wdp:P31/wdp:P279* wde:" + label_wde + "}"# P31: instance of, P279: subclass of

    def _query_match(self, ent, label_wde):
        query = self._create_query(ent, label_wde)
        results = self.trident_db.sparql(query)
        json_results = json.loads(results)
        return True if json_results["results"]["bindings"] else False

    def _decide_for_entity(self, wikilinks):
        if wikilinks.count == 1:
            return wikilinks

        # try to find an entity where the labels match
        for _, wikilink in wikilinks.iterrows():
            hit = wikilink['hit_id']
            ent_label = wikilink['ent_label']
            if ent_label in self.ent_label_mapping.keys():
                for label_wde in self.ent_label_mapping[ent_label]:
                    if self._query_match(hit, label_wde):
                        return wikilink

        # if no label found, return the first one (as this had the highest score in elastic search)
        return wikilinks.iloc[:1]

    def _decide_for_warcid(self, wikilinks):
        if wikilinks.count == 1:
            return wikilinks

        results = pd.DataFrame(columns = wikilinks.columns)
        for _, wikilinks_for_ent in wikilinks.groupby('ent'):
            filtered_wikilink = self._decide_for_entity(wikilinks_for_ent)
            results = results.append(filtered_wikilink)

        return results

    def _decide(self, wikilinks):

        results = pd.DataFrame(columns = wikilinks.columns)
        for _, wikilinks_for_warcid in wikilinks.groupby('warc_id'):
            filtered_wikilinks = self._decide_for_warcid(wikilinks_for_warcid)
            results = results.append(filtered_wikilinks)

        return results

    def _transform_format(self, wikilinks):
        if wikilinks.empty:
            results = []
        else:
            results =  wikilinks['warc_id'] + '\t' + wikilinks['label'] + '\t'+ wikilinks['hit_id'] + '\n'
            results.values.tolist()

        return pd.DataFrame({"temp_output" : set(results)})

    def decide(self, wikilinks):
        """
        Dummy function for streamlining the pipeline\n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tresults of the disambiguated entities (list)
        """
        
        results = self._decide(wikilinks)
        results = self._transform_format(results)

        return results
    
    def _forward(self, records):
        """
        Dummy function for streamlining the pipeline\n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tresults of the disambiguated entities (list)
        """
        # this is used by the pipeline
        # make sure this returns the acceptable output
        # it seems redudant but _forward is universal parse function in the pipeline
        print("--> Disambiguating entities <--")
        records['disambig_entities'] = self.decide(records['wiki_links'])

        print("<STATUS: DONE>\n")

        if records['output_intermediates']:
            pd.DataFrame(
                {
                    "decision_results" : records['disambig_entities']
                }
            ).to_csv(records['output_folder'] + '/decision_results.csv')

        return records