FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install -y python2.7-minimal
RUN apt-get install -y python-pip python-dev build-essential
RUN easy_install pip
RUN pip install awscli
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "/bin/bash" ]
ENTRYPOINT [ "./entrypoint.sh" ]
