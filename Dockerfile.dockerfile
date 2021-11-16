#get image
FROM karmaresearch/wdps_assignment
USER root

#run line below first before other
#docker run -ti --privileged centos sysctl vm.max_map_count=262144 
#docker run -ti -v C:/Users/Jensv/git/webproc:/app/assignment -p 9200:9200 karmaresearch/wdps_assignment
