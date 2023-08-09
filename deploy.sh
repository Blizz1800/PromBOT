git pull origin mongo
docker build -t bot . --network=host
docker rm -f bot
docker run --name bot --network=host -ti -d bot