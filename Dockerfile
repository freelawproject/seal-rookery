FROM python:3.8-slim

RUN apt-get update --option "Acquire::Retries=3" --quiet=2 && \
    apt-get install \
        --no-install-recommends \
        --assume-yes \
        --quiet=2 \
        # So we can use Python-slim
        build-essential gcc python-dev git

# Update system and add image conversion
RUN apt-get update
RUN apt-get install -y imagemagick

RUN pip install git+https://github.com/freelawproject/seal-rookery
RUN update-seals -f -v
