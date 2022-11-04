ARG FUNCTION_DIR="/function"
ARG PY_VERSION=3.10
ARG UBUNTU_TAG=22.04

FROM ubuntu:${UBUNTU_TAG} as build-image
ARG DEBIAN_FRONTEND=noninteractive
ARG PY_VERSION
ARG FUNCTION_DIR

# Create function directory
RUN mkdir -p ${FUNCTION_DIR}
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}


RUN apt-get update && \
    apt-get install -y mat \
                       jq \
                       httpie \
                       xvfb \
                       tesseract-ocr tesseract-ocr-chi-sim \
                       unzip \
                       software-properties-common

# install python
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python${PY_VERSION} python3-distutils python3-pip python3-apt
RUN ln -s `which python3` /usr/bin/python

# Copy requirements
COPY app/requirements.txt ${FUNCTION_DIR}/

# Install the runtime interface client
RUN python -m pip install -r ${FUNCTION_DIR}/requirements.txt   --no-cache-dir

# install playwright deps
RUN python -m playwright install-deps && \
        python -m playwright install

# Copy function code
COPY app/* ${FUNCTION_DIR}/

ENV PORT=8080
EXPOSE ${PORT}

CMD python -m gunicorn -w 4 -b :$PORT app:app --log-level debug --enable-stdio-inheritance
