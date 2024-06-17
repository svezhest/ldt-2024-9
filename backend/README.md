docker buildx build --platform linux/amd64 -t my-fastapi-app:latest .
docker save -o my-fastapi-app.tar my-fastapi-app:latest
