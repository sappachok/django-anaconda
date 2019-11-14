FROM python:3.7

RUN apt-get update \
    && apt-get -y install unzip \
    && apt-get -y install libaio-dev \
    && mkdir -p /opt/data/api

ADD ./oracle-instantclient/ /opt/data
ADD ./install-instantclient.sh /opt/data

# ADD ./requirements.txt /opt/data

WORKDIR /opt/data

ENV ORACLE_HOME=/opt/oracle/instantclient
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME

ENV OCI_HOME=/opt/oracle/instantclient
ENV OCI_LIB_DIR=/opt/oracle/instantclient
ENV OCI_INCLUDE_DIR=/opt/oracle/instantclient/sdk/include

# INSTALL INSTANTCLIENT AND DEPENDENCIES
RUN ./install-instantclient.sh

ENV APP_ROOT /src
ENV CONFIG_ROOT /config

RUN mkdir ${CONFIG_ROOT}
COPY /app/requirements.txt ${CONFIG_ROOT}/requirements.txt
RUN pip install -r ${CONFIG_ROOT}/requirements.txt

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}

ADD /app/ ${APP_ROOT}