# Builds an image with Python and FastAPI configured to run
# a RESTful web service.
#
# To build the image from the root directory of the project:
#   cd <path>/hem-armm-engineering/
#   docker build -f services/nft_pricing/Dockerfile --platform amd64 -t nft-pricing .
#
# To run the container as a web service:
#   # --rm removes the container automatically when it stops running.
#   # --publish 8001:8080 exposes FastAPI's port 8080 in container as port 8001 on local machine.
#   docker run --rm --publish 8002:8080 --interactive --tty --workdir /app --name nft-pricing nft-pricing
#
# To push the image to the repository:
#   Tag the local image:
#     docker tag nft-pricing:latest us-central1-docker.pkg.dev/armm-sandbox/hem-armm/nft-pricing:latest
#   Push the tagged image to the registry:
#     docker push us-central1-docker.pkg.dev/armm-sandbox/hem-armm/nft-pricing:latest

FROM us-central1-docker.pkg.dev/armm-sandbox/hem-armm/nft-base:latest

ENV PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on

RUN mkdir -p /app/hem/armm/pricing
WORKDIR /app/
COPY ./hem/*.py hem/
COPY ./hem/armm/*.py hem/armm/
COPY ./hem/armm/pricing/*.py hem/armm/pricing/

COPY ./services/nft_pricing/*.py .
COPY ./services/nft_pricing/requirements.txt .
RUN python3 -m pip install -r requirements.txt

ENV PYTHONPATH=/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
