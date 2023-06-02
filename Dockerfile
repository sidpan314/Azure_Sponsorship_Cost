FROM python:3.8-slim AS build
WORKDIR /src
COPY requirements.txt .
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential gcc \
  && apt-get install -y apt-utils html2text \
  && python -m venv /venv \
  && /venv/bin/pip install -r requirements.txt --no-warn-script-location \
  && /venv/bin/pip install azure-storage-blob

COPY setup.py .
COPY canalyzer/ canalyzer/
RUN /venv/bin/pip install .
RUN /venv/bin/pip install html-to-text

RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates curl gnupg lsb-release \
  && curl -sL https://aka.ms/InstallAzureCLIDeb | bash

FROM python:3.8-slim AS runtime
ENV WKHTMLTOPDF_VERSION=0.12.6-1
COPY --from=build /venv /venv
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  fontconfig libfreetype6 libjpeg62-turbo libpng16-16 \
  libx11-6 \
  libxcb1 \
  libxext6 \
  libxrender1 \
  xfonts-75dpi \
  xfonts-base \
  wget \
  curl \
  html2text \
  jq \
  && wget -O wkhtmltopdf.deb https://github.com/wkhtmltopdf/packaging/releases/download/${WKHTMLTOPDF_VERSION}/wkhtmltox_${WKHTMLTOPDF_VERSION}.buster_amd64.deb \
  && dpkg -i wkhtmltopdf.deb \
  && rm -f wkhtmltopdf.deb \
  && apt-get purge -y wget \
  && /venv/bin/pip install markdown
WORKDIR /app
COPY styles.css /app/styles.css
COPY appsettings.json /app/appsettings.json

# Make sure scripts in the virtual environment are usable:
ENV PATH=/venv/bin:$PATH
LABEL maintainer="José Truyol <jose.truyol@indimin.com>"
LABEL company="INDIMIN SPA"
LABEL country="CANADA"
