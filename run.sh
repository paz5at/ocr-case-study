IMAGE_NAME="ocr-service:latest"

echo "building docker image"
docker build -t $IMAGE_NAME .

echo "starting docker container"
docker run --rm -p 8080:8080 $IMAGE_NAME