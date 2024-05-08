FROM ubuntu:rolling
WORKDIR /root

RUN apt update && \
        apt -y install git python3-pip

# install aitoolbox support
RUN pip3 install --break-system-packages git+https://github.com/hollosigergely/aitoolbox_support_library.git


# install requirements (we ignore breaking system packages in docker container)
COPY requirements.txt .
RUN pip3 install --break-system-packages -r requirements.txt


COPY src/ .

CMD ["python3", "main.py"]
EXPOSE 80