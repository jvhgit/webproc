#get image
FROM karmaresearch/wdps_assignment
# USER root

RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir spacy ipykernel warcio html2text bs4 numpy elasticsearch

RUN python3 -m spacy download en_core_web_sm
RUN python3 -m spacy download en_core_web_lg

#run line below first before other
# RUN docker run -ti --privileged centos sysctl vm.max_map_count=262144 
# RUN docker run -ti --karmaresearch/wdps_assignment vm.max_map_count=262144 
# RUN docker run -ti -v D:/University/Web Data Processing Systems/Data/assignment-all-splitted/assignment-all-splitted/assignment -p 9200:9200 karmaresearch/wdps_assignment
# RUN docker run -ti --privileged webproc sysctl -w vm.max_map_count=262144
# RUN docker run -ti -v D:/University/Web Data Processing Systems/Data/assignment-all-splitted/assignment-all-splitted/assignment -p 9200:9200 webproc
