#docker run -p 5433:5432 -d postgres postgres
#sleep 5
docker run --network host--detach --name "api1" api
docker run --network host --detach --name "handler1" handler
docker run --network host --detach --name "handler2" handler
docker run --network host --detach --name "handler3" handler
docker run --network host --detach --name "handler4" handler
docker run --network host --detach --name "handler5" handler
docker run --network host --detach --name "handler6" handler
docker run --network host --detach --name "handler7" handler
docker run --network host --detach --name "handler8" handler
docker run --network host --detach --name "handler9" handler
docker run --network host --detach --name "handler10" handler
docker run --network host --detach --name "janitor1" janitor
docker run --network host --detach --name "janitor2" janitor
docker run --network host --detach --name "janitor3" janitor
