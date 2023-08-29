# set base image (host OS)
FROM python:3.8.13 AS base

# install dependencies
FROM base AS build
WORKDIR /app
COPY "requirements.txt" requirements.txt

RUN apt-get update;
RUN apt install -y libgdbm-dev libc6-dev; \
	apt install -y openssl; \
	apt install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
	libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev


RUN apt install libgl1-mesa-glx -y; \
	pip install cmake; \
	mkdir /store; 

# RUN pip install -r requirements.txt

FROM build AS final
# cache buster
ADD https://google.com cache_bust
# set the working directory in the container
# copy the content of the local src directory to the working directory
COPY . .

# command to run on container start
# CMD [ "python", "-u", "./main.py" ]
ENTRYPOINT ["tail", "-f", "/dev/null"]