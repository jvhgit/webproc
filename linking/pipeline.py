### AUTHORS ###
## Clifton Roozendal
## Eduard Bosch
## Floris ten Lohuis
## Jens van Holland

## Version: 1.0.0
## Date: 16-11-2021
## Course: Web Data Processing Systems

### DESCRIPTION ###
# Pipeline class for parsing and processing the data correctly. 
# For better modular development.

#packages
import random
import string
import gzip
import sys 

from part_of_pipeline.clean import Clean
from part_of_pipeline.extract import Extract
from part_of_pipeline.search import Search

#classes
class Pipeline:
    """
    Class *Pipeline*\n
    Takes part_of_pipeline elements and parses it through the pipeline (WARC -> solution format)\n
    TODO: -future- implement multiprocessing/parallelism \n
          (e.g. split large input into chunks or multiple WARC files at the same time)
    """

    def __init__(self, pipeline = [], whitelist = [Clean(), Extract(), Search()]) -> None:
        """
        Initialization function
        Input: \n
        \t pipeline: (list) -> list of tuple pair (name, "part_of_pipeline" object) \n
        \t whitelist: (list) -> list of allowed objects in pipeline\n
        Output: \n
        \t None
        """
        self.pipeline = pipeline
        self.whitelist = whitelist

        #here some extra attributes for clearity
        self.temp_output = [] #do not change
        pass
    
    def _write_to_txt(self, save_to = "temp.txt"):
        """
        Writes results to txt (\\t separated).\n
        Input: \n
        \tsave_to: (str) path + filename.txt default is temp.txt
        Output: \n
        \tNone
        """
        textfile = open(save_to, "w")
        for element in self.temp_output:
            for result in element:
                for k, v in result.items():
                    textfile.write(f'\t{k}\t{v}\n')

        textfile.close()
        pass

    def _split_records(self,stream):
        """
        Splits data into input sequences (from example files)\n
        Input: \n
        \t stream: (str) the whole warc file (text + metadata) \n
        Output: \n
        \thtml text
        """
        payload = ''
        for line in stream:
            if line.strip() == "WARC/1.0":
                yield payload
                payload = ''
            else:
                payload += line
        yield payload

    def parse(self, html_text = None):
        """
        Parse warc file through the pipeline.\n
        Input: \n
        \t html_text: the html-text with entities\n
        Output: \n
        \tNone
        """

        temp = html_text
        for _, part in self.pipeline: temp = part._forward(temp)

        self.temp_output.append(temp) #add the output triple

    def reset(self):
        """
        Resets certain values\n
        Input: \n
        \tNone\n
        Output: \n
        \tNone
        """
        self.temp_output = []

        pass

    def process(self, complete_path = None, save_to = "temp.txt"):
        """
        Process warc file through the pipeline.\n
        Input: \n
        \t complete_path: (str) the complete path to the data (warc.gz) \n
        \t save_to: (str) path + filename.txt default is temp.txt
        Output: \n
        \tNone
        """

        if type(complete_path) == None:
            return "Not a valid input (None)."
        i = 0 #for testing
        with gzip.open(complete_path, 'rt', errors='ignore') as fo:
            for rec in self._split_records(fo):
                self.parse(html_text=rec)
            
                if i ==  5: break #for testing
                i+=1 #for testing
    
        self._write_to_txt(save_to = save_to)
        self.reset()
        pass

    def add(self, name = None, part = None):
        """
        Adds part_of_pipeline object to pipeline.\n
        Input: \n
        \t name: (str) name of part in the pipeline (default is None = random name)\n
        \t part: part_of_pipeline object (default is None = not added to pipeline)
        Output:\n
        \tNone
        """

        if type(name) == type(None): #if no name make random one
            name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

        #check if object is allowed in the pipeline
        if not any([type(acceptable) == type(part) for acceptable in self.whitelist]):
            return f"Not acceptable part. Following parts are whitelisted: {self.whitelist}"

        #add part to pipeline
        pipe_part = (name, part)
        self.pipeline.append(pipe_part)

    def __repr__(self) -> str:
        """
        Prints and checks if pipeline works.\n
        Input: \n
        \tNone\n
        Output:\n
        \tNone
        """
        i = 1
        j = 0
        text = "\n--- Current Pipeline Configuration ---\n\n"
        out_ = ""
        for name, item in self.pipeline:
            temp = f'Step {i}: \'{name}\' -- {item}\n\t---> INPUT: {item.input_} -> OUTPUT: {item.output_}\n\n'
            if (i > 1) & (out_ == item.input_): 
                j+=1
            out_ = item.output_

            i+=1
            text +=temp
        if i == j + 2 : 
            text+="--- Pipeline Chain checked & accepted ---\n\n"
            return text
        else:
            print("Pipeline Chain not accepted. Please check your pipeline.")
            print("Exiting...")
            sys.exit()