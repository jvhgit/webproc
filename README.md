# Content

In this repository an entity linker is (partly) implemented.
In short, there are a few key components for the entity linking, namely:<br>
- The _linking/pipeline.py_ for the **Pipeline** class, which uses classes from other scripts and parses the input (WARC files) through it.
- The _linking/main.py_ for running the entity linker from command line (basically what run.sh runs).
- The _linking/part_of_pipeline/clean.py_ for the **Clean** class, this cleans the html-text.
- The _linking/part_of_pipeline/extract.py_ for the **Extract** class, this extract the entities from the "cleaned" text.
- The _linking/part_of_pipeline/search.py_ for the **Search** class, this searches for the wikilinks of the entities using ElasticSearch.
- The _linking/part_of_pipeline/decision.py_ for the **Decision** class, this class is used for disambiguation (dummy class since there is no actual implementation).
Each script can be adjusted as long the input is the same (i.e. text, list, dict, etc). 

The entire pipeline is called from _main.py_. the file can be run with several different arguments (all of which have a default value, so the file can also be run without setting any arguments), namely:

Argument &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  Default Value:Description<br>
data_dir &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	    /app/assignment/data/sample.warc.gz : Directory of the xxxx.warc.gz file which will be used to for the entity linking.<br>
clean_text &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     1                                  : The cleaning procedure which is used: 1: html2text (default)2: BeautifulSoup:html.parser<br>
extract_model&nbsp;&nbsp;&nbsp;   en_core_web_sm	:                    The model which is used to extract:en_core_web_sm (default) en_core_web_lg (not included but can be downloaded after the build)<br>
query_size_ES&nbsp;&nbsp;&nbsp;&nbsp;  20	          :                      The max number of hits a query can return<br>
search_ES  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     normal	           :                 Please do not alter this - the 'fast' implementation is very buggy<br>
batch_size_NER&nbsp;&nbsp; 8	   :                             The NER model parses n samples in parallel. We found 8 to be the best value (on 8 threads, intel i7, 16gb RAM)<br>
n_threads&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   	8	                          :      The number of threads to use.Please be carefull - do not set to -1, this will go wrong(!)<br>
sim_cutoff_NER&nbsp;&nbsp;	0.35	    :                        To reduce the number of queries = entities, we compute similarity.cross-referencing scores (no time to implement that in parallel) and use a threshold (last one is kept)

An extra documentation/rationalisation file is added for clarification (WDPS - Assignment 1 - Entity Linking - Group 50).

# Installation

We assume that Elasticsearch and Trident are installed locally (we build from the given Docker and installed Elasticsearch and Trident locally). <br>The next installation steps are also stated in the Dockerfile.dockerfile:

  1) Build Image the Dockerfile (in VSCode with Docker extension; rightclick on file and lowest option "Build Image").<br> Make sure that the parent folder is called "webproc" (that is what we used during development). This will install the needed packages. 
   
  2) Next run the previous build and add volume to it, for example,<br>
   `docker run -ti -v C:/Users/Jensv/git/webproc:/app/assignment -p 9200:9200 webproc`

  3) Next, run the following command in the Linux shell (in the container) to start the elasticsearch server:<br>
   `./assets/elasticsearch-7.9.2/bin/elasticsearch -d`
   <br>Before going on make sure the server is actually available by checking: https://localhost:9200/ .
   
  4) At last, to run the main script with default settings (as described above) run the following command:  
  `python3 linking/main.py` <br>
  Use the arguments to change input or output file(names). See main.py or above for the arguments and there values.

<!-- #2) Run the container and add volume (run below in powershell) (example below)
# we assume that elasticsearch and trident are local
# docker run -ti -v C:/Users/Jensv/git/webproc:/app/assignment -p 9200:9200 webproc

#3) Run following command in linux container shell to start elasticsearch server (takes a minute or 2)
# ./assets/elasticsearch-7.9.2/bin/elasticsearch -d
# you can verify the start by going to https://localhost:9200/

#4) To run the entity linker, to the following:
# python3 linking/main.py
# this runs with all the default arguments
# for more information on the commandline arguments see: linking/main.py -->
<!-- First run the Dockerfile (in VSCode) + commented statements in that file. (Make sure you do not have a container running already).<br>
It is assumed that ElasticSearch+Trident is on local drive.<br>
Next run in the container (VSCode remote development advised):<br>
(in this order!)<br> 
- sh run_dependencies.sh
- sh run_model_download.sh
- sh run_server.sh
- sh run.sh <br>

*OR*
Build the Dockerfile.dockerfile, start the container (docker run -ti etc etc) and run:
- sh run_server.sh
- sh run.sh <br> -->
