FROM python:3.6.6-slim

RUN apt update \
    && apt install -y --no-install-recommends \
       ca-certificates \
       gosu \
       git \
       vim \
       silversearcher-ag \
    && rm -rf /var/lib/apt/lists/* /tmp/*

RUN pip3 install openerp-client-lib>=1.1.2

RUN mkdir /opt/csv/

RUN cd /opt/csv/ \
    && git clone --single-branch https://github.com/tfrancoi/odoo_csv_import \
    && cd odoo_csv_import \
    && git checkout b453f43e63c96dfefc3a8a2642d674775b289bb4 \
    && python setup.py develop \
    && cd ..

# COPY ./data /opt/data/

# COPY ./project /opt/project/

# RUN chmod +x /opt/project/*.sh

# RUN chown -R www-data.www-data /opt/project

# RUN chown -R www-data.www-data /opt/data

USER www-data

LABEL "it.linkgroup.name"="Z6 Migrate"
