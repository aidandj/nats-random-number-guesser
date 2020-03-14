# Nats.io random number guesser

Just some experiments with [nats.io](https://nats.io/)

## Server

* Generates a random number, and creates helpers to help guess the number
* Dockerfile that sets up `pipenv` for the server
* This container gets pushed to Dockerhub and used by the main `docker-compose.yml`

## Client

* Tries to guess the number. Keeps track of previous guesses
* Dockerfile that sets up `pipenv` for the client
* This container gets pushed to Dockerhub and used by the main `docker-compose.yml`

## docker-compose.yml

This `docker-compose` will bring up a network of nats.io servers, along with the server and client services. The server container will start automatically, the client container is sitting ready to be connected to. I use `VSCode` to attach a shell to the client container, then run `python client.py`

The python client and server get pulled from my Dockerhub

## Instructions

1. `docker network create nats`
2. `docker-compose up`
3. Attach to client container
4. `python client.py`