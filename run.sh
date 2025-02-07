#TODO 
docker build . -t ynov-api-image

docker run ynov-api-image -p 8000:4242 -e PORT=4242 -v "${pwd}:/home/app" -it ynov-api-image