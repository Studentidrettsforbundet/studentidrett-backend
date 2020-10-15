FROM docker.elastic.co/elasticsearch/elasticsearch:7.9.2

RUN echo vm.max_map_count=262144 > /etc/sysctl.conf && \
    echo vm.swappiness=0 > /etc/sysctl.conf

RUN bin/elasticsearch-plugin install --batch repository-gcs