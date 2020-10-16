FROM python:3.8-slim

#Copy project to Docker image
COPY . /project/
WORKDIR /project

#Install requirements
RUN pip install -r requirements.txt

# Update system and add image conversion
RUN apt-get update
RUN apt-get install -y imagemagick

# Install seal-rookery
RUN python setup.py install

# Update and generate seals
RUN update-seals -f -v
