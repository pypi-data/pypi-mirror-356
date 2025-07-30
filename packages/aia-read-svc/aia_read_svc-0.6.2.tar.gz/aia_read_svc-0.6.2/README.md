---
runme:
  id: 01HJQE75SKBTCT1QQK59F1AVR6
  version: v3
---

# aia-read-svc

AIA Read Service

```sh {"id":"01HJQE75SKBTCT1QQK57A0T1JR"}
poetry run daemon

git ls-remote --get-url origin 
git remote set-url origin git@github.com:ranmadxs/aia-read-svc.git



#tags
git push --tags

git push --delete origin $AIA_TAG_READ
```

## Docker

```sh {"id":"01HJV2GKHFHRCW2MAYBX6DWF7V"}
#set var entorno
export AIA_TAG_READ=v0.6.2
```

```sh {"id":"01HJQ7F9RXZBJJ4YEQAAH1BXHZ"}
#build
docker build . --platform linux/arm64/v8 -t keitarodxs/aia-read-svc:$AIA_TAG_READ

#push
docker push keitarodxs/aia-read-svc:$AIA_TAG_READ

#go into docker container
sudo docker exec -ti aia_read_svc bash

#run
docker run -d --restart=always -e TZ=America/Santiago -v /home/ranmadxs/aia/aia-device/resources/images:/wh40k_images -v /home/ranmadxs/aia/aia-read-svc/target:/app/target --net=bridge --name aia_read_svc --env-file .env keitarodxs/aia-read-svc:$AIA_TAG_READ

docker run --rm -e TZ=America/Santiago -v /home/ranmadxs/aia/aia-device/resources/images:/wh40k_images -v /home/ranmadxs/aia/aia-read-svc/target:/app/target --net=bridge --name aia_read_svc --env-file .env keitarodxs/aia-read-svc:$AIA_TAG_READ

```

```sh {"id":"01HKRRFAZ7Y6SB5N6ZM1S9Q3MM"}
#other commands
docker save -o $AIA_TAG_READ.tar keitarodxs/aia-read-svc:$AIA_TAG_READ

docker load -i $AIA_TAG_READ.tar
```

