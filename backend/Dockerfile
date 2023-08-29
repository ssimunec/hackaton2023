# set base image (host OS)
# FROM ubuntu:22.04 AS base
FROM python:3.8.13-bullseye AS base

# install dependencies
FROM base AS build
WORKDIR /app

RUN apt-get update;

ARG DEBIAN_FRONTEND=noninteractive

RUN apt install -y libgdbm-dev libc6-dev; \
	apt install -y openssl; \
	apt install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
	libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

RUN apt install libgl1-mesa-glx -y; \
	pip install cmake gcc -y; \
	mkdir /store; 


# RUN apt install git -y
# ENV HOME="/app"
# WORKDIR ${HOME}

RUN --mount=type=cache,target=/var/cache/apt \
	apt update && apt-get install -y gcc

# RUN git clone --depth=1 https://github.com/pyenv/pyenv.git .pyenv
# ENV PYENV_ROOT="${HOME}/.pyenv"
# ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"

# ENV PYTHON_VERSION=3.8.13
# RUN pyenv install ${PYTHON_VERSION}
# RUN pyenv global ${PYTHON_VERSION}

# RUN python --version
COPY "requirements.txt" requirements.txt

RUN	pip install -r requirements.txt

WORKDIR /root/.deepface/weights
RUN curl https://github.com/serengil/deepface_models/releases/download/v1.0/age_model_weights.h5 -H 'Accept: application/octet-stream' -L -O 
RUN curl https://github.com/serengil/deepface_models/releases/download/v1.0/gender_model_weights.h5 -H 'Accept: application/octet-stream' -L -O
RUN curl https://github.com/serengil/deepface_models/releases/download/v1.0/facial_expression_model_weights.h5 -H 'Accept: application/octet-stream' -L -O

WORKDIR /app

FROM build AS final
WORKDIR /app
# cache buster
ADD https://google.com cache_bust
# set the working directory in the container
# copy the content of the local src directory to the working directory
COPY . .

# command to run on container start
EXPOSE 8080

CMD [ "python", "-u", "./app.py" ]
# ENTRYPOINT ["tail", "-f", "/dev/null"]