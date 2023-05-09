FROM python:3.8-slim AS build
WORKDIR /src
COPY requirements.txt .
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential gcc\
  && pip install --user -r requirements.txt --no-warn-script-location

COPY setup.py .
COPY canalyzer/ canalyzer/
RUN pip install --user .

FROM python:3.8-slim AS runtime
ENV WKHTMLTOPDF_VERSION=0.12.6-1
COPY --from=build /root/.local /root/.local
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential \
  gcc \
  jq \
  fontconfig libfreetype6 libjpeg62-turbo libpng16-16 \
  libx11-6 \
  libxcb1 \
  libxext6 \
  libxrender1 \
  xfonts-75dpi \
  xfonts-base \
  wget \
  && wget -O wkhtmltopdf.deb https://github.com/wkhtmltopdf/packaging/releases/download/${WKHTMLTOPDF_VERSION}/wkhtmltox_${WKHTMLTOPDF_VERSION}.buster_amd64.deb \
  && dpkg -i wkhtmltopdf.deb \
  && rm -f wkhtmltopdf.deb \
  && apt-get purge -y wget
WORKDIR /app
COPY appsettings.json /app/appsettings.json
COPY styles.css /app/styles.css

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH
LABEL maintainer="José Truyol <jose.truyol@indimin.com>"
LABEL company="INDIMIN SPA"
LABEL country="CHILE"
