# Running the bot in Docker

## Update env file with your credentials
update and rename .env.example to .env

## Build docker image
From the root of the project, run this docker build command: `docker build -t reddit_karma_bot:latest . --no-cache`

## Run Docker Image
`docker run -d --name=reddit-bot reddit_karma_bot:latest`

## View Logs
`docker logs -f reddit-bot`

# Using Docker Compose

## Create docker-compose.yml and fill it with your credentials

```
version: "3"
services:
  redditkarma:
    image: docker pull ghcr.io/MrPowerScripts/reddit-karma-farming-bot:master
    environment:
      - TZ=Europe/Berlin
      - bot_reddit_client_id=ZV9O7nswP9Di0Q
      - bot_reddit_client_secret=rhYRuNSFY-VMGtCXHvk2_4deSm_Q
      - bot_reddit_password=DontBanMeBro!
      - bot_reddit_username=DontBanMeBro
```
## Run it in the background
`docker-compose up -d`
