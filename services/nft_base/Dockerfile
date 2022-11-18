# inspired by https://luis-sena.medium.com/creating-the-perfect-python-dockerfile-51bdec41f1c8
# Builds a base image with Python to be used for services
#
# To build the image from the root directory of the project:
#   cd <path>/ARMM-Data-Engineering/
#   docker build -f services/nft_base/Dockerfile --platform amd64 -t nft-base .
FROM ubuntu:22.04 as builder

# install base python3.10 needs
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y python3.10 python3.10-dev python3.10-venv python3-pip python3-wheel build-essential curl && \
    apt-get clean

# virtualenv
RUN python3.10 -m venv /home/app_user/venv
ENV PATH="/home/app_user/venv/bin:$PATH"

# install poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry && \
    poetry config virtualenvs.create false

# install poetry dependencies
WORKDIR /tmp
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# runner stage so we don't need to carry poetry in our final build
FROM ubuntu:22.04 as runner

# install base python3.10 needs
# Repetitive from builder image but should be a cached layer as long as we keep them identical
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y python3.10 python3.10-dev python3.10-venv python3-pip python3-wheel build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# create non-root user
RUN addgroup --gid 10002 app_group && adduser --system --uid 10001 --gid 10002 app_user
COPY --from=builder /home/app_user/venv /home/app_user/venv

# directory permissions
RUN mkdir /app && chown app_user /app && chown -R app_user /home/app_user/venv

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/home/app_user/venv
ENV PATH="/home/app_user/venv/bin:$PATH"

# switch over to non-root app_user for runtime
USER app_user
CMD ["echo", "!!This is a base image. Do not use directly!!"]
