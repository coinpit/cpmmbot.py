FROM python:3.6
RUN apt-get update && \
    apt-get install -y git vim
RUN git clone https://github.com/coinpit/cpmmbot.py && \
    cd cpmmbot.py && \
    ./build.sh


