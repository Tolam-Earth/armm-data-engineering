# Builds an image with Python and FastAPI configured to run
# a RESTful web service.
#
# To build the image from the root directory of the project:
#   cd <path>/hem-armm-engineering/
#   docker build -f services/nft_classifier/Dockerfile --platform amd64 -t nft-classifier .
#
# To run the container as a web service:
#   # --rm removes the container automatically when it stops running.
#   # --publish 8001:8080 exposes FastAPI's port 8080 in container as port 8001 on local machine.
#   docker run --rm --publish 8001:8080 --interactive --tty --workdir /app --name nft-classifier nft-classifier

FROM nft-base:latest

ENV PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on

RUN mkdir -p /app/hem/armm
WORKDIR /app/
COPY services/nft_classifier/requirements.txt /app/

RUN python3 -m pip install -r requirements.txt
COPY ./hem/ /app/hem/
COPY ./services/nft_classifier/*.py /app/
COPY ./services/nft_classifier/model.pkl /app/

ENV PYTHONPATH=/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
