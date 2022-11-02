ARG FUNCTION_DIR="/function"

FROM mcr.microsoft.com/playwright/python:latest

ARG FUNCTION_DIR

# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}


RUN apt-get update && \
    apt-get install -y mat \
                       jq \
                       httpie \
                       tesseract-ocr tesseract-ocr-chi-sim \
                       unzip

# Copy requirements
COPY app/requirements.txt ${FUNCTION_DIR}/

# Install the runtime interface client
RUN python -m pip install -r ${FUNCTION_DIR}/requirements.txt   --no-cache-dir

# Copy function code
COPY app/* ${FUNCTION_DIR}/

ENV PORT=8080
EXPOSE ${PORT}

CMD python -m gunicorn -w 4 -b :$PORT app:app --log-level debug --enable-stdio-inheritance
