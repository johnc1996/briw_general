
# briw-general base 


### Setting environment variables
Add an environment variable for your user
BRIW_USER_EMAIL="brianallan@gmail.com"; export BRIW_USER_EMAIL



### To generate a development environment
docker run --rm   --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres