FROM postgres

COPY schema/init.sql /docker-entrypoint-initdb.d

ENV POSTGRES_USER cloud
ENV POSTGRES_PASSWORD cloud
ENV POSTGRES_DB cloudb

EXPOSE 5432
