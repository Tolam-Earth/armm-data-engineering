# How to Run Docker Containers Locally
This document outlines the process to pull down and launch docker images from the artifact repository on Google Cloud.

## Preparing Your Environment

The hem-armm-engineering containers are launched using the docker-compose tool.  There are several steps that you need to complete prior to running this command.

### Installation of Docker

First you will need to install Docker by navigating [here](https://docs.docker.com/get-docker/).  Follow the links provided to install Docker for your operating system.   

**Note:** Docker is licensed software and you will need a license appropriate to your situation in order to use Docker Desktop.

## Create the Docker Images

In order to run the containers you will need to prepare each of the images as outlined below
1. The Orchestrator Daemon is located in the hem-armm-services repository.
   From the orchestrator-daemon subdirectory issue the following command:
   ~~~
   ../gradlew dockerBuild
   ~~~
2. The Pricing Daemon is located in the hem-armm-services repository.
   From the pricing-daemon subdirectory issue the following command:
   ~~~
   ../gradlew dockerBuild
   ~~~
3. The Trader Evaluator is located in the hem-armm-services repository.
   From the trader-evaluator subdirectory issue the following command:
   ~~~
   ../gradlew dockerBuild
   ~~~
4. The base image is located in the hem-armm-engieneering repository.
   From the root issue the following command:
   ~~~
   docker build -f ./services/nft_base/Dockerfile --platform amd64 -t nft-base .
   ~~~
5. The NFT Classifier is located in the hem-armm-engineering repository.
   From the root issue the following command:
   ~~~
   docker build -f ./services/nft_classifier/Dockerfile --platform amd64 -t nft-classifier .
   ~~~
6. NFT Pricing is located in the hem-armm-engineering repository.
   From the root issue the following command:
   ~~~
   docker build -f ./services/nft_pricing/Dockerfile --platform amd64 -t nft-pricing .
   ~~~
7. The NFT Transformer is located in the hem-armm-engineering repository.
   From the root issue the following command:
   ~~~
   docker build -f ./services/nft_transformer/Dockerfile --platform amd64 -t nft-transformer .
   ~~~
   

## Running the Containers

Open a terminal and navigate to the top level directory of this repository after cloning.  This is the location of the docker-compose-tolam-earth.yml file that the docker-compose tool will utilize when launching the environment.

Execute the following command:
~~~
docker-compose -f docker-compose-tolam-earth up
~~~

It will take a couple of minutes as additional containers build and launch.  You will know the process is complete once you see a steady stream of logging from the containers to the terminal.

Verify that all of the containers are healthy and running by opening a new terminal on your system and executing the following command:
~~~
docker ps -a
~~~
When all containers display a status of 'up' you have a running environment.  If any of the containers have a status of 'exited' there were problems when trying to run that container.  
