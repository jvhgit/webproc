First run the Dockerfile (in VSCode) + commented statements in that file. (Make sure you do not have a container running already).<br>
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
- sh run.sh <br>

In short, there are a few key components for the entity linking, namely:<br>
- The _linking/pipeline.py_ for the **Pipeline** class, which uses classes from other scripts and parses the input (WARC files) through it.
- The _linking/main.py_ for running the entity linker from command line (basically what run.sh runs).
- The _linking/part_of_pipeline/clean.py_ for the **Clean** class, this cleans the html-text.
- The _linking/part_of_pipeline/extract.py_ for the **Extract** class, this extract the entities from the "cleaned" text.
- The _linking/part_of_pipeline/search.py_ for the **Search** class, this searches for the wikilinks of the entities using ElasticSearch.

Each script can be adjusted as long the input is the same (i.e. text, list, dict, etc). 

The entire pipeline is called from _main.py_. the file can be run with several different arguments (all of which have a default value, so the file can also be run without setting any arguments), namely:

Argument        Default Value	                    Description
data_dir	    /app/assignment/data/sample.warc.gz Directory of the xxxx.warc.gz file which will be used to for the entity linking.
clean_text      1                                   The cleaning procedure which is used:\n\t1: html2text (default)\n\t2: BeautifulSoup:html.parser
extract_model   en_core_web_sm	                    The model which is used to extract:\n\ten_core_web_sm (default)\n\ten_core_web_lg
query_size_ES   15	                                The max number of hits a query can return
search_ES       normal	                            Please do not alter this - the 'fast' implementation is very buggy
batch_size_NER  8	                                The NER model parses n samples in parallel.\nWe found 8 to be the best value (on 8 threads, intel i7, 16gb RAM)
n_threads   	1	                                The number of threads to use.\nPlease be carefull - do not set to -1, this will go wrong(!)
sim_cutoff_NER	0.35	                            To reduce the number of queries = entities, we compute similarity.cross-referencing scores (no time to implement that in parallel) and use a threshold (last one is kept)

Running time is an issue for some part - in next versions some things might change due to efficiency and parallelism.  