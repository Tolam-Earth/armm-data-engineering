# ARMM-Data-Engineering

**Index**

- [Developer Setup](#developer-setup)
    - [Pre-Commit Setup](#pre-commit-setup)
    - [Python Setup](#python-setup)
- [Developer Activities](#developer-activities)
    - [Unit Testing](#unit-testing)
    - [Code Coverage](#code-overage)
- [Services](#services)
- [Docker Images](#docker-images)
    - [Building an image](#building-an-image)
    - [Running a local image](#running-a-local-image)
- [License](#license)

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

### Unit Testing

We are using [pytest](https://pytest.org/) in this project. You can integrate it with most IDEs but you can also run it in your terminal:
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
rootdir: /Users/moorej/code/hem/ARMM-Data-Engineering
collected 33 items                                                                                 

tests/nft/test_geo.py ....                           [ 12%]
tests/nft/test_nft.py .................              [ 63%]
tests/nft_classifier/test_nft_classifier.py ...      [ 72%]
tests/nft_pricing/test_nft_pricing.py .....          [ 87%]
tests/nft_transformer/test_nft_transformer.py ....   [100%]

===========================================================
```

Alternatively if you're not in a poetry shell you can run with: `poetry run coverage run -m pytest`
```bash
$ poetry run coverage run -m pytest
===========================================================
platform darwin -- Python 3.10.5, pytest-7.1.2, pluggy-1.0.0
rootdir: /Users/moorej/code/hem/ARMM-Data-Engineering
collected 33 items                                                                                 

tests/nft/test_geo.py ....                           [ 12%]
tests/nft/test_nft.py .................              [ 63%]
tests/nft_classifier/test_nft_classifier.py ...      [ 72%]
tests/nft_pricing/test_nft_pricing.py .....          [ 87%]
tests/nft_transformer/test_nft_transformer.py ....   [100%]

===========================================================
```

You can then run a report to show the test coverage captured.
```bash
$ coverage report -m    
Name                                                 Stmts   Miss  Cover   Missing
----------------------------------------------------------------------------------
hem/__init__.py                                          0      0   100%
hem/armm/__init__.py                                     0      0   100%
hem/armm/clustering/__init__.py                          0      0   100%
hem/armm/clustering/model/__init__.py                    0      0   100%
hem/armm/clustering/model/basemodel.py                  13     13     0%   1-23
hem/armm/clustering/model/basemodel_GM_template.py      13      6    54%   16-19, 22-23
hem/armm/clustering/model/gridsearch.py                 10      5    50%   21-26
hem/armm/clustering/model/pipelinemodel.py              11      5    55%   9-10, 14-16
hem/armm/clustering/pool_meta/__init__.py                0      0   100%
hem/armm/clustering/pool_meta/main.py                   36     36     0%   1-51
hem/armm/clustering/predict/__init__.py                  0      0   100%
hem/armm/clustering/predict/loadmodel.py                 9      1    89%   11
hem/armm/clustering/predict/main.py                     25     10    60%   9-13, 34-39
hem/armm/clustering/preprocessing/__init__.py            0      0   100%
hem/armm/clustering/preprocessing/preprocessing.py      41     22    46%   10-29, 36-38, 43-58
hem/armm/clustering/train/__init__.py                    0      0   100%
hem/armm/clustering/train/helper.py                     10     10     0%   1-16
hem/armm/clustering/train/main.py                       35     35     0%   1-75
hem/armm/geo.py                                         23      2    91%   39-40
hem/armm/handlers.py                                     6      0   100%
hem/armm/nft.py                                        103      0   100%
hem/armm/pricing/main.py                                27     13    52%   11-18, 33-40
hem/armm/pricing/pricing.py                             19      0   100%
----------------------------------------------------------------------------------
TOTAL                                                  381    158    59%
```
The same as before, if you're not in a poetry shell use `poetry run coverage report -m`.

## Services
- [NFT Transformer](./services/nft_transformer)
    - A RESTful microservice that transforms and augments NFT Detail data as needed for downstream machine learning applications.
    - It is deployed within the dataflow to ingest NFT Detail data.
- [NFT Classifier](./services/nft_classifier)
    - A RESTful microservice that classifies an NFT to an NFT pool.
    - It is deployed within the dataflow to ingest NFT Detail data.
- [NFT Pricing](./services/nft_pricing)
    - A RESTful microservice that estimates a price range for a set of NFTs in a pool.
    - It is deployed within the pricing dataflow.

## Docker Images
### Building an image
Build component images from the root directory of the project:
```bash
cd <path>/ARMM-Data-Engineering/
docker build -f services/nft_base/Dockerfile --platform amd64 -t nft-base .
docker build -f services/nft_transformer/Dockerfile --platform amd64 -t nft-transformer .
docker build -f services/nft_classifier/Dockerfile --platform amd64 -t nft-classifier .
docker build -f services/nft_pricing/Dockerfile --platform amd64 -t nft-pricing .
```

#### Naming conventions

- The source code directories are named with underscores, e.g. `nft_classifier`.
- However, the service names use hyphens, e.g. `nft-classifier`.

#### Target architectures
Some members of the development team use a MacBook with an M1 chip as their
development machine. 
The default behavior on those machines when building a Docker image is to
build an image for the `arm64` chip architecture. 
But GCP virtual machines and most other developers
on the team need an `amd64` build.
It is possible to build to a specific architecture
in the docker `build` command by using the `--platform` option. 
That is why we use the `--platform amd64` option in the commands above.

You can identify the target architecture of an image by using the `inspect` command.
For example:
```bash
docker image inspect nft-classifier
```

### Running a local image
To run the images built in the previous section as web services:
```bash
docker run --rm --publish 8000:8080 \
    --interactive --tty \
    --workdir /app \
    --name nft-transformer \
    nft-transformer:latest 
docker run --rm --publish 8001:8080 \
    --interactive --tty \
    --workdir /app \
    --name nft-classifier \
    nft-classifier:latest 
docker run --rm --publish 8002:8080 \
    --interactive --tty \
    --workdir /app \
    --name nft-pricing \
    nft-pricing:latest 
```
where:

- `--rm` removes the container automatically when it stops running.
- `--publish 8001:8080` exposes FastAPI's port 8080 from the container as port 8001 on the local machine. If you have more than one web service running, you will need to choose a different port for each service. Each container will expose `8080`, but you can map that to `8000`, `8001`, `8002`, ... or any other available ports on the machine that is running the container.
- `--name nft-classifier` names the container, so it is easy to identify from `docker ps` output.

The order in which you start the images does not matter. 
They are independent of each other.

## License
Copyright &copy; 2022 Tolam Earth

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at 

http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
