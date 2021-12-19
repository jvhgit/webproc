### AUTHORS ###
## Clifton Roozendal
## Floris ten Lohuis
## Jens van Holland

## Version: 1.1.0
## Date: 19-12-2021
## Course: Web Data Processing Systems

### DESCRIPTION ###
## Extract class, extracts the enities from given text

## packages
import spacy
import re
import pandas as pd
import difflib
import time
import multiprocessing

class Extract:
    # class information
    input_ = "str:clean"
    output_ = "list:amb_entities"

    def __init__(self, nlp_model = 'en_core_web_sm', sim_cutoff_NER=0.35, blacklist_ne_label = ["CARDINAL", "DATE", "TIME", "MONEY", "PERCENT", "QUANTITY", "ORDINAL"], blacklist_ne = [""," ", "GMT Server","GMT",] ) -> None:
        """
        Initialisation function\n
        Input: \n
        \t nlp_model: (str) small NER model: "en_core_web_sm" (default), large NER model: "en_core_web_lg"\n
        \t blacklist_ne: (list) list of blacklisted Named Entity tags, these will be removed from the set.
        Output: \n
        \tNone
        """
        self.nlp = spacy.load(nlp_model)
        self.sim_cutoff_NER = sim_cutoff_NER
        # self.nlp.get_pipe('ner').moves.prohibit_action(u'U-DATE')
        self.blacklist_ne_label = blacklist_ne_label
        self.blacklist_ne = blacklist_ne

        pass
    
    def _clean_entity(self,entity):
        """
        Cleans an entity using regex rules\n
        TODO:extend rules 
        Input: \n
        \t entity: (str) entity found by the extraction \n
        Output: \n
        \tEntity which is cleaned with some regex
        """
        entity = re.sub(r"\(/.+?\s", " ", entity)
        entity = re.sub(r"#|\*", " ", entity)
        entity = re.sub(r"\s{1,}", " ", entity)
        #entity = re.sub('[^A-Za-z0-9 ]+', '', entity)
        return entity

    def _extract_entities(self, doc):
        """
        Cleans an entity using regex rules\n
        TODO:extend rules 
        Input: \n
        \t doc: (str) doc found by the nlp extraction \n
        Output: \n
        \tCleaned list of entities
        """
        ents_doc = []
        for ent in doc.ents:
            if ent.label_ not in self.blacklist_ne_label:
                ent_str = self._clean_entity(str(ent))
                if ent_str not in self.blacklist_ne and ent_str not in ents_doc and len(difflib.get_close_matches(ent_str, ents_doc, cutoff=self.sim_cutoff_NER)) == 0:
                    ents_doc.append(ent_str)
        return ents_doc

    # def _extract_entities_single(self, string):
    #     ents_doc = []
    #     doc = self.nlp(string)
    #     for ent in doc.ents:
    #         if ent.label_ not in self.blacklist_ne_label:
    #             ent_str = self._clean_entity(str(ent))
    #             if ent_str not in self.blacklist_ne and ent_str not in ents_doc and len(difflib.get_close_matches(ent_str, ents_doc, cutoff=self.sim_cutoff_NER)) == 0:
    #                 ents_doc.append(ent_str)
    #     return ents_doc


    def extract(self, corpus, ids, batch_size =8, n_threads = 1):
        """
        Extracts the entities of a given text using Spacy model\n
        Input: \n
        \t text: (str) clean (non-html) text with entities\n
        Output: \n
        \tlist of (cleaned) entities
        """

        #for computationally benefit, we only use the NER of the spacy pipe line so we disable everything else
        #do not set n_process = -1!!
        #below returns generator works best with batch_size of 8
        docs = self.nlp.pipe(corpus, n_process = n_threads ,disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"], batch_size=batch_size)
        
        #single threaded
        start = time.time()

        i = 0
        num_docs = len(corpus)
        ents = []
        for doc in docs:
            i+=1
            if i %100 ==0:
                print(f"\t Extracted entities for {i}/{num_docs} documents")
            ents.append(self._extract_entities(doc))

        sec = round(time.time() - start)
        print(f"\t NER completed in {sec} seconds ")

        # Multi-threading was not faster in this case...

        # #multi threaded
        # start = time.time()
        # with multiprocessing.Pool(n_threads) as p:
        #     ents = p.map(self._extract_entities, docs)
        # sec = round(time.time() - start)
        # print(f"\t NER multi-threaded completed in {sec} seconds ")

        # #multi threaded 2
        # start = time.time()
        # with multiprocessing.Pool(n_threads) as p:
        #     ents = p.map(self._extract_entities_single, corpus)
        # sec = round(time.time() - start)
        # print(f"\t NER multi-threaded completed in {sec} seconds ")

        # sec = round(time.time() - start)
        # print(f"\t NER completed in {sec} seconds ")

        # make dataframe with found entities and entities types    
        data = pd.DataFrame(
            {
                "ents" : ents, 
                "ids":ids
            }
        )

        #unpack the lists in the pandas columns
        data = data.set_index(['ids']).apply(pd.Series.explode).reset_index()

        return data
 
    def _forward(self, records):
        """
        Dummy function for streamlining the pipeline\n
        Input: \n
        \t text: (str) clean (non-html) text with entities\n
        Output: \n
        \tlist of (cleaned) entities
        """
        # this is used by the pipeline
        # make sure this returns the acceptable output
        #  i
        # *t seems redudant but _forward is universal parse functions in the pipeline
        print("--> Extracting entities from text <--")
        extracted = self.extract(
            corpus = records['text'], 
            ids = records['id'], 
            batch_size = records['batch_size_NER'],
            n_threads=records['n_threads'])

        extracted.to_csv('/app/assignment/results/extracted_results.csv')

        records['amb_entities'] = extracted

        print("<STATUS: DONE>\n")
        return records