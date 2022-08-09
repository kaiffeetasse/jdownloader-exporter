#git stash
git pull
docker build --tag jdownloader-exporter:latest .
chmod +x update.sh
docker-compose down
docker-compose up -d
