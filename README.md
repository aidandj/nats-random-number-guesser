# Nats.io random number guesser

Just some experiments with [nats.io](https://nats.io/)

## Server

Generates a random number, and creates helpers to help guess the number

## Client

Tries to guess the number. Keeps track of previous guesses

## nats.io server

I used this `docker-compose.yml` to stand up the server.

```yml
version: "3"
services:
  nats:
    image: nats
    ports:
      - "8222:8222"
  nats-1:
    image: nats
    command: "--cluster nats://0.0.0.0:6222 --routes=nats://ruser:T0pS3cr3t@nats:6222"
  nats-2:
    image: nats
    command: "--cluster nats://0.0.0.0:6222 --routes=nats://ruser:T0pS3cr3t@nats:6222"
networks:
  default:
    external:
      name: nats
```