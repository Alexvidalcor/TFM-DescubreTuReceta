FROM debian:latest
LABEL maintainer="Alexvidalcor alejavid@ucm.es"

WORKDIR /home/

COPY scrapping_images.py scripts/
COPY values_scrapping_images.py scripts/
# COPY input_scrapping_images.csv scripts/

ENV CHROME_VERSION=103.0.5060.53
ENV GECKO_VERSION=v0.31.0

RUN apt update \
    && apt install -y \
        python3-pip \
        chromium \
        firefox-esr \
        unzip \
        wget \
        zip \
    && pip install \
        pandas \
        selenium \
        webdriver-manager

RUN wget "https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip \
    && rm chromedriver_linux64.zip \
    && mv chromedriver /usr/bin

RUN wget "https://github.com/mozilla/geckodriver/releases/download/${GECKO_VERSION}/geckodriver-${GECKO_VERSION}-linux64.tar.gz" \
    && tar -xf geckodriver-${GECKO_VERSION}-linux64.tar.gz \
    && rm geckodriver-${GECKO_VERSION}-linux64.tar.gz \
    && mv geckodriver /usr/bin