### AUTHORS ###
## Clifton Roozendal
## Floris ten Lohuis
## Jens van Holland

## Version: 1.0.0
## Date: 26-11-2021
## Course: Web Data Processing Systems

### DESCRIPTION ###
#Clean class for cleaning html text with bs4 or html2text

## packages
import html2text
from bs4 import BeautifulSoup
import multiprocessing
class Clean:
    # class information
    input_ = "str:html"
    output_ = "str:clean"

    def __init__(self, option = 2) -> None:
        """
        Initialisation function\n
        Input: \n
        \t option: (int) parsing option 1: html2text (default), 2: bs4 \n
        Output: \n
        \tNone
        """

        self.option = option 
        pass

    def clean(self, text):
        """
        Cleans html text using given configuration. \n
        Input: \n
        \t text: (str) html text of a given warc file \n
        Output: \n
        \t(mostly) cleaned text (in terms of html lingo)
        """
        if self.option == 1:    return html2text.html2text(str(text))
        elif self.option == 2:  return BeautifulSoup(text, features="html.parser").get_text()
        # elif #ption == 3:
            #maybe make some custom parser with regex or some other package#
        pass 
    
    def _forward(self, records):
        """
        Dummy function for streamlining the pipeline\n
        Input: \n
        \t text: (str) html text of a given warc file  \n
        Output: \n
        \t(mostly) cleaned text (in terms of html lingo)
        """
        # this is used by the pipeline
        # make sure this returns the acceptable output
        # it seems redudant but _forward is universal parse functions in the pipeline
        print("--> Cleaning HTML-text <--")
        with multiprocessing.Pool(records['n_threads']) as p:
                temp = p.map(self.clean, records['html_text'] )
        print("<STATUS: DONE>\n")
        records['text'] = temp

        return records

