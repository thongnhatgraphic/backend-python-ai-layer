FROM postgres:15

RUN apt-get update

RUN apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-15

RUN git clone https://github.com/pgvector/pgvector.git

RUN cd pgvector && make && make install