FROM ubuntu:xenial
RUN apt-get update && \
    apt-get install -y git vim python3 build-essential libssl-dev libffi-dev python3-dev python3-venv && \
    cd /root && \
    mkdir environments && \
    cd environments && \
    python3 -m venv my_env

#RUN /bin/bash -c "source /root/environments/my_env/bin/activate"
#RUN source my_env/bin/activate

RUN cd && git clone https://github.com/coinpit/cpmmbot.py && \
    cd cpmmbot.py    && \
    /bin/bash -c "source /root/environments/my_env/bin/activate; ./build.sh"

#ENTRYPOINT /bin/bash -c "source /root/environments/my_env/bin/activate"
