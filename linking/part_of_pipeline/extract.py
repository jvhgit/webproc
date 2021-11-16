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
import spacy
import re

class Extract:
    # class information
    input_ = "str:clean"
    output_ = "list:amb_entities"

    def __init__(self, nlp_model = 'en_core_web_sm', blacklist_ne = ["CARDINAL"] ) -> None:
        """
        Initialisation function\n
        Input: \n
        \t nlp_model: (str) small NER model: "en_core_web_sm" (default), large NER model: "en_core_web_lg"\n
        \t blacklist_ne: (list) list of blacklisted Named Entity tags, these will be removed from the set.
        Output: \n
        \tNone
        """
        self.nlp = spacy.load(nlp_model)
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

    def extract(self, text):
        """
        Extracts the entities of a given text using Spacy model\n
        Input: \n
        \t text: (str) clean (non-html) text with entities\n
        Output: \n
        \tlist of (cleaned) entities
        """
        #for computationally benefit, we only use the NER of the spacy pipe line so we disable everything else
        doc = self.nlp(text ,disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])
        entities = []
        for ent in doc.ents:
            if ent.label_ not in self.blacklist_ne: 
                #if entity is allowed clean it with some regex rules
                entities.append(self._clean_entity(str(ent)))
            else: continue

        return entities
        # return zip(doc.ents, [i.label_ for i in doc.ents]) 
    
    def _forward(self, text):
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
        return self.extract(text = text)

