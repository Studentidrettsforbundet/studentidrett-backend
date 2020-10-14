FROM docker.elastic.co/elasticsearch/elasticsearch:7.9.2

RUN bin/elasticsearch-plugin install --batch repository-gcs

COPY sysctl.conf ./etc/sysctl.conf.d