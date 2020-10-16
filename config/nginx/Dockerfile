FROM nginx:latest

# init.sh converted to UNIX
RUN apt-get update && apt-get install -y dos2unix
COPY init.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/init.sh
RUN dos2unix /usr/local/bin/init.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/

# ssh
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
    && apt-get install -y --no-install-recommends dialog \
    && apt-get update \
	&& apt-get install -y --no-install-recommends openssh-server \
	&& echo "$SSH_PASSWD" | chpasswd

COPY sshd_config /etc/ssh/

EXPOSE 2222

COPY nginx.conf /etc/nginx/nginx.conf

CMD ["/usr/local/bin/init.sh"]