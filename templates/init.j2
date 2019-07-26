#!/bin/bash

createdb guacamole_db
psql -d guacamole_db -f - < /var/log/docker/initdb.sql
psql -c "CREATE USER guacamole_user WITH PASSWORD '{{ postgres_password }}';" guacamole_db
psql -c "GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA public TO guacamole_user;" guacamole_db
psql -c "GRANT SELECT,USAGE ON ALL SEQUENCES IN SCHEMA public TO guacamole_user;" guacamole_db
