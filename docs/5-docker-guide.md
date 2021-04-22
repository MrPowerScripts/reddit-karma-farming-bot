# Running the bot in Docker


## Build docker image
From the root of the project, run this docker build command: `docker build -t reddit_karma_bot:latest . --no-cache`

## Run Docker Image
docker run -d \
  --name=reddit-bot \
  -env=.env \
  reddit_karma_bot:latest
