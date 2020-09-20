FROM ubuntu:18.04

# Configuração da timezone
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN date

# Instalação dos pacotes necessários
RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install --fix-missing

RUN apt-get install -y \
    vim \
    python3.6 \
    python3-pip \
    python3-dev \
    cron

RUN apt-get install -y \
    libpq-dev \
    x11-utils \
    xvfb


RUN pip3 install --upgrade pip
RUN pip3 install pipenv
RUN pip3 install supervisor

COPY config/supervisor/supervisord.conf /etc/supervisord.conf
COPY config/supervisor/stop-supervisor.sh /opt/reglare/stop-supervisor.sh

ARG OITO_VERSAO=0.0.1
ARG APP_NAME
ARG OITO_APP

ENV APP_NAME=${APP_NAME}
ENV OITO_VERSAO=${OITO_VERSAO}

# Variáveis de ambiente para python com UTF-8
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY src/resources/cron-crawler /etc/cron.d/cron-crawler

RUN chmod +x /etc/cron.d/cron-crawler

RUN apt-get install -y \
    fonts-liberation \
    libappindicator3-1 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo2 \
    libcups2 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libxcursor1 \
    libxss1 \
    wget \
    xdg-utils \
    libasound2 \
    util-linux \
    wkhtmltopdf \
    xvfb

COPY src/resources/wkhtmltopdf.sh /usr/bin/wkhtmltopdf.sh

RUN chmod a+x /usr/bin/wkhtmltopdf.sh

RUN ["mv", "/usr/bin/wkhtmltopdf", "/usr/bin/wkhtmltopdf_original"]

RUN chmod a+x /usr/bin/wkhtmltopdf_original

RUN ["ln", "-s", "/usr/bin/wkhtmltopdf.sh", "/usr/local/bin/wkhtmltopdf"]

RUN ["ln", "-s", "/usr/bin/wkhtmltopdf.sh", "/usr/bin/wkhtmltopdf"]

COPY src /opt/reglare/crawler-projudi

WORKDIR /opt/reglare/crawler-projudi

RUN dpkg -i resources/google-chrome-stable_current_amd64.deb

RUN ["pipenv", "--python", "3.6", "--site-packages"]

RUN ["pipenv", "run", "pip", "install", "-e", "."]

# "--deploy", arg utilizado abaixo quando estiver estável
RUN ["pipenv", "install", "--deploy", "--system"]

CMD ["supervisord", "--nodaemon", "--configuration", "/etc/supervisord.conf"]