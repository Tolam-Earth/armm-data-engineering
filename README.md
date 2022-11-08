# hem-armm-engineering

**Index**

- [Developer Setup](#developer-setup)
    - [Pre-Commit Setup](#pre-commit-setup)
    - [Python Setup](#python-setup)
- [Developer Activities](#developer-activities)
    - [Testing](#testing)
    - [Code Coverage](#code-overage)
- [Services](#services)
- [Docker Images](#docker-images)
    - [Building an image](#building-an-image)
    - [Running an image](#running-an-image)
    - [Pushing an image to the Artifact Registry](#pushing-an-image-to-the-artifact-registry)
- [Copyright](#copyright)

---

## Developer Setup

### Pre-Commit Setup
1. Install [pre-commit](https://pre-commit.com/#install)
   1. You may need to add the installation location to your PATH. If you are on macOS brew installation is recommended.
2. Install [autopep8](https://pypi.org/project/autopep8/)
   1. Ensure `autopep8` is available in your PATH where you run your commits. e.g. a base conda or pyenv environment

Optional: Add to your IDE
* https://github.com/hscgavin/autopep8-on-pycharm
* https://code.visualstudio.com/docs/python/editing#_general-formatting-settings

3. Install the pre-commit git hooks
```
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

Note: When updating [.pre-commit-config.yaml](.pre-commit-config.yaml), re-run the `pre-commit install` command and then run on all files:
```
$ pre-commit run --all-files
```

### Python Setup

You can utilize [pyenv](https://github.com/pyenv/pyenv) or [conda](https://docs.conda.io/en/latest/) for setting up your base python interpreter(s).

1. Install [Poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer) if you have not installed on your machine
2. Install project dependencies into poetry environment: `poetry install`
 
General Poetry usage:
Use your poetry environment defined by [pyproject.toml](pyproject.toml). How to: https://python-poetry.org/docs/master/basic-usage/#activating-the-virtual-environment

Adding Dependencies
https://python-poetry.org/docs/master/basic-usage/#specifying-dependencies
Adding development only dependencies (e.g. tools for testing, code coverage, etc.)
`poetry add $PACKAGE --dev`
This will change in Poetry 1.2 to use the groups syntax `poetry add $PACKAGE --group dev`

Note: If you modify the pyproject.toml dependencies directly (as opposed to using `poetry add $PACKAGE` you may need to run `poetry update` to update the lockfile)

Need requirements.txt for a build process that does not support poetry?
```
poetry export -f requirements.txt --output requirements.txt
```

## Developer Activities

### Testing

We are using pytest in this project. You can integrate it with most IDEs but you can also run it in your terminal:
```
poetry run pytest tests/

# if in a poetry shell
pytest tests/
```

### Code Coverage

[Python Coverage Library](https://coverage.readthedocs.io/en/6.4.2/)

The `coverage` command should not need extra installation steps as it is a defined dev dependency in pyproject.toml and poetry should install it for you. However, if you're in another environment or using it elsewhere it can simply be installed with `pip install coverage`.

```
$ coverage run -m pytest
===========================================================
platform darwin -- Python 3.10.5, pytest-7.1.2, pluggy-1.0.0
rootdir: /Users/moorej/code/hem/hem-armm-engineering
collected 2 items

tests/test_armm.py ..                                [100%]

===========================================================
```

Alternatively if you're not in a poetry shell you can run with: `poetry run coverage run -m pytest`
```
$ poetry run coverage run -m pytest
===========================================================
platform darwin -- Python 3.10.5, pytest-7.1.2, pluggy-1.0.0
rootdir: /Users/moorej/code/hem/hem-armm-engineering
collected 2 items

tests/test_armm.py ..                                [100%]

===========================================================
```

You can then run a report to show the test coverage captured.
```
$ coverage report -m    
Name                   Stmts   Miss  Cover   Missing
----------------------------------------------------
hem/__init__.py            0      0   100%
hem/armm/__init__.py       3      0   100%
tests/test_armm.py         7      0   100%
----------------------------------------------------
TOTAL                     10      0   100%

```
The same as before, if you're not in a poetry shell use `poetry run coverage report -m`.

## Services
- [NFT Transformer](./services/nft_transformer)
- [NFT Classifier](./services/nft_classifier)

## Docker Images
### Building an image
Build the image from the root directory of the project. For example,
```bash
cd <path>/hem-armm-engineering/
docker build -f services/nft_classifier/Dockerfile -t nft-classifier .
```
#### Naming conventions

- The source code directories are named with underscores, e.g. `nft_classifier`.
- However, the service names use hyphens, e.g. `nft-classifier`.

#### Target architectures
Some members of the development team use a MacBook with an M1 chip.
The default behavior on those machines when building a Docker image is to build an image for
the `arm64` chip architecture. But GCP virtual machines and most other developers
on the team need an `amd64` build. It is possible to build to a specific architecture
in the docker `build` command by using the `--platform` option, such as:
```bash
docker build -f services/nft_transformer/Dockerfile --platform amd64 -t nft-transformer .
```

You can identify the target architecture of an image by using the `inspect` command.
For example:
```bash
docker image inspect us-central1-docker.pkg.dev/armm-sandbox/hem-armm/nft-classifier:latest
```
or for a local image:
```bash
docker image inspect nft-classifier
```

### Running an image
To run the image as a web service:
```bash
docker run --rm --publish 8000:8080 \
    --interactive --tty \
    --workdir /app \
    --name nft-transformer \
    us-central1-docker.pkg.dev/armm-sandbox/hem-armm/nft-transformer:latest 
```
where:

- `--rm` removes the container automatically when it stops running.
- `--publish 8000:8080` exposes FastAPI's port 8080 from the container as port 8000 on the local machine. If you have more than one web service running, you will need to choose a different port for each service. Each container will expose `8080`, but you can map that to `8000`, `8001`, `8002`, ... or any other available ports on the machine that is running the container.
- `--name nft-classifier` names the container, so it is easy to identify from `docker ps` output.

### Pushing an image to the Artifact Registry
These steps are based on the [Google Artifact Registry documentation](https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling#pushing).

- Make sure your Docker config file is configured for the gcloud credential helper:
    - `cat ~/.docker/config.json`
    - If necessary, set the configuration for the [ARMM Artifact Registry](https://console.cloud.google.com/artifacts/docker/armm-sandbox/us-central1/hem-armm?project=armm-sandbox),
        which is in the `us-central1` region:
        - `gcloud auth configure-docker us-central1-docker.pkg.dev`
- Tag the local image. This example is for the `nft-transformer` service:
    - `docker tag nft-transformer:latest us-central1-docker.pkg.dev/armm-sandbox/hem-armm/nft-transformer:latest`
- Push the tagged image to the registry:
    - `docker push us-central1-docker.pkg.dev/armm-sandbox/hem-armm/nft-transformer:latest`

## Copyright
Copyright &copy; 2022 Object Computing, Inc.
