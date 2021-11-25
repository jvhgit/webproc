### AUTHORS ###
## Clifton Roozendal
## Eduard Bosch
## Floris ten Lohuis
## Jens van Holland

## Version: 1.0.0
## Date: 16-11-2021
## Course: Web Data Processing Systems

### DESCRIPTION ###
## Extract class, extracts the enities from given text

## packages
import multiprocessing
import spacy
import re
import time
import pandas as pd
import difflib

class Extract:
    # class information
    input_ = "str:clean"
    output_ = "list:amb_entities"

    def __init__(self, nlp_model = 'en_core_web_sm', blacklist_ne = ["CARDINAL", "DATE", "TIME", "MONEY", "PERCENT", "QUANTITY", "ORDINAL"] ) -> None:
        """
        Initialisation function\n
        Input: \n
        \t nlp_model: (str) small NER model: "en_core_web_sm" (default), large NER model: "en_core_web_lg"\n
        \t blacklist_ne: (list) list of blacklisted Named Entity tags, these will be removed from the set.
        Output: \n
        \tNone
        """
        self.nlp = spacy.load(nlp_model)
        # self.nlp.get_pipe('ner').moves.prohibit_action(u'U-DATE')
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
        return entity

    def _get_ents(self, label):  
        if label in self.blacklist_ne: 
            return None
        return label

    def extract(self, corpus, ids, batch_size =8):
        """
        Extracts the entities of a given text using Spacy model\n
        Input: \n
        \t text: (str) clean (non-html) text with entities\n
        Output: \n
        \tlist of (cleaned) entities
        """
        # print(len(corpus))
        #for computationally benefit, we only use the NER of the spacy pipe line so we disable everything else
        #do not set n_process = -1!!
        #below returns generator works best with batch_size of 8
        docs = self.nlp.pipe(corpus, n_process = 8 ,disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"], batch_size=batch_size)
        num_docs = len(corpus)

        ents,labels = [], []
        i = 0
        for doc in docs:
            # print("OK")
            ents.append(list(doc.ents))
            labels.append(list(map(lambda ent: ent.label_, doc.ents )))
            i+=1
            if i %100 ==0:
                print(f"\t Processed {i}/{num_docs} documents")
        print(f"\t Processed {num_docs}/{num_docs} documents")

        #make dataframe with found entities and entities types    
        data = pd.DataFrame(
            {
                "ents" : ents, 
                "labels" : labels,
                "ids":ids
            }
        )

        #unpack the lists in the pandas columns
        data = data.set_index(['ids']).apply(pd.Series.explode).reset_index()
        
        #filters/cleans the found entities
        data = data[~data.labels.isin(self.blacklist_ne)].dropna().reset_index(drop = True) #remove ents of specific types
        data.ents = data.ents.astype(str) #cast from spacy.Span to str
        # data = data.drop_duplicates(['ids', 'ents']).reset_index(drop = True) #drop whole row duplicates
        data = data.drop_duplicates().reset_index(drop = True) #drop whole row duplicates
        data.ents = data.ents.apply(self._clean_entity) #some regex to remove some specific chars
        temp = []
        i = 0
        for _, g in data.groupby('ids'):
            i+=1
            if i %100 ==0:
                print(f"\t Cross-referenced entities for {i}/{num_docs} documents")
            g['temp_id'] = list(range(len(g)))
            g['text_similar'] = g.temp_id.apply(lambda row: len(difflib.get_close_matches(g[g.temp_id == row].ents.values[0], list(g[g.temp_id > row].ents), cutoff = 0.35)) > 0)
            temp.append(g)

        data = temp[0].append(temp[1:])
        data.to_csv("tst.csv")
        print(len(data))
        data = data[data.text_similar == False].reset_index(drop = True)
        print(len(data))
        return data[['ids', 'ents']]

 
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
        # it seems redudant but _forward is universal parse functions in the pipeline
        print("--> Extracting entities from text <--")
        records['amb_entities'] = self.extract(corpus = records['text'], ids = records['id'], batch_size = records['batch_size_NER'])
        print("<STATUS: DONE>\n")
        # print(instance['entities'])
        return records




