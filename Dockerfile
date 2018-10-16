FROM ubuntu:16.04
RUN apt-get update;apt-get install -y python2.7-minimal;apt-get install -y python-pip python-dev build-essential;easy_install pip;pip install awscli
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "./entrypoint.sh" ]
