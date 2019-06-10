#!/bin/bash

createdb guacamole_db
cat /var/log/docker/initdb.sql | psql -d guacamole_db -f -
psql -c "CREATE USER guacamole_user WITH PASSWORD 'PASSWORD_HERE';" guacamole_db
psql -c "GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA public TO guacamole_user;" guacamole_db
psql -c "GRANT SELECT,USAGE ON ALL SEQUENCES IN SCHEMA public TO guacamole_user;" guacamole_db
