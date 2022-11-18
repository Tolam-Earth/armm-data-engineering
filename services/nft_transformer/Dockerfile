# Builds an image with Python and FastAPI configured to run
# a RESTful web service.
#
# To build the image from the root directory of the project:
#   cd <path>/hem-armm-engineering/
#   docker build -f services/nft_transformer/Dockerfile --platform amd64 -t nft-transformer .
#
# To run the container as a web service:
#   # --rm removes the container automatically when it stops running.
#   # --publish 8000:8080 exposes FastAPI's port 8080 in container as port 8000 on local machine.
#   docker run --rm --publish 8000:8080 --interactive --tty --workdir /app --name nft-transformer nft-transformer

FROM nft-base:latest

ENV PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on

RUN mkdir -p /app/hem/armm
WORKDIR /app/
# TODO: build and install with poetry in base image
COPY ./hem/*.py hem/
COPY ./hem/armm/*.py hem/armm/
COPY ./hem/armm/data/ hem/armm/data

COPY ./services/nft_transformer/*.py /app/
COPY ./services/nft_transformer/requirements.txt .
RUN python3 -m pip install -r requirements.txt

ENV PYTHONPATH=/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
