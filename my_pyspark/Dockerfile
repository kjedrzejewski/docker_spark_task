FROM "bitnami/spark:latest"
USER root
RUN apt-get update && apt-get install -y gnupg
RUN set -ex; \
    key='A4A9406876FCBD3C456770C88C718D3B5072E1F5'; \
    export GNUPGHOME="$(mktemp -d)"; \
    gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "$key"; \
    gpg --batch --export "$key" > /etc/apt/trusted.gpg.d/mysql.gpg; \
    gpgconf --kill all; \
    rm -rf "$GNUPGHOME"; \
    apt-key list > /dev/null
RUN pip install pandas
RUN pip install PyMySQL
RUN pip install sqlalchemy
USER 1001
