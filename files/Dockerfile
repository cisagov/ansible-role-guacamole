FROM postgres
MAINTAINER Kyle Evers <Kyle.Evers@trio.dhs.gov>
ENV POSTGRES_PASSWORD="PASSWORD_HERE"

USER postgres

COPY initdb.sql /var/log/docker/initdb.sql
# .sh and .sql files copied to docker entrypoint will be run
COPY init.sh /docker-entrypoint-initdb.d/init.sh
