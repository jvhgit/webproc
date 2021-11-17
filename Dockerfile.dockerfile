#get image
FROM karmaresearch/wdps_assignment
# USER root

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir spacy ipykernel warcio html2text bs4 numpy elasticsearch

RUN python3 -m spacy download en_core_web_sm
RUN python3 -m spacy download en_core_web_lg

#run line below first before other
#docker run -ti --privileged centos sysctl vm.max_map_count=262144 
#docker run -ti --karmaresearch/wdps_assignment vm.max_map_count=262144 
# docker run -ti -v C:/Users/Jensv/git/webproc:/app/assignment -p 9200:9200 karmaresearch/wdps_assignment
# docker run -ti --privileged webproc sysctl -w vm.max_map_count=262144
# docker run -ti -v C:/Users/Jensv/git/webproc:/app/assignment -p 9200:9200 webproc
